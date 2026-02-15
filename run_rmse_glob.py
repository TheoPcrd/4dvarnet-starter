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
import json

xp_name = sys.argv[1]
print(xp_name)

### Creation du fichier .json

base_output="/Odyssey/private/t22picar/multivar_drifter/"
path_files=f'{base_output}rec/{xp_name}/daily/'

# Chemin vers le fichier JSON
file_path = f'{base_output}metric/dictionary/'
file_name = 'data_type_metric_generic.json'

# Calcul des metrics 

if "_00m" in xp_name:
    depth = 0
    input_drifter = '/Odyssey/private/t22picar/data/drifters/drifter_00m/AOML_GL_00/'
elif "_15m" in xp_name:
    depth = 15
    input_drifter = '/Odyssey/private/t22picar/data/drifters/AOML/'
else: 
    print("no depth in xp name")
    depth = 15
# Formater depth avec deux chiffres significatifs
depth_formatted = "{:02}".format(depth)


input_dict = f'{base_output}metric/dictionary/'

outputdir = f'{base_output}rec/{xp_name}/metric'

path_dict_product = input_dict+f'{xp_name}.json' 

first_date = datetime.datetime.strptime('20190101T000000Z', const.FMT)
last_date  = datetime.datetime.strptime('20191231T000000Z', const.FMT) 

"""
outputdir = f'{base_output}rec/{xp_name}/metric/California/'

path_dict_region = input_dict+'region_California.json'

# Warning ! CMEMS instead of AOML ?!
drifter_list = [input_drifter+f'Drifters_AOML_GL_{depth}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 

"""

outputdir = f'{base_output}rec/{xp_name}/metric/Global/'

path_dict_region = input_dict+'region_global.json'

# Warning ! CMEMS instead of AOML ?!
drifter_list = [input_drifter+f'Drifters_AOML_GL_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 