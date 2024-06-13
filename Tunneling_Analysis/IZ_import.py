# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 15:16:02 2023

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
from STS_Analysis import STS_2D_bin,plot_IVmap
from IZ_Analysis import IZ_align


def import_vp_IZ(path):
    return import_vp_TS(path)

def IZ_combine_paths(paths, length = 4):
    out = pd.DataFrame()
    frame_num = len(paths)
    frame_names = np.linspace(1, frame_num,frame_num)
    for i in range(len(paths)):
        #print(i)
        imp = import_vp_STS_fix(paths[i])
        data = imp[0]
        if i == 0:
            meta1 = imp[1]
            meta2 = imp[2]
        STS_set_frame_idx(data, frame_names[i])
        out = pd.concat([out,data])
    return [out,meta1,meta2]




def make_IZ_paths(folder=None,initialdir = None):
    IZ_paths = list([])
    #stability_paths = list([])
    if folder == None:    
        folder = choose_folder(initialdir= initialdir)
    paths = os.listdir(folder)
    for i in paths:
            # if 'stability' in i:
            #     stability_paths.append(folder + '/'+ i)
            #     continue
            if len(os.listdir(os.path.join(folder,i))) == 0:
                continue
            IZ_paths.append(folder + '/'+ i)
    return IZ_paths


def IZ_combine_folder(folder = None,subfldrs = False,length = 4): 
    if folder == None:
        folder = choose_folder()
    else:
        folder = folder
    if subfldrs == True:
        paths = make_folder_paths(folder)
    else: 
        paths = get_files(folder)
    IZ_data= IZ_combine_paths(paths,length)
    return IZ_data

def IZ_combine(IZ_paths):
    out = list([])
    meta1 = list([])
    meta2 = list([])
    for i in IZ_paths:
        if len(i)== 0:
            continue
        if os.path.isdir(i)==False:
            continue
        print(i)
        eins,zwei,drei = IZ_combine_folder(folder = i)
        out.append(eins)
        meta1.append(zwei)
        meta2.append(drei)
    return [out,meta1,meta2]

def IZ_singleparam(IZset):
        i = IZset
        current = re.split(', Current=', i[1][6])
        
        bias = re.split('Bias=',current[0])
        
        bias = float(re.split(' V',bias[1])[0])
        print(bias)
        current = float(re.split(' nA',current[1])[0])
        print(current)
        return [current,bias]

def IZ_get_params(IZ_files):
    FB_meta_curr = list([])
    FB_meta_bias = list([])
    for i in IZ_files[2]:
        if isinstance(i,int) == True:
            current,bias = IZ_singleparam(IZ_files[2])
            FB_meta_curr.append(current)
            FB_meta_bias.append(bias)
            break
        else:
            current = re.split(', Current=', i[1][6])
            print(current)
            bias = re.split('Bias=',current[0])
            print(bias)
            bias = float(re.split(' V',bias[1])[0])
            
            current = float(re.split(' nA',current[1])[0])
        FB_meta_curr.append(current)
        FB_meta_bias.append(bias)
    FB_meta_curr = np.array(FB_meta_curr)
    FB_meta_bias = np.array(FB_meta_bias)
    return np.array([FB_meta_curr,FB_meta_bias])

# path = choose_files()[0]
# imp = import_vp_TS(path)
# file = imp[0]
# meta1 = imp[1]
# meta2 = imp[2]

# #%%

# IZ_paths = make_IZ_paths()

# imp = IZ_combine(IZ_paths)


# #%%
# IZ_files = pd.DataFrame(imp).transpose()
    

# #%%
# meta = IZ_get_params(IZ_files)

# #%%

# from IPython import get_ipython

# #get_ipython().run_line_magic('matplotlib', 'inline')
# get_ipython().run_line_magic('matplotlib', 'qt')
# #%%
# file_set = IZ_combine_all(subfldrs = False)
# file_set = IZ_align(file_set)

# IZ_map = STS_2D_bin(file_set,params = ["Z (Å)","ADC0-I (nA)"],points = [1000,1000])
# plot_IVmap(IZ_map,logmod = 100)
# #%%
# # file_set = IZ_combine_all(subfldrs = True)

# # col = copy.deepcopy(file_set["Zmon (Å)"])
# # frames = col.index.get_level_values("Frames")
# # frames = np.unique(frames)
# # idx = pd.IndexSlice
# # newcol = col.loc[idx[1:1],:] 

# #%%
# #newcol2 = col.loc[idx[1:1],0][1][0]
# # file_set = IZ_align(file_set)

# #%%
# # IZ_map = STS_2D_bin(file_set,params = ["Z (Å)","ADC0-I (nA)"],points = [1000,1000])
# #%%
# # plot_IVmap(IZ_map,logmod = 100)





# #%%

# # file_set.plot.scatter(x = "Zmon (Å)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)
# # file_set.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)
# # file_set.plot.scatter(x = "Z (Å)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)



# #%%

# # out.plot.scatter(x = "Z (Å)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)
# # out.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)

