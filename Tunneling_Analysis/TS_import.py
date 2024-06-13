# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 18:24:21 2023

@author: Norman
"""
import numpy as np
import os
from os import listdir
from os import walk
import pandas as pd
import matplotlib.pyplot as plt
import math
from tkinter import Tk, filedialog
import re
import copy
from Import import choose_files, choose_folder, import_vp_TS, import_vp_STS_fix
from Convert import STS_combine,STS_combine_all, STS_set_frame_idx, make_folder_paths, get_files


def TS_combine(paths, length = 4):
    out = pd.DataFrame()
    frame_num = len(paths)
    frame_names = np.linspace(1, frame_num,frame_num)
    for i in range(len(paths)):
       
        #print(i)
        #print(paths[i])
        imp = import_vp_STS_fix(paths[i])
        data = imp[0]
        if i == 0:
            meta1,meta2 = imp[1],imp[2]
        STS_set_frame_idx(data, frame_names[i])
        out = pd.concat([out,data])
    return [out,meta1,meta2]


def TS_combine_all(folder = None,subfldrs = False,length = 4): 
    if folder == None:
        folder = choose_folder()
    else:
        folder = folder
    if subfldrs == True:
        paths = make_folder_paths(folder)
    else: 
        paths = get_files(folder)
    out,meta1,meta2 = TS_combine(paths,length)
    return [out,meta1,meta2]

def make_ZI_paths(folder=None,initialdir = None):
    ZI_paths = list([])
    stability_paths = list([])
    if folder == None:    
        folder = choose_folder(initialdir= initialdir)
    paths = os.listdir(folder)
    for i in paths:
            if 'stability' in i:
                stability_paths.append(folder + '/'+ i)
                continue
            if len(os.listdir(os.path.join(folder,i))) == 0:
                continue
            ZI_paths.append(folder + '/'+ i)
    return [ZI_paths,stability_paths]

def ZI_combine(ZI_paths):
    out = list([])
    meta1 = list([])
    meta2 = list([])
    for i in ZI_paths:
        if len(i)== 0:
            continue
        eins,zwei,drei = TS_combine_all(i)
        out.append(eins)
        meta1.append(zwei)
        meta2.append(drei)
    return [out,meta1,meta2]

def ZI_get_current(ZI_files):
    FB_meta = list([])
    for i in ZI_files[2]:
        current = re.split(', Current=', i[1][6])
        current = float(re.split(' nA',current[1])[0])
        FB_meta.append(current)
    return np.array(FB_meta)

def ZI_dis_params(ZI_files,param = "ADC0-I (nA)"):
    medians = list([])
    deviations = list([])
    for i in ZI_files[0]:
        medians.append(i[param].median())
        deviations.append(i[param].std())
    return [np.array(medians),np.array(deviations)]   
    

def plot_ZI_dist(ZI_files, show = True,param = "ADC0-I (nA)",ylabel = 'I(nA)', title = 'Setpoint stability I',label = 'Average Current'):
    FB_meta = ZI_get_current(ZI_files)

    sorter = np.argsort(FB_meta)

    FB_meta = FB_meta[sorter]


    medians,deviations = ZI_dis_params(ZI_files,param)

    medians = np.array(medians)[sorter]
    deviations = np.array(deviations)[sorter]

    plt.plot(FB_meta,medians,'-b', label  = label)
    plt.plot(FB_meta,np.add(medians,deviations),'--r' , label = '+/- Standard Deviation')
    plt.plot(FB_meta,np.subtract(medians,deviations),'--r')


    plt.legend()
    plt.ylabel(ylabel)
    plt.xlabel('Current Setpoint (nA)')
    plt.title(title)
    if show == True:
        plt.show()

def plot_ZI_Zdist(ZI_files, show = True):
    plot_ZI_dist(ZI_files, show = show, param = "Zmon (Å)", ylabel = 'Z Global', title = 'Setpoint stability Z', label = 'Average position')
    



def save_ZIfile(ZI_files,filename, folder = None, initialdir = None):
    if folder == None:
        folder = choose_folder(initialdir = initialdir)
    savepath = os.path.join(folder,filename)
    if isinstance(ZI_files,list) == True:
        ZI_files = pd.DataFrame(ZI_files).transpose()
    ZI_files.to_pickle(savepath)

def ZI_convert(filename, folder = None, initialdir = None,savefolder = None):
    if folder == None:
        folder = choose_folder(initialdir = initialdir)
    if savefolder == None:
        savefolder = folder
    ZI_paths = make_ZI_paths(folder = folder)
    paths = ZI_paths[0]
    ZI_files = ZI_combine(paths)
    save_ZIfile(ZI_files,filename, folder = savefolder,initialdir = initialdir)
##%%

# initialdir = choose_folder()
# #%%
# file_set = TS_combine(choose_files(initialdir= initialdir))
# #%%
# initialdir = choose_folder()
# ZI_paths = make_ZI_paths(initialdir)
# paths = ZI_paths[0]
# stab_paths = ZI_paths[1]

# #%%

# ZI_files = ZI_combine(paths)
# #%%
# print(type(ZI_files))
# print(isinstance(ZI_files,list))
# #%%
# plot_ZI_dist(ZI_files)

# #%%

# #save_folder = choose_folder(initialdir = initialdir)
# #file_name = 'ZI1'
# savepath = os.path.join(initialdir,file_name)
# #ZI_files = pd.DataFrame(ZI_files)
# ZI_files.to_pickle(savepath)

# #%%
# #I_files = ZI_files.transpose(
# ZI_files = pd.read_pickle(choose_files(initialdir = initialdir)[0])
# #%%

# file_set.plot.scatter(x = "Zmon (Å)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)
# file_set.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)
# file_set.plot.scatter(x = "Time (ms)", y = "Zmon (Å)",c="DarkBlue",s=0.1)

# #%%

# print(file_set["ADC0-I (nA)"].median())
# print(file_set["ADC0-I (nA)"].std())



