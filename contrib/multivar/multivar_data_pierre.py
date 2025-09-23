from contrib.moving_patches.movpatch_data_tests import MovingPatchDataModuleFastRecGPU, XrDatasetMovingPatchFastRecGPU, XrDatasetMovingPatchFastRecGPUNoFullNaN
from contrib.multivar.multivar_utils import MultivarBatchSelector
import numpy as np
import xarray as xr
import functools as ft
import torch
import time
from dask.diagnostics.progress import ProgressBar

#from pathlib import Path


class MultivarXrDataset(XrDatasetMovingPatchFastRecGPU):
    def __init__(self, *args, aug_dims=None, aug_dims_noise=None, aug_dims_offset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.aug_dims = aug_dims
        self.aug_dims_noise = aug_dims_noise
        self.aug_dims_offset = aug_dims_offset
        self._rng = np.random.default_rng()

        if self.aug_dims is not None:
            self.time_perm = np.random.permutation(self.da_dims['time'])
    
    def apply_augmentation(self, item, sl):

        if self.aug_dims is None and self.aug_dims_noise is None and self.aug_dims_offset is None:
            return item
        
        #print("Apply_augmentation")

        if self.aug_dims is not None: 
            for (aug_input_idx, aug_target_idx) in self.aug_dims:
                sl_aug = sl.copy()
                sl_aug['time'] = self.time_perm[sl['time']]
                aug_item = self.da.isel(**sl_aug)
                aug_item_input = np.where(np.isfinite(aug_item.values[aug_input_idx,:]), item.values[aug_target_idx,:], np.full_like(aug_item.values[aug_target_idx,:], np.nan))
                item.values[aug_input_idx,:] = aug_item_input

        if self.aug_dims_noise is not None:
            for (aug_noise_idx, aug_noise_value) in self.aug_dims_noise:
                noise = self._rng.uniform(-aug_noise_value, aug_noise_value, item.values[aug_noise_idx].shape).astype(np.float32)
                item.values[aug_noise_idx] = item.values[aug_noise_idx] + noise

    def get_coords_leadtime(self):
        self.return_coords = True
        coords_sizes = []
        coords_slices = []
        try:
            for i in range(len(self)):
                coords_size, coords_slice = self[i]
                coords_sizes.append(coords_size)
                coords_slices.append(coords_slice)
        finally:
            self.return_coords = False
            return coords_sizes, coords_slices

    def reconstruct_from_items(self, items: torch.Tensor, weight=None, leadtime=0):
        """
            Reconstruction of patches that can contain padded patches
        """

        # getting coords
        start_time = time.time()
        coords_slices = self.get_coords()

        coords_dims = self.patch_dims
        
        new_dims = [f'v{i}' for i in range(len(items[0].cpu().shape) - len(coords_dims))]
        dims = new_dims + list(coords_dims)

        new_shape = items[0].shape[:len(new_dims)]
        full_unpadded_shape = [*new_shape, *self.get_unpadded_dims()]
        #full_padded_shape = [*new_shape, *self.get_padded_dims()]

        # create cuda slices
        full_slices = []
        time_cut = items[0].size(dim=1)
        for idx, coord_slices in enumerate(coords_slices):
            coord_slices['time'] = np.arange(coord_slices['time'][leadtime], coord_slices['time'][leadtime] + time_cut)
            full_slices.append(np.ix_(*([np.arange(len_new_dim) for len_new_dim in full_unpadded_shape[:len(new_dims)]]+list(coord_slices.values()))))

        # create cuda tensors
        #rec_tensor = torch.zeros(size=full_padded_shape).cuda()
        #count_tensor = torch.zeros(size=full_padded_shape).cuda()
        rec_tensor = torch.zeros(size=full_unpadded_shape).cuda()
        count_tensor = torch.zeros(size=full_unpadded_shape).cuda()
        w = torch.tensor(weight).cuda()

        for idx in range(items.size(0)):
            rec_tensor[full_slices[idx]] += items[idx] * w
            count_tensor[full_slices[idx]] += w
        result_tensor = (rec_tensor / count_tensor).cpu()
        #result_array = np.array(result_tensor[[slice(0,max_shape) for max_shape in full_unpadded_shape]])
        result_array = result_tensor.numpy()

        result_da = xr.DataArray(
            result_array,
            dims=dims,
            coords={d: self.da[d] for d in self.patch_dims},
        )

        print('total reconstruction time: {:.3f}'.format(time.time() - start_time))
        return result_da

class MultivarDataModule(MovingPatchDataModuleFastRecGPU):

    def __init__(self, multivar_da, domains, xrds_kw, dl_kw, norm_stats=None, aug_dims=None, aug_dims_noise=None, aug_dims_offset=None, **kwargs):
        self.input_da, self.multivar_information = multivar_da
        #print(self.input_da.sel(variable="u_drifter").mean(skipna=True).values.item())
        self.aug_dims = aug_dims
        self.aug_dims_noise = aug_dims_noise
        self.aug_dims_offset=aug_dims_offset
        self._norm_stats = norm_stats
        super().__init__(self.input_da, domains, xrds_kw, dl_kw, norm_stats=norm_stats, **kwargs)
        self.multivar_info()

    # Modified by TP to add norm stat defined option
    def norm_stats(self):
        if self._norm_stats is None:
            self._norm_stats = self.train_mean_std()
            print("Norm stats computed", self._norm_stats)
        else:
            self._norm_stats = (np.array(self._norm_stats[0]),np.array(self._norm_stats[1]))
            print("Norm stats defined", self._norm_stats)

        """
        #save norm_stats
        if self.logger:
            print(f"Saving norm at : {Path(self.logger.log_dir)}")
            with open(f"{Path(self.logger.log_dir)}"+'/norm_stats.pkl', 'wb') as f:
                pickle.dump(self._norm_stats, f)
        else:
            print("No self.logger")
        """
        
        return self._norm_stats
    
    def placeholder_norm_stats(self):
        return 0., 1.

    def output_norm_stats(self):
        m,s = self._norm_stats[0][self.multivar_info_dict['full_output_idx']], self._norm_stats[1][self.multivar_info_dict['full_output_idx']]
        return m, s
    
    def input_norm_stats(self):
        return self._norm_stats[0][self.multivar_info_dict['full_input_idx']], self._norm_stats[1][self.multivar_info_dict['full_input_idx']]

    def train_mean_std(self):
        m = []
        s = []

        print("Computing mean and std of training dataset ...")
        
        #print(self.domains['train'])

        data = self.input_da.sel(self.xrds_kw.get('domain_limits', {})).sel(self.domains['train'])

        #print(data)

        for var, var_information in self.multivar_information.items():
            if var.startswith('masked_'):
                m_var, s_var = data.sel(variable=var.split('masked_')[1]).pipe(lambda da: (da.mean().values.item(), da.std().values.item()))
            else:
                #TP modif nanmean
                m_var, s_var = data.sel(variable=var).pipe(lambda da: (da.mean(skipna=True).values.item(), da.std(skipna=True).values.item()))

            m.append(m_var)
            s.append(s_var)
        return np.array(m), np.array(s)

    def post_fn(self):
        
        m, s = self.norm_stats()
        def normalize(item):
            item_shape_len = len(item.shape)
            return (item - np.expand_dims(m, tuple(range(1, item_shape_len)))) / np.expand_dims(s, tuple(range(1, item_shape_len)))

        return normalize

    def setup(self, stage='test'):
        # calling MovingPatch Datasets, rand=True for train only

        post_fn = self.post_fn()
        self.train_ds = MultivarXrDataset(
            self.input_da.sel(self.domains['train']), **self.xrds_kw, aug_dims=self.aug_dims,aug_dims_noise=self.aug_dims_noise, aug_dims_offset=self.aug_dims_offset, postpro_fn=post_fn, rand=True
        )
        self.val_ds = MultivarXrDataset(
            self.input_da.sel(self.domains['val']), **self.xrds_kw, postpro_fn=post_fn, rand=False, aug_dims_offset=self.aug_dims_offset
        )
        self.test_ds = MultivarXrDataset(
            self.input_da.sel(self.domains['test']), **self.xrds_kw, postpro_fn=post_fn, rand=False, aug_dims_offset=self.aug_dims_offset
        )

    def multivar_info(self):
        full_input_idx = []
        prior_input_idx = []
        full_output_idx = []
        state_obs_channels = []
        state_obs_input_idx = []
        masked_state_obs_input_idx = []
        len_time_channels = self.xrds_kw.patch_dims['time']

        for idx, (var, var_information) in enumerate(self.multivar_information.items()):
            if var_information['input_arch'] == 'full_input':
                full_input_idx.append(idx)
                if var_information['output_arch'] == 'full_output':
                    state_obs_input_idx.append(idx)
                if 'masked_obs' in list(var_information.keys()):
                    state_obs_input_idx.append(idx)
                    # ASSUMES THAT MASKED_OBS IMPLIES THAT ITS UNMASKED VERSION IS A FULL OUTPUT
                    masked_state_obs_input_idx.append(idx+1)
            elif var_information['input_arch'] == 'prior_input':
                prior_input_idx.append(idx)
            if var_information['output_arch'] == 'full_output':
                full_output_idx.append(idx)

        for state_obs_input in state_obs_input_idx:
            if state_obs_input in list(full_output_idx):
                idx = np.argwhere(np.array(full_output_idx) == state_obs_input).item()
                state_obs_channels.extend([idx*len_time_channels+i for i in range(len_time_channels)])

        for masked_state_obs_input in masked_state_obs_input_idx:
            if masked_state_obs_input in list(full_output_idx):
                idx = np.argwhere(np.array(full_output_idx) == masked_state_obs_input).item()
                state_obs_channels.extend([idx*len_time_channels+i for i in range(len_time_channels)])
                
        multivar_info = dict(
            full_input_idx = full_input_idx,
            prior_input_idx = prior_input_idx,
            full_output_idx = full_output_idx,
            state_obs_channels = state_obs_channels,
            state_obs_input_idx = state_obs_input_idx,
            var_names = list(self.multivar_information.keys())
        )
        self.multivar_info_dict = multivar_info

        batch_selector = MultivarBatchSelector()
        batch_selector.multivar_setup(multivar_info)

class MultivarNfNXrDataset(MultivarXrDataset, XrDatasetMovingPatchFastRecGPUNoFullNaN):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MultivarNfNDataModule(MultivarDataModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, stage='test'):
        # calling MovingPatch Datasets, rand=True for train only
        post_fn = self.post_fn()
        self.train_ds = MultivarNfNXrDataset(
            self.input_da.sel(self.domains['train']), **self.xrds_kw, aug_dims=self.aug_dims, aug_dims_noise=self.aug_dims_noise, aug_dims_offset=self.aug_dims_offset, postpro_fn=post_fn, rand=True
        )
        self.val_ds = MultivarNfNXrDataset(
            self.input_da.sel(self.domains['val']), **self.xrds_kw, postpro_fn=post_fn, rand=False, aug_dims_offset=self.aug_dims_offset
        )
        self.test_ds = MultivarNfNXrDataset(
            self.input_da.sel(self.domains['test']), **self.xrds_kw, postpro_fn=post_fn, rand=False, aug_dims_offset=self.aug_dims_offset
        )
            