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
#from src import utils
#import hydra

#with hydra.initialize('config', version_base='1.3'):
#    cfg = hydra.compose("main", overrides=[
#        'xp=ose_pipeline_1y_global_4_multivar_15m_unet_1patch_test_L4'])
#xp_name=cfg.xp_name

# Récupération du xp_name 
xp_name = sys.argv[1]
print(xp_name)

### Creation du fichier .json

path_files=f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/daily/'

# Chemin vers le fichier JSON
file_path = '/Odyssey/private/t22picar/multivar_uv/metric/dictionary/'
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

if "_0m" in xp_name:
    depth = 0
elif "_15m" in xp_name:
    depth = 15
else: 
    print("no depth in xp name")
    depth = 0
# Formater depth avec deux chiffres significatifs
depth_formatted = "{:02}".format(depth)

input_dict = '/Odyssey/private/t22picar/multivar_uv/metric/dictionary/'
input_drifter = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_data/drifter/'
outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric'

path_dict_product = input_dict+f'{xp_name}.json' 

first_date = datetime.datetime.strptime('20190101T000000Z', const.FMT)
last_date  = datetime.datetime.strptime('20191231T000000Z', const.FMT) 

outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/Agulhas/'

path_dict_region = input_dict+'region_Agulhas.json'
#drifter_list = [input_drifter+'Drifters_AOML_region_T1_00m_20190101T000000Z_20200101T000000Z.pyo.gz']
drifter_list = [input_drifter+f'Drifters_AOML_region_T1_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 

outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/GulfStream/'
path_dict_region = input_dict+'region_GulfStream.json'
#drifter_list = [input_drifter+'Drifters_AOML_region_T1_00m_20190101T000000Z_20200101T000000Z.pyo.gz']
drifter_list = [input_drifter+f'Drifters_AOML_region_GulfStream_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 


outputdir = f'/Odyssey/private/t22picar/multivar_uv/rec/{xp_name}/metric/Mediterranean/'
path_dict_region = input_dict+'region_Mediterranean.json'
#drifter_list = [input_drifter+'Drifters_AOML_region_T1_00m_20190101T000000Z_20200101T000000Z.pyo.gz']
drifter_list = [input_drifter+f'Drifters_AOML_region_Mediterranean_{depth_formatted}m_20190101T000000Z_20200101T000000Z.pyo.gz']

eulerian.run(drifter_list, path_dict_product, 
             first_date=first_date, last_date=last_date, 
             region=path_dict_region, sdepth=1, output_dir=outputdir) 
