
import warnings
warnings.filterwarnings("ignore")
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.ticker as mticker

folder_data = "/Odyssey/private/t22picar/data/glorys_15m/"
file_glorys = "glorys_multivar_15m_2010.nc"
maps_glorys = xr.open_dataset(folder_data+file_glorys)

folder_data_4th = "/Odyssey/public/glorys/reanalysis/"
file_glorys_4th = "glorys12_multivar_2020_4th.nc"
maps_4th = xr.open_dataset(folder_data_4th+file_glorys_4th)

# Original grid 1/12 (2041,4320) --> 1/4
new_sizes = [size // 3 for size in (2041, 4320)]
print('new sizes: {}'.format(new_sizes))

def regrid_da(regrid_sizes, da: xr.DataArray):

        lat_space = np.linspace(start=da.lat.min(), stop=da.lat.max(), num=regrid_sizes[0])
        lon_space = np.linspace(start=da.lon.min(), stop=da.lon.max(), num=regrid_sizes[1])

        new_da = da.interp({"lat":lat_space, "lon":lon_space}, method="linear")

        return new_da

maps_glorys = maps_glorys.rename({"latitude": "lat"})
maps_glorys = maps_glorys.rename({"longitude": "lon"})

maps_glorys = regrid_da(new_sizes,maps_glorys)

for year in range(2011,2019):
    print(year)
    file_glorys = f"glorys_multivar_15m_{year}.nc"
    maps_glorys_i = xr.open_dataset(folder_data+file_glorys)
    print("Interpolation ... ")
    maps_glorys_i = maps_glorys_i.rename({"latitude": "lat"})
    maps_glorys_i = maps_glorys_i.rename({"longitude": "lon"})  
    maps_glorys_i = regrid_da(new_sizes,maps_glorys_i)
    print("Interpolation done ")
    print("Concatenation ... ")
    maps_glorys = xr.concat([maps_glorys, maps_glorys_i], dim='time')
    print("Concatenation done ")

maps_glorys = maps_glorys.sel(depth=maps_glorys.depth[0])

# save data 
print("Saving...")
save_file="glorys_multivar_15m_2010-2018.nc"
print("Saving done")
# Sauvegarder le DataArray en fichier NetCDF
maps_glorys.to_netcdf(folder_data+save_file)