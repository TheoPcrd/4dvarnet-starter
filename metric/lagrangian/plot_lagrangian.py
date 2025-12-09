date_target = "2019-03-24" 

import velocity_metrics.lagrangian.drifters as drifters
import velocity_metrics.lagrangian.cumulative_distance as sde
import velocity_metrics.utils.constant as const  
import os
import warnings
import sys
import datetime
warnings.filterwarnings("ignore")
#sys.path.append('/Odyssey/private/t22picar/2024_DC_WOC-ESA/')
import json

import netCDF4
import numpy
import matplotlib
# import cartopy
import glob
import os
import sys
import datetime
from matplotlib import pyplot
import pickle
import gzip
from tqdm import tqdm
from typing import Optional, Tuple
import logging
logger = logging.getLogger(__name__)
import matplotlib.pyplot
import cartopy.crs as ccrs
import xarray

#lon_max=-43
#lon_min=-80
#lat_max=46.5 
#lat_min=25

def dist(lon1: numpy.ndarray, lat1: numpy.ndarray, lon2: numpy.ndarray,
         lat2: numpy.ndarray) -> numpy.ndarray:
    coslat = numpy.cos(numpy.deg2rad(lat1))
    dist = numpy.sqrt(((lon1 - lon2) * coslat)**2 + (lat1 - lat2)**2)
    return dist

def compute_nlcs(lon_d: numpy.ndarray, lat_d: numpy.ndarray,
                 time_d: numpy.ndarray, lon_f: numpy.ndarray,
                 lat_f: numpy.ndarray, time_f: numpy.ndarray) -> numpy.ndarray:
    # Compute Normalized Lagrangian Cumulative Separation
    lon_d_interp = numpy.interp(time_f, time_d, lon_d)
    lat_d_interp = numpy.interp(time_f, time_d, lat_d)

    dde = numpy.zeros(numpy.shape(lon_f))
    sde = numpy.zeros(numpy.shape(lon_f))

    #print(numpy.shape(lon_f))
    """
    # Distance between points in drifter
    lld = dist(lon_d_interp[1:], lat_d_interp[1:], lon_d_interp[:-1],
               lat_d_interp[:-1])

    len_time, len_pa = numpy.shape(lon_f)
    first_time = 2
    for pa in range(len_pa):
        # separation between drifter and fictive particule
        dde[:, pa] = dist(lon_d_interp[:], lat_d_interp[:], lon_f[:, pa],
                          lat_f[:, pa])
        for it in range(first_time, len_time-1):
            # Normalized cumulative separation
            #sde[it, pa] = sum(dde[2: it, pa]) / sum(lld[1: 
            # Normalized cumulative separation
            dde_sum = 0
            lld_sum = 0
            for i in range(first_time, it+1):
                dde_sum +=  dde[i-1, pa]
                lld_sum += sum(lld[first_time:i])
            #lld_sum += lld[it + i + 1]
            sde[it, pa] = dde_sum / lld_sum if lld_sum != 0 else numpy.nan
#            sde[it, pa] = sum(dde[2: it+1, pa]) / sum(lld[1: it+1])
            #if lld[it] < 5.e-6:
            #    sde[it, pa] = numpy.nan
     """
    return sde, dde, lon_d_interp, lat_d_interp

def read_fictive_traj_netcdf(ifile: str, nstep: Optional[int] = 250):
    data = netCDF4.Dataset(ifile, 'r')
    dic_attr = {'ide': data.ide, 'data_type': data.data_type,
                'label': data.label, 'depth': data.depth}
    lon = data.variables['lon_hr'][:nstep, :]
    # try:
    lat = data.variables['lat_hr'][:nstep, :]
    mask = data.variables['mask_hr'][:nstep, :]
    _mask = ((abs(lon) > 360) | (abs(lat) > 90) | (mask == 1))
    lon[_mask] = numpy.nan
    lat[_mask] = numpy.nan
    time = data.variables['time_hr'][:nstep]
    data.close()
    
    return lon, lat, time, dic_attr

def read_fictive_traj_pickle(data: dict, nstep: Optional[int] = 250):
    dic_attr = {'ide': data['ide'], 'data_type': data['data_type'],
                'label': data['label'], 'depth': data['depth'],
                'first_date': data['first_date']}
    lon = data['lon_hr'][:nstep, :]
    # try:
    lat = data['lat_hr'][:nstep, :]
    mask = data['mask_hr'][:nstep, :]
    _mask = ((abs(lon) > 360) | (abs(lat) > 90) | (mask == 1))
    lon[_mask] = numpy.nan
    lat[_mask] = numpy.nan
    time = data['time_hr'][:nstep]
    return lon, lat, time, dic_attr


def get_fictive_traj(ifile: str, dic_all: dict, dic_drif, isplot: Optional[bool] = True,
                    projection: Optional[str] = None) -> dict:
    
    #print("read_fictive_traj_pickle")
    _fname_out = ifile
    res = read_fictive_traj_pickle(dic_all[ifile])
    hrlon, hrlat, hrtime, dic_attr = res
    hrlon = numpy.mod(hrlon + 180, 360) - 180

    if dic_attr['ide'] not in dic_drif:
        print('No ide in dic drif')
        return
    
    #logging.debug(f'Read drifter data {drifter_pyo}')
    _lon = numpy.mod(numpy.array(dic_drif[dic_attr['ide']]['lon']) + 180,
                        360) - 180
    _lat = dic_drif[dic_attr['ide']]['lat']
    _time = numpy.array(dic_drif[dic_attr['ide']]['time'])
    first_day = datetime.datetime.timestamp(dic_attr['first_date'])
    # ddays = [(x - first_day).total_seconds() / 86400 for x in _time]
    ddays = [(x - first_day) / 86400 for x in _time]


    if hrtime[-1] > ddays[-1]:
        print("Pb with hrtime" )
        #return 

    #print("compute_nlcs")
    sde, dde, _lon_interp, _lat_interp = compute_nlcs(_lon, _lat, ddays,
                                                        hrlon, hrlat, hrtime)
    
    return hrlon, hrlat, hrtime, dic_attr,_lon_interp,_lat_interp

def get_list_advection(date_target,fictive_traj):
    if os.path.isdir(fictive_traj):
        input_netcdf = True
        list_advection = glob.glob(os.path.join(fictive_traj, '*nc'))
    else:
        try:
            if 'gz' in os.path.splitext(fictive_traj)[-1]:
                with gzip.open(fictive_traj, 'rb') as f:
                    dic_all = pickle.load(f)
            else:
                with open(fictive_traj, 'rb') as f:
                    dic_all = pickle.load(f)
        except pickle.UnpicklingError:
            logger.error(f'{fictive_traj} should be a pickle object')
            sys.exit(1)
        input_netcdf = False

        # Filtrer les entrées
        filtered_items = {
            key: value
            for key, value in dic_all.items()
            if value.get('first_date').strftime("%Y-%m-%d")  == date_target
        }
        #print()
        list_advection = list(filtered_items.keys())
        nb_drifter = len(list_advection)
        print(f"number of drifter : {nb_drifter}")
        return list_advection,dic_all

def get_sst_L4_8th(date_target,box):
    lon_min, lon_max, lat_min, lat_max = box
    date_target = datetime.datetime.strptime(date_target, "%Y-%m-%d") + datetime.timedelta(days=5)
    result_filepath = "/Odyssey/private/t22picar/data/sst_L4/SST_L4_OSTIA_2010-01-01-2022-01-01_8th.nc"
    map = xarray.open_dataset(result_filepath).sel(time=date_target)["thetao"].sel(lon=slice(lon_min,lon_max)).sel(lat=slice(lat_min,lat_max))
    return map

def get_sst_L4_8th_log(date_target):
    date_target = datetime.datetime.strptime(date_target, "%Y-%m-%d") + datetime.timedelta(days=5)
    result_filepath = "/Odyssey/private/t22picar/data/sst_L4/SST_L4_OSTIA_2010-01-01-2022-01-01_8th.nc"
    map = xarray.open_dataset(result_filepath).sel(time=date_target)["thetao"].sel(lon=slice(lon_min,lon_max)).sel(lat=slice(lat_min,lat_max))
    du_dx = (numpy.abs(map.differentiate("lon")))
    du_dy = (numpy.abs(map.differentiate("lat")))
    grad = numpy.log(du_dx + du_dy)
    map.values = grad
    return map

def get_sst_L4_4th(date_target):
    date_target = datetime.datetime.strptime(date_target, "%Y-%m-%d") + datetime.timedelta(days=5)
    result_filepath = "/Odyssey/private/t22picar/data/sst_L4/SST_L4_OSTIA_2019_4th.nc"
    map = xarray.open_dataset(result_filepath).sel(time=date_target)["thetao"].sel(lon=slice(lon_min,lon_max)).sel(lat=slice(lat_min,lat_max))
    return map

def get_sst_L4_4th_log(date_target):
    date_target = datetime.datetime.strptime(date_target, "%Y-%m-%d") + datetime.timedelta(days=5)
    result_filepath = "/Odyssey/private/t22picar/data/sst_L4/SST_L4_OSTIA_2019_4th.nc"
    map = xarray.open_dataset(result_filepath).sel(time=date_target)["thetao"].sel(lon=slice(lon_min,lon_max)).sel(lat=slice(lat_min,lat_max))
    du_dx = (numpy.abs(map.differentiate("lon")))
    du_dy = (numpy.abs(map.differentiate("lat")))
    grad = numpy.log(du_dx + du_dy)
    map.values = grad
    return map

import xarray
def get_sst_L3_8th(date_target):
    date_target = datetime.datetime.strptime(date_target, "%Y-%m-%d") + datetime.timedelta(days=5)
    result_filepath = "/Odyssey/private/t22picar/data/sst_L3/SST_L3_2010-01-01-2020-01-01_8th.nc"
    map = xarray.open_dataset(result_filepath).sel(time=date_target)["thetao"].sel(lon=slice(lon_min,lon_max)).sel(lat=slice(lat_min,lat_max))
    return map

import xarray
def get_sst_L3(date_target):
    date_target = datetime.datetime.strptime(date_target, "%Y-%m-%d") + datetime.timedelta(days=5)
    result_filepath = "/Odyssey/private/t22picar/data/sst_L3/SST_L3_2010-01-01-2020-01-01.nc"
    map = xarray.open_dataset(result_filepath).sel(time=date_target)["adjusted_sea_surface_temperature"].sel(lon=slice(lon_min,lon_max)).sel(lat=slice(lat_min,lat_max))
    map=map.rename({"longitude": "lon" })
    map=map.rename({"latitude": "lat"})
    return map

def get_sst_MW(date_target):
    date_target = datetime.datetime.strptime(date_target, "%Y-%m-%d") + datetime.timedelta(days=5)
    result_filepath = "/Odyssey/private/t22picar/data/sst_L4/SST_MW_2010_2020_4th.nc"
    map = xarray.open_dataset(result_filepath).sel(time=date_target)["analysed_sst"].sel(lon=slice(10,30)).sel(lon=slice(lon_min,lon_max)).sel(lat=slice(lat_min,lat_max))
    return map


def plot_lagrangian_traj(date_target,fictive_traj,fictive_traj_neurost,dic_drif,box):
    lon_min, lon_max, lat_min, lat_max = box
    alpha=0.2
    map_back = get_sst_L4_8th(date_target,box)
    list_advection, dic_all = get_list_advection(date_target,fictive_traj)
    list_advection_neurost, dic_all_neurost = get_list_advection(date_target,fictive_traj_neurost)

    figure = pyplot.figure(figsize=(12, 12))
    proj=ccrs.PlateCarree()

    for advection,advection_neurost in zip(list_advection,list_advection_neurost):
        
        #print(advection)

        lon_f_n, lat_f_n, hrtime_n, dic_attr_n,lon_d,lat_d = get_fictive_traj(advection_neurost,dic_all_neurost,dic_drif)

        lon_f, lat_f, hrtime, dic_attr,lon_d,lat_d = get_fictive_traj(advection,dic_all,dic_drif)
        
        #print(hrtime)
        
        proj=ccrs.PlateCarree()
        
        ax0 = pyplot.subplot(111, projection=proj)


        extent = (numpy.nanmin(lon_f)-1, numpy.nanmax(lon_f)+1,
                    numpy.nanmin(lat_f)-1, numpy.nanmax(lat_f)+1)
        
        ax0.gridlines(crs=proj, draw_labels=True, color='gray', linestyle='--',
                        alpha=0.5)
        for pa in range(0, numpy.shape(lon_f)[1], 1):
            ax0.plot(lon_f[:, pa], lat_f[:, pa], 'b', transform=proj,alpha=alpha,zorder=5)

        for pa in range(0, numpy.shape(lon_f_n)[1], 1):
            ax0.plot(lon_f_n[:, pa], lat_f_n[:, pa], 'g', transform=proj,alpha=alpha,zorder=5)

        ax0.plot(lon_d, lat_d, '-k', transform=proj,alpha=1,zorder=10)
        ax0.scatter(lon_d[0],lat_d[0], transform=proj,alpha=1,c='k',s=20,marker='o',zorder=10)
        ax0.scatter(lon_d[-1],lat_d[-1], transform=proj,alpha=1,c='k',s=20,marker='^',zorder=10)
    
    sst_cm = ax0.pcolormesh(map_back.lon,map_back.lat,map_back,cmap=matplotlib.pyplot.cm.RdBu_r)

    ax0.plot(lon_f[:, 0], lat_f[:, 0], 'b', transform=proj,alpha=1,label=dic_attr["data_type"])
    ax0.plot(lon_f_n[:, 0], lat_f_n[:, 0], 'g', transform=proj,alpha=1,label=dic_attr_n["data_type"])
    ax0.plot(lon_d, lat_d, '-k', transform=proj,alpha=1,label="Drifter")

    ax0.set_ylim(lat_min,lat_max)
    ax0.set_xlim(lon_min,lon_max)

    ax0.legend()
    ax0.set_title(f"First date advection : {date_target}")

    cbar = matplotlib.pyplot.colorbar(sst_cm, ax=ax0, orientation='vertical', pad=0.08,shrink=0.35)
    cbar.set_label("SST day+5 (K)")

def get_sde(ifile: str, dic_all: dict, dic_drif, isplot: Optional[bool] = True,
                    projection: Optional[str] = None) -> dict:
    
    #print("read_fictive_traj_pickle")
    _fname_out = ifile
    res = read_fictive_traj_pickle(dic_all[ifile])
    hrlon, hrlat, hrtime, dic_attr = res
    hrlon = numpy.mod(hrlon + 180, 360) - 180

    if dic_attr['ide'] not in dic_drif:
        print('No ide in dic drif')
        return
    
    #logging.debug(f'Read drifter data {drifter_pyo}')
    _lon = numpy.mod(numpy.array(dic_drif[dic_attr['ide']]['lon']) + 180,
                        360) - 180
    _lat = dic_drif[dic_attr['ide']]['lat']
    _time = numpy.array(dic_drif[dic_attr['ide']]['time'])
    first_day = datetime.datetime.timestamp(dic_attr['first_date'])
    # ddays = [(x - first_day).total_seconds() / 86400 for x in _time]
    ddays = [(x - first_day) / 86400 for x in _time]


    if hrtime[-1] > ddays[-1]:
        print("Pb with hrtime" )
        #return 

    #print("compute_nlcs")
    sde, dde, _lon_interp, _lat_interp = compute_nlcs_sde(_lon, _lat, ddays,
                                                        hrlon, hrlat, hrtime)
    
    return sde, dde

def compute_nlcs_sde(lon_d: numpy.ndarray, lat_d: numpy.ndarray,
                 time_d: numpy.ndarray, lon_f: numpy.ndarray,
                 lat_f: numpy.ndarray, time_f: numpy.ndarray) -> numpy.ndarray:
    # Compute Normalized Lagrangian Cumulative Separation
    lon_d_interp = numpy.interp(time_f, time_d, lon_d)
    lat_d_interp = numpy.interp(time_f, time_d, lat_d)

    dde = numpy.zeros(numpy.shape(lon_f))
    sde = numpy.zeros(numpy.shape(lon_f))

    #print(numpy.shape(lon_f))

    # Distance between points in drifter
    lld = dist(lon_d_interp[1:], lat_d_interp[1:], lon_d_interp[:-1],
               lat_d_interp[:-1])

    len_time, len_pa = numpy.shape(lon_f)
    first_time = 2
    for pa in range(len_pa):
        # separation between drifter and fictive particule
        dde[:, pa] = dist(lon_d_interp[:], lat_d_interp[:], lon_f[:, pa],
                          lat_f[:, pa])
        for it in range(first_time, len_time-1):
            # Normalized cumulative separation
            #sde[it, pa] = sum(dde[2: it, pa]) / sum(lld[1: 
            # Normalized cumulative separation
            dde_sum = 0
            lld_sum = 0
            for i in range(first_time, it+1):
                dde_sum +=  dde[i-1, pa]
                lld_sum += sum(lld[first_time:i])
            #lld_sum += lld[it + i + 1]
            sde[it, pa] = dde_sum / lld_sum if lld_sum != 0 else numpy.nan
#            sde[it, pa] = sum(dde[2: it+1, pa]) / sum(lld[1: it+1])
            #if lld[it] < 5.e-6:
            #    sde[it, pa] = numpy.nan

    return sde, lld_sum, lon_d_interp, lat_d_interp