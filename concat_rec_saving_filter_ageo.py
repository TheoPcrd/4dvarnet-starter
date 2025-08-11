import xarray as xr
import numpy as np
import sys
import hydra
from typing import Optional
import datetime


ATTRS ={'time': {'dtype': 'int64',}, # 'units': 'days since 2019-01-01', }, 
        'lon': {'dtype': 'float32', 'valid_min': -180., 'valid_max': 180.,
                'long_name': 'longitude', 'standard_name': 'longitude',
                'units': 'degrees_east'},
        'lat': {'dtype': 'float32', 'valid_min': -90., 'valid_max': 90.,
                'long_name': 'latitude', 'standard_name': 'latitude',
                'units': 'degrees_north'},
        'ugos': {'dtype': 'float32', 'valid_min': -100., 'valid_max': 100.,
                'units': 'm/s',
                'long_name': 'Eastward total velocity',
                },
        'vgos': {'dtype': 'float32', 'valid_min': -100., 'valid_max': 100.,
                'units': 'm/s',
                'long_name': 'Northward total velocity',
                },
                }
COMPLEVEL = 4
ZLIB = True
FV32 = 1.e+20
ENC_FV = {'zlib': ZLIB, 'complevel': COMPLEVEL, '_FillValue': FV32,
          'dtype': 'float32'}
ENC = {'zlib': ZLIB, 'complevel': COMPLEVEL, 'dtype': 'float32'}


def save(ds: xr.Dataset, listkey: list, file_out: str, 
         ATTR_VARS: Optional[dict] = ATTRS, fillvalue: Optional[float] = FV32):
    encoding = {}
    for key in listkey:
        print(key)
        dic_attr = {}
        if key in ATTR_VARS.keys():
            dic_attr = ATTR_VARS[key]
        ds[key].values[np.isnan(ds[key].values)] = fillvalue
        ds = ds.assign({key: (['time', 'lat', 'lon'], ds[key].values,
                            dic_attr)})

        encoding[key] = ENC_FV
        print(ENC_FV)
    for key in ('lon', 'lat', 'time'):
    #for key in ('lon', 'lat'):
        dic_attr = {}
        if key in ATTR_VARS.keys():
            dic_attr = ATTR_VARS[key]
        ds = ds.assign({key: ([key,], ds[key].values,
                            dic_attr)})
        encoding[key] = ENC
    encoding['time']['dtype'] = 'int64'
    encoding['lat']['dtype'] = 'float32'
    encoding['lon']['dtype'] = 'float32'
    
    print(encoding)

    t0 = ds['time'].values[0] - np.timedelta64(12, 'h')
    t1 = ds['time'].values[-1] + np.timedelta64(12, 'h')

    ds.attrs['title'] = 'multivar_uv'
    ds.attrs['project'] = 'multivar_uv'
    ds.attrs['summary'] = ''
    ds.attrs['references'] = ''
    ds.attrs['institution'] = 'IMT Atlantic'
    ds.attrs['creator_name'] = 'Theo'
    ds.attrs['version_id'] = '0.1'
    ds.attrs['date_created'] = str(datetime.datetime.now())
    ds.attrs['geospatial_lat_min'] = f'{np.min(ds["lat"].values)}N'
    ds.attrs['geospatial_lat_max'] = f'{np.max(ds["lat"].values)}N'
    ds.attrs['geospatial_lon_min'] = f'{np.min(ds["lon"].values)}E'
    ds.attrs['geospatial_lon_max'] = f'{np.max(ds["lon"].values)}E'
    ds.attrs['time_coverage_start'] = np.datetime_as_string(t0, unit='s')
    ds.attrs['time_coverage_end'] = np.datetime_as_string(t1, unit='s')
    #ds.to_netcdf(file_out, 'w', format="NETCDF4", encoding=encoding)
    return ds,encoding

#with hydra.initialize('config', version_base='1.3'):
#    cfg = hydra.compose("main", overrides=[
#        'xp=ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4'])

#path_file=cfg.xp_name

path_file = sys.argv[1]
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

#ds_maps.to_netcdf(f"rec/{path_file}/test_data.nc")

### FILTER ####
mask = np.load('/Odyssey/private/t22picar/2023a_SSH_mapping_OSE/nb_diags_THEO/uv_score_mask/mask_glorys_4th.npy')
mask = mask[np.newaxis,:,:]
mask = mask.repeat(365,axis=0)
ds_maps = ds_maps.where(mask, np.nan)

from glob import glob
import xarray as xr

ds_maps_ageo = ds_maps.copy()

if "duacs" in path_file:
    print("duacs geostrophy")
    folder_data = "/Odyssey/private/t22picar/multivar_uv/rec/duacs_geos/daily/"
    #folder_data = "/Odyssey/private/t22picar/multivar_uv/rec/duacs_geos_lucile/daily/"
    list_of_maps = sorted(glob(folder_data+'/unet_rec_*.nc'))
    maps_geo = xr.open_mfdataset(list_of_maps, combine='nested', concat_dim='time')

if "neurost" in path_file:
    print("neurost geostrophy")
    folder_data = "/Odyssey/private/t22picar/data/uv/NeurOST_SST-SSH_uv_allsat-al_2019_4th.nc"
    maps_geo = xr.open_dataset(folder_data).sel(time=slice("2019-01-01","2019-12-31"))

ds_maps.ugos.values = ds_maps.ugos.values + maps_geo.ugos.values
ds_maps.vgos.values = ds_maps.vgos.values + maps_geo.vgos.values

import os
# Chemin du dossier que vous souhaitez créer
dossier_path_daily = f'./rec/{path_file}/daily'
# Créer le dossier
os.makedirs(dossier_path_daily, exist_ok=True)

### SAVING ####
# Récupérer la liste des variables sans les dimensions
variables = [var for var in ds_maps.variables if var not in ds_maps.dims]
ds_maps,encoding = save(ds_maps,variables,dossier_path_daily)

#Select day per day 
from datetime import datetime, timedelta
# Définir la date de début et la date de fin
start_date = datetime(2019, 1, 1)
end_date = datetime(2020, 1, 1)

# Boucle sur chaque jour de la période
current_date = start_date
while current_date < end_date:
    #print(current_date.strftime('%Y-%m-%d'))  # Affiche la date au format AAAA-MM-JJ
    ds_map_day=ds_maps.sel(time=current_date)
    folder_out = dossier_path_daily+f"/unet_rec_{current_date.strftime('%Y-%m-%d')}.nc"
    ds_map_day.to_netcdf(folder_out, 'w', format="NETCDF4", encoding=encoding)
    current_date += timedelta(days=1)  # Passe au jour suivant


#Chemin du dossier que vous souhaitez créer
dossier_path_daily = f'./rec/{path_file}/daily_ageos'
# Créer le dossier
os.makedirs(dossier_path_daily, exist_ok=True)

### SAVING ####
# Récupérer la liste des variables sans les dimensions
variables = [var for var in ds_maps_ageo.variables if var not in ds_maps_ageo.dims]
ds_maps_ageo,encoding = save(ds_maps_ageo,variables,dossier_path_daily)

# Boucle sur chaque jour de la période
current_date = start_date
print("ageo saving")
print(current_date)
while current_date < end_date:
    #print(current_date.strftime('%Y-%m-%d'))  # Affiche la date au format AAAA-MM-JJ
    ds_map_day=ds_maps_ageo.sel(time=current_date)
    folder_out = dossier_path_daily+f"/unet_rec_{current_date.strftime('%Y-%m-%d')}.nc"
    ds_map_day.to_netcdf(folder_out, 'w', format="NETCDF4", encoding=encoding)
    current_date += timedelta(days=1)  # Passe au jour suivant


"""
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
"""