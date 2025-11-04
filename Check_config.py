import multiprocessing as mp
mp.set_start_method("spawn", force=True)

import os


os.environ["HYDRA_FULL_ERROR"] = "1"

import hydra
with hydra.initialize('config', version_base='1.3'):
    cfg = hydra.compose("main", overrides=[
        'xp=unet_uv_drifters_test_2'
    ])

#mutivar_da = hydra.utils.call(cfg.datamodule.multivar_da)

#lit_mod = hydra.utils.call(cfg.model)

#breakpoint()
dm = hydra.utils.call(cfg.datamodule) # will instantiate src.data.BaseDataModule with parameters specified in config
dm.setup() # setup the datamodule see https://lightning.ai/docs/pytorch/stable/data/datamodule.html#lightningdatamodule-api*

train_dl = dm.train_dataloader() # # Split data into batch, selection of the etrainuation data + Computation of norm / Augmentation
train_ds = train_dl.dataset 
input_data = train_ds


from pytorch_lightning import Trainer

trainer = Trainer(
  inference_mode=False,
  gradient_clip_val=0.5,
  accelerator='gpu',
  devices=1,
  #fast_dev_run=True,
  limit_train_batches=1,  # Utilise seulement 10% des batches d'entraînement
  limit_val_batches=1,    # Utilise seulement 10% des batches de validation
)

import torch 
lit_mod = hydra.utils.call(cfg.model)

trainer.fit(lit_mod, datamodule=dm)