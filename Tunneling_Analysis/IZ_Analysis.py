# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:44:28 2023

@author: Norman
"""
import numpy as np
import copy
import pandas as pd
from Import import choose_folder,choose_files
from Convert import vp_to_csv_index
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import axes3d
from IPython import get_ipython


def IZ_align(file_set):
    if "Z (Å)" in file_set.columns:
        return None
    
    col = copy.deepcopy(file_set["Zmon (Å)"])
    frames = col.index.get_level_values("Frames")
    frames = np.unique(frames)
    
    idx = pd.IndexSlice

    for i in frames:
        if i == frames[0]:
            newcol = col.loc[idx[i:i],:] - col.loc[idx[i:i],0][i][0]
        else:
            sub = col.loc[idx[i:i],:] - col.loc[idx[i:i],0][i][0]
            newcol = pd.concat([newcol,sub])
    newcol.name = "Z (Å)"

    out = pd.concat([file_set,newcol],axis = 1)
    return out

