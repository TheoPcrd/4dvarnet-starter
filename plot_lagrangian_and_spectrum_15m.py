import pickle
import glob
import os
import re
import sys   
sys.path.append("/Odyssey/private/t22picar/multivar_uv/metric")
import utils_nb
from matplotlib import pyplot
from typing import Tuple, Optional
import velocity_metrics.spectrum.spectrum as spectrum
import velocity_metrics.lagrangian.cumulative_distance as sde
import matplotlib.pyplot as plt 


xp_name = sys.argv[1]
print(xp_name)

WORKDIR = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_product_evaluation/DC_product_evaluation/'
# Global Variables
idir = os.path.join(WORKDIR, 'spectrum')
region_list = ["Agulhas","GulfStream","Mediterranean"]

def plot_spectrum_15m(list_xp_name,savefig):

    depth = '1.pyo'
    list_color=['r', 'b', 'c', 'm', 'g', 'y']

    for region in region_list:
        #print(region)
        idir = os.path.join(WORKDIR, 'spectrum')
        if region=="Agulhas":
            listdir = utils_nb.make_list_spectrum(idir, "T1", depth)
        elif region=="Mediterranean":
                list_color=['b', 'c', 'm', 'g', 'y']
                listdir = utils_nb.make_list_spectrum(idir, region, depth)
        else: 
            listdir = utils_nb.make_list_spectrum(idir, region, depth)
        listdir=listdir[:-2]
        # Filtrer les éléments
        listdir = [element for element in listdir if "neurost_region" in element or "015_004" in element]

        print(listdir)
        for xp_name in list_xp_name:
            listdir = listdir + [f"/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/{region}/spectrum_{xp_name}_region_{region}_{depth}"]

        for idir in listdir:
            if '.png' in idir:
                listdir.remove(idir)

        path=f"/Odyssey/private/t22picar/multivar_uv/rec/{savefig}/metric/{region}/plot_score/"
        if not os.path.exists(path):
            os.makedirs(path)
        path_save = path+f"spectrum_depth=15m.png"

        fig = spectrum.plot(listdir, outfile=path_save, list_color=list_color)
        plt.title(f"{region} at 15m")


def plot_lagrangian_15m(list_xp_name,savefig=None):

    for region in region_list:
        # Global Variables
        idir = os.path.join(WORKDIR, 'cumulative_distance')
        depth = '15'
        listdir = []
        list_color=['r', 'b', 'c', 'm', 'g', 'y','k',"b"]

        if region=="Agulhas":
            listdir = utils_nb.make_list_sde(idir, "T1", depth)
            #listdir=[listdir[2],listdir[4]]
        elif region == "Mediterranean": 
            listdir = utils_nb.make_list_sde(idir, region, depth)
            list_color=['b', 'c', 'm', 'g', 'y','k',"b"]
            #listdir = [listdir[1]]
        else:
            listdir = utils_nb.make_list_sde(idir, region, depth)
            #listdir=[listdir[2]]
            #listdir = []
        listdir = [element for element in listdir if "neurost" in element or "015_004" in element]

        for xp_name in list_xp_name:
            listdir = listdir + [f"/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/{region}/plot/SDE_region_{region}_20190101-20191231_{xp_name}.pyo.gz"]
        _list = []
        for ifile in listdir:
            if (os.path.splitext(ifile)[-1] != '.png') and ('miost' not in ifile):
                _list.append(ifile)
        listdir = _list #print(_list)
        
        if savefig:
            path=f"/Odyssey/private/t22picar/multivar_uv/rec/{savefig}/metric/{region}/plot_score/"
            if not os.path.exists(path):
                os.makedirs(path)
            #path_save = path+f"lagrangian_score_depth={depth}m.png"
            output_filename=f"lagrangian_score_depth={depth}m.png"
            #plt.savefig(path_save)

        fig = sde.plot(_list, output_dir=path, output_filename=output_filename,
                    list_color=list_color)
        #['r', 'b', 'c', 'g', 'y', 'k', 'lime'])
        fig[0].suptitle(f'{region} at 15m')

        if savefig:
            path=f"/Odyssey/private/t22picar/multivar_uv/rec/{savefig}/metric/{region}/plot_score/"
            if not os.path.exists(path):
                os.makedirs(path)
            path_save = path+f"lagrangian_score_depth={depth}m.png"
            plt.savefig(path_save)


list_xp_name=["ssh_duacs_sst_w_to_u_v_11d_15m","duacs_geos_15m"]
list_xp_name.append(xp_name)
#list_xp_name=["neurost_sst_ssh","ssh_duacs_sst_w_to_u_v_11d_15m_ageos","duacs_geos_15m","ssh_duacs_sst_w_to_u_v_17d_15m"]

plot_lagrangian_15m(list_xp_name,savefig=xp_name)

list_xp_name=["ssh_duacs_sst_w_to_u_v_11d_15m"]
list_xp_name.append(xp_name)

plot_spectrum_15m(list_xp_name,savefig=xp_name)