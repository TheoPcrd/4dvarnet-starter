import xarray as xr
import numpy as np
import sys
import hydra
from typing import Optional
import datetime
#Select day per day 


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


# Définir la date de début et la date de fin
start_date = datetime.datetime(2019, 1, 1)
end_date = datetime.datetime(2019, 12, 31)

# Récupération du xp_name 
path_file = sys.argv[1]
print(path_file)

result_filepath = f"outputs/saved/{path_file}/{path_file}/test_data_dim0.nc"
res_uo = xr.open_dataset(result_filepath).sel(time=slice(start_date,end_date))
res_uo = res_uo.rename({'out': 'ugos'})

result_filepath = f"outputs/saved/{path_file}/{path_file}/test_data_dim1.nc"
res_vo = xr.open_dataset(result_filepath).sel(time=slice(start_date,end_date))
res_vo = res_vo.rename({'out': 'vgos'})

ds_maps = xr.merge([res_uo, res_vo])

lat_ref=ds_maps.lat.values
lon_ref=ds_maps.lon.values

print(f"Domaine = [{lat_ref[0]},{lat_ref[-1]},{lon_ref[0]},{lon_ref[-1]}]")
 ### FILTER ####

if "finescale" in path_file or "8th" in path_file: 
    file_grid = "/Odyssey/private/t22picar/data/ssh_L4/SSH_L4_CMEMS_2010-01-01-2024-01-01.nc"
    file_grid = xr.open_dataset(file_grid).isel(time=0).sel(latitude=slice(lat_ref[0],lat_ref[-1])).sel(longitude=slice(lon_ref[0],lon_ref[-1]))
    mask = np.where(np.isnan(file_grid.adt),False,True)
    mask = mask[np.newaxis,:,:]
    mask = mask.repeat(365,axis=0)
    ds_maps = ds_maps.where(mask, np.nan)    

else : 

    file_grid = "/Odyssey/private/t22picar/data/ssh_L4/SSH_L4_CMEMS_2010-01-01-2024-01-01_4th.nc"
    file_grid = xr.open_dataset(file_grid).isel(time=0).sel(lat=slice(lat_ref[0],lat_ref[-1])).sel(lon=slice(lon_ref[0],lon_ref[-1]))
    mask = np.where(np.isnan(file_grid.zos),False,True)
    mask = mask[np.newaxis,:,:]
    mask = mask.repeat(365,axis=0)
    ds_maps = ds_maps.where(mask, np.nan)

import os
# Chemin du dossier que vous souhaitez créer
dossier_path_daily = f'./rec/{path_file}/daily'
# Créer le dossier
os.makedirs(dossier_path_daily, exist_ok=True)


### SAVING ####
# Récupérer la liste des variables sans les dimensions
variables = [var for var in ds_maps.variables if var not in ds_maps.dims]
ds_maps,encoding = save(ds_maps,variables,dossier_path_daily)


from datetime import datetime, timedelta

# Boucle sur chaque jour de la période
current_date = start_date
while current_date <= end_date:
    #print(current_date.strftime('%Y-%m-%d'))  # Affiche la date au format AAAA-MM-JJ
    ds_map_day=ds_maps.sel(time=current_date)
    folder_out = dossier_path_daily+f"/unet_rec_{current_date.strftime('%Y-%m-%d')}.nc"
    ds_map_day.to_netcdf(folder_out, 'w', format="NETCDF4", encoding=encoding)
    current_date += timedelta(days=1)  # Passe au jour suivant

### Creation du fichier .json

import json

base_output="/Odyssey/private/t22picar/multivar_drifter/"
path_files=f'{base_output}rec/{path_file}/daily/'

# Chemin vers le fichier JSON
file_path = f'{base_output}metric/dictionary/'
file_name = 'data_type_metric_generic.json'

# Lire le fichier JSON
with open(file_path+file_name, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Exemple de modification : ajouter une nouvelle clé-valeur
data['data_type'] = path_file
data['label'] = path_file
data['path'] = path_files

# Afficher les données actuelles
print("Données actuelles :")
print(json.dumps(data, indent=4, ensure_ascii=False))

file_name_update = f'{path_file}.json'
# Écrire les modifications dans le fichier JSON
with open(file_path+file_name_update, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"\nLe fichier {file_name_update} a été créé.")