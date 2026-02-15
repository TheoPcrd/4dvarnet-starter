import velocity_metrics.utils.constant as const 
import velocity_metrics.spectrum.spectrum as spectrum 
import sys  
import datetime
from IPython.display import display, Markdown
import warnings 
warnings.filterwarnings("ignore") 
sys.path.append('/Odyssey/private/t22picar/2024_DC_WOC-ESA/')
import json

#list_region = ["Agulhas","GulfStream","Mediterranean","California","NA"]
list_region = ["Hawai","Canary"]

xp_name = sys.argv[1]
print(xp_name)
base_output="./"
# Calcul des metrics 

if "_0m" in xp_name or "_00m" in xp_name:
    depth = 0
    depth_ind=0
elif "_15m" in xp_name:
    depth = 15
    depth_ind=1
else: 
    print("no depth in xp name")
    depth = 15
    depth_ind=1
# Formater depth avec deux chiffres significatifs
depth_formatted = "{:02}".format(depth)

input_dict = f'{base_output}/metric/dictionary/'
input_drifter = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_data/drifter/'
path_dict_product = input_dict+f'{xp_name}.json' 

first_date = datetime.datetime.strptime('20190101T000000Z', const.FMT)
last_date  = datetime.datetime.strptime('20191231T000000Z', const.FMT) 

for region in list_region:

    print(region)

    outputdir = f'{base_output}rec/{xp_name}/metric_{depth_formatted}m/{region}/'
    path_dict_region = input_dict+f'region_{region}.json'
    dic_spectrum = spectrum.run([path_dict_product], path_dict_region, depth = depth_ind, output_dir= outputdir)