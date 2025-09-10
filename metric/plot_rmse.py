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

dir_eulerian = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_product_evaluation/DC_product_evaluation/eulerian_rms/'

def plot_rmse_score_0m(xp_name):

    print("depth = 0m")

    outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/Agulhas/'

    list_dict = [{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_cmems_015_004_00/Eulerian_RMS_015_004.pyo','name':'GlobCurrent Total'}, 
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_woc-l4-cureul0m-glob-1h_00/Eulerian_RMS_woc-l4-cureul0m-glob-1h.pyo','name':'WOC inertial global 00m 1h'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_unet_duacs_0m_00/Eulerian_RMS_unet_duacs_0m.pyo','name':'unet duacs 00m'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_unet_neurost_0m_00/Eulerian_RMS_unet_neurost_0m.pyo','name':'unet neurost 00m'},
                ] 

    list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Agulhas result")
    display(utils.DictTable(list_dict))

    outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/GulfStream/'

    list_dict = [{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_cmems_015_004_00/Eulerian_RMS_015_004.pyo','name':'GlobCurrent Total'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_woc-l4-cur-natl3d_rep-1d_00/Eulerian_RMS_woc-l4-cur-natl3d_rep-1d.pyo','name':'WOC-Omega3D'}, 
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_woc-l4-cureul0m-glob-1h_00/Eulerian_RMS_woc-l4-cureul0m-glob-1h.pyo','name':'WOC inertial global 00m'}] 

    list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Gulfstream result")
    display(utils.DictTable(list_dict))
    
def plot_rmse_score_15m(list_xp_name):

    print("depth = 15m")

    
    list_dict = [#{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_008_047_15/Eulerian_RMS_008_047.pyo','name':'GlobCurrent Geostrophic'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_cmems_015_004_15/Eulerian_RMS_015_004.pyo','name':'GlobCurrent Total'},
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_woc-l4-cureul15m-glob-1h_15/Eulerian_RMS_woc-l4-cureul15m-glob-1h.pyo','name':'WOC inertial global 15m 1h'},
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_woc-l4-curgeo-bfn-3h_15/Eulerian_RMS_woc-l4-curgeo-bfn-3h.pyo','name':'WOC BFN-QG 3h'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_neurost_15/Eulerian_RMS_neurost.pyo','name':'NeurOST'}]
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_unet_duacs_15m_15/Eulerian_RMS_unet_duacs_15m.pyo','name':'Unet duacs 15m'},
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_T1_unet_neurost_15m_15/Eulerian_RMS_unet_neurost_15m.pyo','name':'unet neurost 15m'}] 

    #list_dict = [element for element in list_dict if "RMS_neurost" in element or "015_004" in element]

    for xp_name in list_xp_name:
        outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/Agulhas/'
        list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Agulhas result")
    display(utils.DictTable(list_dict))
    

    list_dict = [#{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_008_047_15/Eulerian_RMS_008_047.pyo','name':'GlobCurrent Geostrophic'},
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_cmems_015_004_15/Eulerian_RMS_015_004.pyo','name':'GlobCurrent Total'}, 
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_woc-l4-cur-natl2d_rep-1d_15/Eulerian_RMS_woc-l4-cur-natl2d_rep-1d.pyo','name':'WOC SST-SSH'}, 
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_woc-l4-cureul15m-glob-1h_15/Eulerian_RMS_woc-l4-cureul15m-glob-1h.pyo','name':'WOC inertial global 15m'}, 
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_woc-l4-cur-natl3d_rep-1d_15/Eulerian_RMS_woc-l4-cur-natl3d_rep-1d.pyo','name':'WOC Omega-3D'}, 
                {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_neurost_15/Eulerian_RMS_neurost.pyo','name':'NeurOST'}]
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_unet_duacs_15/Eulerian_RMS_unet_duacs_15m.pyo','name':'Unet duacs'},
                #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_GulfStream_unet_neurost_15/Eulerian_RMS_unet_neurost_15m.pyo','name':'Unet neurost'}] 
    
    #list_dict = [element for element in list_dict if "RMS_neurost" in element or "015_004" in element]


    for xp_name in list_xp_name:
        outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/GulfStream/'
        list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Gulfstream result")
    display(utils.DictTable(list_dict))

    list_dict = [#{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_Mediterranean_008_047_15/Eulerian_RMS_008_047.pyo','name':'GlobCurrent Geostrophic'}, 
             #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_Mediterranean_woc-l4-cureul-glob-1h_15/Eulerian_RMS_woc-l4-cureul-glob-1h.pyo','name':'WOC inertial global 15m'},
             #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_Mediterranean_woc-l4-dadr-med-1d_15/Eulerian_RMS_woc-l4-dadr-med-1d.pyo','name':'WOC dADR-SR'},
             {'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_Mediterranean_neurost_15/Eulerian_RMS_neurost.pyo','name':'NeurOST'}]
             #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_Mediterranean_unet/Eulerian_RMS_unet_duacs_15m.pyo','name':'Unet duacs'},
             #{'type_stat':'Mean','path':dir_eulerian+'eulerian_rms_Mediterranean_unet/Eulerian_RMS_unet_neurost_15m.pyo','name':'Unet neurost'}] 
    

    #list_dict = [element for element in list_dict if "RMS_neurost" in element or "015_004" in element]

    for xp_name in list_xp_name:
        outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/Mediterranean/'
        list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 

    print("Mediterranean result")
    display(utils.DictTable(list_dict))