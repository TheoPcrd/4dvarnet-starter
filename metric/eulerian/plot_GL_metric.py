import velocity_metrics.utils.constant as const 
import velocity_metrics.eulerian.eulerian_drifters as eulerian  
import velocity_metrics.spectrum.spectrum as spectrum
import velocity_metrics.lagrangian.cumulative_distance as sde
import datetime
import sys   
from IPython.display import display, Markdown
import matplotlib.pyplot as plt
import cartopy 
import warnings 
warnings.filterwarnings("ignore") 
sys.path.append('/Odyssey/private/t22picar/2024_DC_WOC-ESA/')
from src import utils
import utils_nb as utils_nb
import pickle 
import os 

dir_eulerian = '/Odyssey/private/t22picar/2024_DC_WOC-ESA/dc_product_evaluation/DC_product_evaluation/eulerian_rms/'
base_outputdir = "../../"

#diroutput ="metric_bsize=0.125" 
def plot_lagrangian_result(list_xp_name,region_list,savefig=None,depth=15):

    if depth==15:
        path_metric="metric_15m"
    elif depth ==0:
        path_metric="metric_00m"

    for region in region_list:
        # Global Variables

        listdir = []
        list_color=['r','b', 'g', 'm', 'c', 'y','k','orange']
        listdir=[]

        for xp_name in list_xp_name:
            if "15m" in xp_name:
                listdir = listdir + [f"{base_outputdir}/rec/{xp_name}/{path_metric}/{region}/plot/SDE_region_{region}_20190101-20191231_{xp_name}.pyo.gz"]
            else:
                listdir = listdir + [f"{base_outputdir}/rec/{xp_name}/{path_metric}/{region}/plot/SDE_region_{region}_20190101-20191231_{xp_name}_15m.pyo.gz"]
        _list = []
        for ifile in listdir:
            if (os.path.splitext(ifile)[-1] != '.png') and ('miost' not in ifile):
                _list.append(ifile)
        listdir = _list #print(_list)
        
        if savefig:
            path=f"/Odyssey/private/t22picar/{base_outputdir}/rec/{savefig}/{path_metric}/{region}/plot_score/"
            if not os.path.exists(path):
                os.makedirs(path)
            #path_save = path+f"lagrangian_score_depth={depth}m.png"
            output_filename=f"lagrangian_score_depth={depth}m.png"
            #plt.savefig(path_save)
            fig = sde.plot(_list, output_dir=path, output_filename=output_filename,
                        list_color=list_color)
        else: 
            path=None
            output_filename=None
            fig = sde.plot(_list, list_color=list_color)
        
        fig[0].suptitle(f'{region} at 15m')

        if savefig:
            path=f"/Odyssey/private/t22picar/multivar_gs/rec/{savefig}/{path_metric}/{region}/plot_score/"
            if not os.path.exists(path):
                os.makedirs(path)
            path_save = path+f"lagrangian_score_depth={depth}m.png"
            plt.savefig(path_save)

def plot_rmse_score(list_xp_name,list_region,keys=None,depth=15):

    if depth ==15:
        path_metric="metric_15m"
    elif depth == 0:
        path_metric="metric_00m"

    for region in list_region:
        list_dict = []
        for xp_name in list_xp_name:
            outputdir = f'{base_outputdir}rec/{xp_name}/{path_metric}/{region}/'
            list_dict = list_dict+[{'type_stat':'Mean','path':outputdir+f'/Eulerian_RMS_{xp_name}.pyo','name':f'{xp_name}'}] 
            
        print(f"{region} result")
        display(DictTable_color(list_dict,keys=keys))

class DictTable_color():
    """
    Overridden dict class which takes a list of dictionaries and renders an HTML Table in IPython Notebook.
    The table cells are colored using a very light blue-to-pink gradient.
    The smallest value in each column is displayed in bold.
    """

    def __init__(self, list, keys=['Norm RMSD', 'Norm Correlation', 'Norm Quadratic Error (%)', 'Norm Explained Variance (%)', 'Number of Points']):
        self.html_table = None
        self.list = list
        self.keys = keys

    def _get_min_max_per_column(self):
        """Collect min and max values for each key (column)."""
        min_max = {key: {'min': float('inf'), 'max': float('-inf')} for key in self.keys}
        min_indices = {key: None for key in self.keys}
        max_indices = {key: None for key in self.keys}
        for i, dict in enumerate(self.list):
            filehandler = open(dict['path'], 'rb')
            object = pickle.load(filehandler)
            for key in self.keys:
                if key in object:
                    value = object[key]
                    if value < min_max[key]['min']:
                        min_max[key]['min'] = value
                        min_indices[key] = i
                    if value > min_max[key]['max']:
                        min_max[key]['max'] = value
                        max_indices[key] = i
        return min_max, min_indices, max_indices

    def _value_to_color(self, value, min_val, max_val):
        """Convert a value to a very light RGB color, from pastel blue to light pink."""
        if min_val == max_val:
            return "background-color: #ffffff; color: black;"

        # Normalize value between 0 and 1
        normalized = (value - min_val) / (max_val - min_val)

        # Use a quadratic easing for even lighter tones
        lightness = normalized ** 0.3

        # Very light blue (200, 230, 255) to light pink (255, 200, 220)
        red = int(200 + 55 * lightness)
        green = int(230 - 30 * lightness)
        blue = int(255 - 55 * lightness)

        return f"background-color: rgb({red}, {green}, {blue}); color: black;"


    def _value_to_color_r(self, value, min_val, max_val):
        """Convert a value to a RGB color between blue (low) and red (high)."""
        if min_val == max_val:
            return "background-color: #ffffff;"  # White if all values are the same

        # Normalize value between 0 and 1
        normalized = (value - min_val) / (max_val - min_val)

        # Use a quadratic easing for even lighter tones
        lightness = normalized ** 0.3  # Emphasize lightness

        # Very light blue (200, 230, 255) to light pink (255, 200, 220)
        red = int(200 + 55 * lightness)
        green = int(230 - 30 * lightness)
        blue = int(255 - 55 * lightness)

        return f"background-color: rgb({blue}, {green}, {red}); color: black;"
    
    def _repr_html_(self):
        min_max, min_indices, max_indices = self._get_min_max_per_column()

        filehandler = open(self.list[0]['path'], 'rb')
        object = pickle.load(filehandler)

        #html = ["<table style='border-collapse: collapse; width: 100%; border: 1px solid #dddddd;'>"]
        html = ["<table style='border-collapse: collapse; width: 100%; border: 1px solid #000000;'>"]
        html.append("<tr style='background-color: #f8f9fa; color: black;'>")
        html.append("<td style='border: 1px solid #000000; padding: 8px;'><b>{0}</b></td>".format(self.list[0]['type_stat']))
        for key in self.keys:
            if key in object:
                html.append("<td style='border: 1px solid #000000; padding: 8px;'><b>{0}</b></td>".format(key))
        html.append("</tr>")

        for i, dict in enumerate(self.list):
            filehandler = open(dict['path'], 'rb')
            object = pickle.load(filehandler)
            html.append("<tr>")
            html.append("<td style='border: 1px solid #000000; padding: 8px;'><b>{0}</b></td>".format(dict['name']))
            for key in self.keys:
                if key in object:
                    value = object[key]
                    min_val = min_max[key]['min']
                    max_val = min_max[key]['max']
                    if "Correlation" in key  or "Variance" in key:
                        style = self._value_to_color_r(value, min_val, max_val)
                        if max_indices[key] == i:
                            html.append("<td style='border: 1px solid #000000; padding: 8px; {1}'><b>{0}</b></td>".format("{:.2f}".format(value), style))
                        else:
                            html.append("<td style='border: 1px solid #000000; padding: 8px; {1}'>{0}</td>".format("{:.2f}".format(value), style))
                    else:
                        style = self._value_to_color_r(value, min_val, max_val)
                        # Check if this is the smallest value in the column
                        if min_indices[key] == i:
                            html.append("<td style='border: 1px solid #000000; padding: 8px; {1}'><b>{0}</b></td>".format("{:.2f}".format(value), style))
                        else:
                            html.append("<td style='border: 1px solid #000000; padding: 8px; {1}'>{0}</td>".format("{:.2f}".format(value), style))
            html.append("</tr>")

        html.append("</table>")
        self.html_table = '\n'.join(html)
        return self.html_table

def print_json(path_json):
    import json
    f = open(path_json)
    data = json.load(f)
    for i in data:
        print(i, ':', data[i])