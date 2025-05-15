import warnings
warnings.filterwarnings("ignore")
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
import cfgrib

folder_data = "/Odyssey/private/t22picar/data/era5/"
file_glorys = "era5_2019-2021_hourly.grib" # Actually not glorys 

maps_glorys = xr.open_dataset(folder_data+file_glorys, engine="cfgrib")
maps_glorys['longitude'] = xr.where(maps_glorys['longitude'] > 180, maps_glorys['longitude'] - 360, maps_glorys['longitude'])
lat_simu = maps_glorys.latitude.values
lon_simu = maps_glorys.longitude.values
#lon_simu = maps_glorys.longitude.values - 180 
#maps_glorys.longitude[maps_glorys.longitude>180].values = maps_glorys.longitude[maps_glorys.longitude>180].values - 360 # longitude wtf


folder_data_4th = "/Odyssey/private/t22picar/data/glorys_15m/"
file_glorys_4th = "glorys_15.81m_2019-01-01-2020-01-01_4th.nc"
maps_4th = xr.open_dataset(folder_data_4th+file_glorys_4th)
lat_ref = maps_4th.lat
lon_ref = maps_4th.lon

maps_glorys = maps_glorys.rename({"latitude": "lat"})
maps_glorys = maps_glorys.rename({"longitude": "lon"})

# Original grid 1/12 (2041,4320) --> 1/4
new_sizes = [size // 3 for size in (2041, 4320)]
print('new sizes: {}'.format(new_sizes))

def regrid_da(regrid_sizes, da: xr.DataArray):

        lat_space = np.linspace(start=lat_ref.min(), stop=lat_ref.max(), num=regrid_sizes[0])
        lon_space = np.linspace(start=lon_ref.min(), stop=lon_ref.max(), num=regrid_sizes[1])

        new_da = da.interp({"lat":lat_space, "lon":lon_space}, method="linear")

        return new_da

# Daily mean wind
maps_glorys = maps_glorys.resample(valid_time='1D').mean()

# Interpolation new grid
maps_glorys = regrid_da(new_sizes,maps_glorys)

#Split into two files
maps_glorys = maps_glorys.drop("number").drop("step").drop("surface").rename({"valid_time": "time"})
tstart = "20-01-2020"
tend= "20-04-2021"
maps_glorys_train = maps_glorys.sel(time=slice(tstart,tend))

# save data 
save_file="era5_2020_2021_dailymean_4th.nc"
# Sauvegarder le DataArray en fichier NetCDF
maps_glorys_train.to_netcdf(folder_data+save_file)

tstart = "01-01-2019"
tend= "01-01-2020"
maps_glorys_test = maps_glorys.sel(time=slice(tstart,tend))

# save data 
save_file="era5_2019_dailymean_4th.nc"
# Sauvegarder le DataArray en fichier NetCDF
maps_glorys_test.to_netcdf(folder_data+save_file)