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

# Récupération du xp_name 
xp_name = sys.argv[1]
print(xp_name)
base_output="./"
# Calcul des metrics 



if "_0m" in xp_name or "_00m" in xp_name:
    depth = 0
    depth_ind=0
    print(f"depth = {depth}")
elif "_15m" in xp_name:
    depth = 15
    depth_ind=1
    print(f"depth = {depth}")
else: 
    print("!!! no depth in xp name !!!")
    depth = 15
    depth_ind=1
# Formater depth avec deux chiffres significatifs

depth_formatted = "{:02}".format(depth)
input_dict = f'{base_output}metric/dictionary/'
input_drifter = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_data/drifter/'
outputdir = f'{base_output}rec/{xp_name}/metric'

### TO CHANGE FOR BOX SIZE ###

#path_drifter_param = input_dict + 'drifters_parameters_bsize=0.125.ini' #'drifters_parameters.ini'
#dir_output = "metric_bsize=0.125" #

dir_output = "metric"
path_drifter_param = input_dict + 'drifters_parameters.ini'

path_dict_product = input_dict+f'{xp_name}.json' 

first_date = datetime.datetime.strptime('20190101T000000Z', const.FMT)
last_date  = datetime.datetime.strptime('20191231T000000Z', const.FMT) 


input_lagrangian_position = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_data/lagrangian_position_pickle/'

region="Agulhas"
outputdir = f'{base_output}rec/{xp_name}/{dir_output}/{region}/'
path_dict_region = input_dict + f'region_{region}.json'
region="T1"
# Formater depth avec deux chiffres significatifs
#path_drifter_param = input_dict + 'drifters_parameters.ini'
path_drifter_position = input_lagrangian_position + f'Fictive_pos_Drifters_AOML_region_{region}_{depth_formatted}m_20190101T000000Z_20200101T000000Z.json' 
first_date = '20190101T000000Z'
last_date = '20191231T000000Z'
advection_days = 10

_ = drifters.run_all_load_once(path_drifter_param, path_dict_product, path_drifter_position,
                 days_of_advection=advection_days, output_dir=outputdir, region=path_dict_region, 
                 first_date=first_date, last_date=last_date, sdepth=depth_ind)

drifter_list = [input_drifter + f'Drifters_AOML_region_{region}_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']
region="Agulhas"
path_artificial_drifters = os.path.join(outputdir,f'{xp_name}_region_{region}_dep{depth_ind}.pyo.gz')
print(path_artificial_drifters)
outputfilename = f'SDE_region_{region}_20190101-20191231'
outputdir_plot=outputdir+'/plot/'

_ = sde.run(path_artificial_drifters, drifter_list, output_dir=outputdir_plot, output_filename=outputfilename,isplot=False)


region="GulfStream"
outputdir = f'{base_output}rec/{xp_name}/{dir_output}/{region}/'
# Formater depth avec deux chiffres significatifs
path_dict_region = input_dict + f'region_{region}.json'
#path_drifter_param = input_dict + 'drifters_parameters.ini'
path_drifter_position = input_lagrangian_position + f'Fictive_pos_Drifters_AOML_region_{region}_{depth_formatted}m_20190101T000000Z_20200101T000000Z.json' 
first_date = '20190101T000000Z'
last_date = '20191231T000000Z'
advection_days = 10

_ = drifters.run_all_load_once(path_drifter_param, path_dict_product, path_drifter_position,
                 days_of_advection=advection_days, output_dir=outputdir, region=path_dict_region, 
                 first_date=first_date, last_date=last_date, sdepth=depth_ind)

drifter_list = [input_drifter + f'Drifters_AOML_region_{region}_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']
path_artificial_drifters = os.path.join(outputdir, f'{xp_name}_region_{region}_dep{depth_ind}.pyo.gz')
outputfilename = f'SDE_region_{region}_20190101-20191231'
outputdir_plot=outputdir+'/plot/'
#
_ = sde.run(path_artificial_drifters, drifter_list, output_dir=outputdir_plot, output_filename=outputfilename,isplot=False)


"""
region="Mediterranean"
outputdir = f'{base_output}rec/{xp_name}/{dir_output}/{region}/'
# Formater depth avec deux chiffres significatifs
path_dict_region = input_dict + f'region_{region}.json'
#path_drifter_param = input_dict + 'drifters_parameters.ini'
path_drifter_position = input_lagrangian_position + f'Fictive_pos_Drifters_AOML_region_{region}_{depth_formatted}m_20190101T000000Z_20200101T000000Z.json' 
first_date = '20190101T000000Z'
last_date = '20191231T000000Z'
advection_days = 10

_ = drifters.run_all_load_once(path_drifter_param, path_dict_product, path_drifter_position,
                 days_of_advection=advection_days, output_dir=outputdir, region=path_dict_region, 
                 first_date=first_date, last_date=last_date, sdepth=depth_ind)

drifter_list = [input_drifter + f'Drifters_AOML_region_{region}_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']
path_artificial_drifters = os.path.join(outputdir, f'{xp_name}_region_{region}_dep{depth_ind}.pyo.gz')
outputfilename = f'SDE_region_{region}_20190101-20191231'
outputdir_plot=outputdir+'/plot/'
#
_ = sde.run(path_artificial_drifters, drifter_list, output_dir=outputdir_plot, output_filename=outputfilename,isplot=False)
"""