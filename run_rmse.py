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

# Lire le fichier JSON
with open(file_path+file_name, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Exemple de modification : ajouter une nouvelle clé-valeur
data['data_type'] = xp_name
data['label'] = xp_name
data['path'] = path_files

# Afficher les données actuelles
print("Données actuelles :")
print(json.dumps(data, indent=4, ensure_ascii=False))

file_name_update = f'{xp_name}.json'
# Écrire les modifications dans le fichier JSON
with open(file_path+file_name_update, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"\nLe fichier {file_name_update} a été créé.")

# Calcul des metrics 

if "_00m" in xp_name:
    depth = 0
elif "_15m" in xp_name:
    depth = 15
else: 
    print("no depth in xp name")
    depth = 15
# Formater depth avec deux chiffres significatifs
depth_formatted = "{:02}".format(depth)

input_dict = f'{base_output}metric/dictionary/'
input_drifter = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_data/drifter/'
outputdir = f'{base_output}rec/{xp_name}/metric'

path_dict_product = input_dict+f'{xp_name}.json' 

first_date = datetime.datetime.strptime('20190101T000000Z', const.FMT)
last_date  = datetime.datetime.strptime('20191231T000000Z', const.FMT) 

outputdir = f'{base_output}rec/{xp_name}/metric/Agulhas/'

path_dict_region = input_dict+'region_Agulhas.json'
drifter_list = [input_drifter+f'Drifters_AOML_region_T1_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 

outputdir = f'{base_output}rec/{xp_name}/metric/GulfStream/'
path_dict_region = input_dict+'region_GulfStream.json'
#drifter_list = [input_drifter+'Drifters_AOML_region_T1_00m_20190101T000000Z_20200101T000000Z.pyo.gz']
drifter_list = [input_drifter+f'Drifters_AOML_region_GulfStream_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 

outputdir = f'{base_output}rec/{xp_name}/metric/Mediterranean/'
path_dict_region = input_dict+'region_Mediterranean.json'
#drifter_list = [input_drifter+'Drifters_AOML_region_T1_00m_20190101T000000Z_20200101T000000Z.pyo.gz']
drifter_list = [input_drifter+f'Drifters_AOML_region_Mediterranean_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 


print("Add CAL")

if "_00m" in xp_name:
    input_drifter = '/Odyssey/private/t22picar/data/drifters/drifter_00m/AOML_GL_00/'
elif "_15m" in xp_name:
    input_drifter = '/Odyssey/private/t22picar/data/drifters/AOML/'
else: 
    print("No depth ?")
outputdir = f'{base_output}rec/{xp_name}/metric'

path_dict_product = input_dict+f'{xp_name}.json' 

first_date = datetime.datetime.strptime('20190101T000000Z', const.FMT)
last_date  = datetime.datetime.strptime('20191231T000000Z', const.FMT) 

outputdir = f'{base_output}rec/{xp_name}/metric/California/'

path_dict_region = input_dict+'region_California.json'

# Warning ! CMEMS instead of AOML ?!
drifter_list = [input_drifter+f'Drifters_AOML_GL_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 