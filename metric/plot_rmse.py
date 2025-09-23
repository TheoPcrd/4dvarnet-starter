import velocity_metrics.utils.constant as const 
import velocity_metrics.eulerian.eulerian_drifters as eulerian  
import datetime
import sys   
from IPython.display import display, Markdown
import matplotlib.pyplot as plt
import cartopy 
import warnings 
warnings.filterwarnings("ignore") 
sys.path.append('/Odyssey/private/t22picar/2024_DC_WOC-ESA/')
from src import utils
import utils_nb

dir_eulerian = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_product_evaluation/DC_product_evaluation/eulerian_rms/'
base_outputdir = "../"

def plot_rmse_score_0m(xp_name):

    print("depth = 0m")

    outputdir = f'{base_outputdir}rec/{xp_name}/metric/GulfStream/'

    list_dict = [{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_cmems_015_004_00/Eulerian_RMS_015_004.pyo','name':'GlobCurrent Total'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_woc-l4-cur-natl3d_rep-1d_00/Eulerian_RMS_woc-l4-cur-natl3d_rep-1d.pyo','name':'WOC-Omega3D'}, 
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_woc-l4-cureul0m-glob-1h_00/Eulerian_RMS_woc-l4-cureul0m-glob-1h.pyo','name':'WOC inertial global 00m'}] 

    list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Gulfstream result")
    display(utils.DictTable(list_dict))
    
def plot_rmse_score_15m(list_xp_name,keys=None):

    print("depth = 15m")
    
    list_dict = [{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_cmems_015_004_15/Eulerian_RMS_015_004.pyo','name':'GlobCurrent Total'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_neurost_15/Eulerian_RMS_neurost.pyo','name':'NeurOST'}]


    for xp_name in list_xp_name:
        outputdir = f'{base_outputdir}rec/{xp_name}/metric/Agulhas/'
        list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Agulhas result")

    if keys:
        display(utils.DictTable(list_dict,keys=keys))
    else:
        display(utils.DictTable(list_dict))

    print("depth = 15m")

    list_dict = [{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_cmems_015_004_15/Eulerian_RMS_015_004.pyo','name':'GlobCurrent Total'}, 
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_neurost_15/Eulerian_RMS_neurost.pyo','name':'NeurOST'}]
    
    for xp_name in list_xp_name:
        outputdir = f'{base_outputdir}rec/{xp_name}/metric/GulfStream/'
        list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Gulfstream result")
    if keys:
        display(utils.DictTable(list_dict,keys=keys))
    else:
        display(utils.DictTable(list_dict))


    list_dict = [
             {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_Mediterranean_neurost_15/Eulerian_RMS_neurost.pyo','name':'NeurOST'}]

    for xp_name in list_xp_name:
        outputdir = f'{base_outputdir}/rec/{xp_name}/metric/Mediterranean/'
        list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Mediterranean result")
    if keys:
        display(utils.DictTable(list_dict,keys=keys))
    else:
        display(utils.DictTable(list_dict))