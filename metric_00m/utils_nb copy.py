

from typing import Tuple, Optional
import glob
import os
import re
import pickle


class DictTable(dict):
    # Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    # and renders an HTML Table in IPython Notebook.
    def _repr_html_(self):
        html = ["<table width=100%>"]
        iter = 0
        for pat, dic in self.items():
            html.append("<tr>")
            if iter == 0:
                html.append(f'<td> </td>')
                for key in dic.keys():
                    html.append(f'<td>{key}</td>')
                html.append("</tr>")
                html.append("<tr>")

            html.append(f'<td> {pat} </td>')
            for key, value in dic.items():
                html.append(f'<td>{value:.3}</td>')
            html.append("</tr>")
            iter += 1
        html.append("</table>")
        return ''.join(html)


def make_list_spectrum(idir: str, region: str, depth: str
             ) ->Tuple[dict, dict]:
    pattern = f'spectrum*{region}_{depth}'
    listdir = sorted(glob.glob(os.path.join(idir, '**', pattern), recursive=True))
    return listdir


def make_list_eulerian(idir: str, region: str, depth: str
             ) ->Tuple[dict, dict]:
    pattern = f'eulerian_rms_{region}_*{depth}'
    listdir = sorted(glob.glob(os.path.join(idir, pattern, 'Eulerian_BINNED_*pyo'), recursive=True))
    return listdir
    

def make_list_sde(idir: str, region: str, depth: str
             ) ->Tuple[dict, dict]:
    pattern = f'{region}*{depth}'
    listdir = sorted(glob.glob(os.path.join(idir, pattern, '**')))
    return listdir


def make_list_frontsvel(idir: str, region: str, depth: str
             ) ->Tuple[dict, dict]:
    pattern = f'{region}*{depth}'
    listdir = sorted(glob.glob(os.path.join(idir, pattern, '**')))
    return listdir


listkey_comp = ('Eastward RMSD', 'Northward RMSD', 
           'Eastward Correlation', 'Northward Correlation',
           'Eastward Quadratic Error (%)', 'Northward Quadratic Error (%)',
           'Eastward Explained Variance (%)', 'Northward Explained Variance (%)',
           'Number of Points')
listkey_norm = ('Norm RMSD', 'Norm Correlation', 'Norm Quadratic Error (%)', 
               'Norm Explained Variance (%)', 
               'Number of Points')
DIC_LABEL = {'woc-l4-cureul15m-glob-1h': 'WOC inertial global 15m 1h',
             'woc-l4-cureul0m-glob-1h': 'WOC inertial global 00m 1h',
             'woc-l4-cureul-glob-1h': 'WOC inertial global 15m 1h',
             '015_004': 'CMEMS total REP',
             'eodyn': 'EODYN AIS',
             'oscar': 'OSCAR',
             'neurost': 'NEUROST',
             'woc-l4-curgeo-bfn-3h': 'WOC BFNQG 3h',
             '008_047': 'CMEMS Geostrophique REP',
             'woc-l4-dadr-med-1d': 'WOC dADR Med',
             'woc-l4-cur-natl3d_rep-1d': 'WOC Omega3D',
             'woc-l4-cureul-natl-1h': 'WOC inertial Natl 1h',
             'woc-l4-cur-natl2d_rep-1d': 'WOC SST-SSH',
             'unet_duacs_0m': 'unet_duacs_00',
             'unet_neurost_0m': 'unet_neurost_00',
             'unet_duacs_15m': 'unet_duacs_15',
             'unet_neurost_15m': 'unet_neurost_15',
             'ssh_duacs_sst_w_to_u_v_11d_15m_ageos_midtrain': 'ssh_duacs_sst_w_to_u_v_11d_15m_ageos_midtrain'
            }
DIC_LABEL_STD = {'Eulerian_STD_woc-l4-cureul15m-glob-1h': 'WOC inertial global 15m 1h',
             'Eulerian_STD_woc-l4-cureul0m-glob-1h': 'WOC inertial global 00m 1h',
            'Eulerian_STD_woc-l4-cureul-glob-1h': 'WOC inertial global 15m 1h',

             'Eulerian_STD_015_004': 'CMEMS total REP',
             'Eulerian_STD_woc-l4-curgeo-bfn-3h': 'WOC BFNQG 3h',
             'Eulerian_STD_008_047': 'CMEMS Geostrophique REP',
             'Eulerian_STD_woc-l4-dadr-med-1d': 'WOC dADR Med',
             'Eulerian_STD_woc-l4-cur-natl3d_rep-1d': 'WOC Omega3D',
             'Eulerian_STD_woc-l4-cureul-natl-1h': 'WOC inertial Natl 1h',
             'Eulerian_STD_woc-l4-cur-natl2d_rep-1d': 'WOC SST-SSH',
             'Eulerian_STD_eodyn': 'EODYN AIS',
             'Eulerian_STD_oscar': 'OSCAR',
             'Eulerian_STD_neurost': 'NEUROST',
             'Eulerian_STD_unet_duacs_0m': 'unet_duacs_0',
             'Eulerian_STD_unet_duacs_15m': 'unet_duacs_15',
             'Eulerian_STD_unet_neurost_0m': 'unet_neurost_0',
             'Eulerian_STD_unet_neurost_15m': 'unet_neurost_15',
             'Eulerian_STD_unet_duacs': 'unet_duacs',
             'Eulerian_STD_unet_neurost': 'unet_neurost',                 
            }

def make_dict_eul(idir: str, region: str, depth: str,listdir_add=None
             ) ->Tuple[dict, dict]:
    pattern = f'eulerian_rms_{region}*{depth}'
    listdir = glob.glob(os.path.join(idir, pattern, 'Eulerian_RMS_*pyo'))
    if listdir_add:
        listdir=listdir+listdir_add
    ddic_mean = {}
    ddic_std = {}
    print(listdir)
    for ifile in listdir:
        pat = re.split(f'({region})', os.path.basename(ifile))
        with open(ifile, 'rb') as f:
            dic = pickle.load(f)
        if 'STD' in ifile:  
            continue  
            pat = re.split(f'std_', os.path.splitext(os.path.basename(ifile))[0])
            pat = pat[-1].split('_')
            pat = '_'.join(pat[2:])
            label = DIC_LABEL[pat]
            ddic_std[label] = dic
        else:
            pat = re.split(f'mean_', os.path.splitext(os.path.basename(ifile))[0])
            pat = pat[-1].split('_')
            pat = '_'.join(pat[2:])
            print(pat)
            label = DIC_LABEL[pat]
            ddic_mean[label] = dic
    return ddic_mean, ddic_std


class DictTable_eul(dict):
    # Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    # and renders an HTML Table in IPython Notebook.

    def _repr_html_(self, listkey=listkey_norm):

        html = ["<table width=100%>"]
        iter = 0
        for pat, dic in self.items():
            print(pat)
            html.append("<tr>")
            if iter == 0:
                html.append(f'<td> </td>')
                for key in dic.keys():
                    if key not in listkey: continue

                    #if 'Percentage' in key: continue
                    if key in DIC_LABEL.keys():
                        label = DIC_LABEL[key]
                    html.append(f'<td>{key}</td>')
                html.append("</tr>")
                html.append("<tr>")

            html.append(f'<td> {pat} </td>')
            for key, value in dic.items():
                if key not in listkey: continue
                if 'Number' in key:
                    html.append(f'<td>{value}</td>')
                else:
                    html.append(f'<td>{value:.3}</td>')
            html.append("</tr>")
            iter += 1
        html.append("</table>")
        return ''.join(html)


class DictTable_eul_comp(dict):
    # Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    # and renders an HTML Table in IPython Notebook.

    def _repr_html_(self, listkey=listkey_comp):

        html = ["<table width=100%>"]
        iter = 0
        for pat, dic in self.items():
            print(pat)
            html.append("<tr>")
            if iter == 0:
                html.append(f'<td> </td>')
                for key in dic.keys():
                    if key not in listkey: continue

                    #if 'Percentage' in key: continue
                    if key in DIC_LABEL.keys():
                        label = DIC_LABEL[key]
                    html.append(f'<td>{key}</td>')
                html.append("</tr>")
                html.append("<tr>")

            html.append(f'<td> {pat} </td>')
            for key, value in dic.items():
                if key not in listkey: continue
                if 'Number' in key:
                    html.append(f'<td>{value}</td>')
                else:
                    html.append(f'<td>{value:.3}</td>')
            html.append("</tr>")
            iter += 1
        html.append("</table>")
        return ''.join(html)


