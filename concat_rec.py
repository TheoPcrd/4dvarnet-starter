import xarray as xr
import numpy as np
import sys
import hydra

with hydra.initialize('config', version_base='1.3'):
    cfg = hydra.compose("main", overrides=[
        'xp=ose_pipeline_2019_global_4th_1patch_L4_generic'])

path_file=cfg.xp_name

print(path_file)

tstart_1='2019-01-01'
tend_1= '2019-06-30'

tstart_2='2019-07-01'
tend_2='2019-12-31'

result_filepath = f"rec/{path_file}/2019_global_4/test_data_dim0.nc"
res_uo_1 = xr.open_dataset(result_filepath)
res_uo_1 = res_uo_1.sel(time=slice(tstart_1, tend_1))

result_filepath = f"rec/{path_file}/2019_global_4_2/test_data_dim0.nc"
res_uo_2 = xr.open_dataset(result_filepath)
res_uo_2 = res_uo_2.sel(time=slice(tstart_2, tend_2))

res_uo = xr.concat([res_uo_1, res_uo_2], dim='time')
res_uo = res_uo.rename({'out': 'ugos'})

result_filepath = f"rec/{path_file}/2019_global_4/test_data_dim1.nc"
res_vo_1 = xr.open_dataset(result_filepath)
res_vo_1 = res_vo_1.sel(time=slice(tstart_1, tend_1))

result_filepath = f"rec/{path_file}/2019_global_4_2/test_data_dim1.nc"
res_vo_2 = xr.open_dataset(result_filepath)
res_vo_2 = res_vo_2.sel(time=slice(tstart_2, tend_2))

res_vo = xr.concat([res_vo_1, res_vo_2], dim='time')
res_vo = res_vo.rename({'out': 'vgos'})
ds_maps = xr.merge([res_uo, res_vo])
ds_maps.to_netcdf(f"rec/{path_file}/test_data.nc")





import os 
import shutil
# Vérifie si le fichier test_data.nc existe dans le dossier courant
if os.path.isfile(f"rec/{path_file}/test_data.nc"):
    # Vérifie si le dossier 2019_global_4 existe et le supprime
    if os.path.isdir(f"rec/{path_file}/2019_global_4"):
        shutil.rmtree(f"rec/{path_file}/2019_global_4")
        print("Le dossier 2019_global_4 a été supprimé.")
    else:
        print("Le dossier 2019_global_4 n'existe pas.")

    # Vérifie si le dossier 2019_global_4_2 existe et le supprime
    if os.path.isdir(f"rec/{path_file}/2019_global_4_2"):
        shutil.rmtree(f"rec/{path_file}/2019_global_4_2")
        print("Le dossier 2019_global_4_2 a été supprimé.")
    else:
        print("Le dossier 2019_global_4_2 n'existe pas.")
else:
    print("Le fichier test_data.nc n'existe pas.")
