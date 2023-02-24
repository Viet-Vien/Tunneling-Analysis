# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 11:50:37 2022

@author: Norman
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 18:42:27 2022

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

dir_path = os.path.dirname(os.path.realpath(__file__)) # working folder path (folder that this file sits in)
folder_name = "\\EQT008 vs EQT010\\Spot2\\1nA"   
file_name = "\\STS_1Vs_000-VP327-VP.vpdata"                     
path = dir_path + folder_name + file_name
segment_number = 3   

def choose_files():                                    # function to open file selection dialogue box
    root = Tk()                                         # starts tkinter
    root.withdraw()                                     # hides tkinter initial dialogue box
    root.attributes('-topmost', True)                   # pushes newly opened window to always be on front
    file_paths = filedialog.askopenfilenames(initialdir = dir_path)              # opens file selection dialogue (from work directory)
    return file_paths 
# path = choose_files()[0]

def test_read(path,**kwargs): #read file from path
    file = pd.read_csv(path,**kwargs)
    return file.loc[:,~file.columns.duplicated()]

def subfolders(folder = None):
    subfolders = list([])
    if folder == None:
        folder = choose_folder()
    else:
        folder = folder
    paths = os.listdir(folder)
    for i in paths:
        #print(i)
        if os.path.isdir(os.path.join(folder,i))==True:
            subfolders.append(folder + '/' + i)
        else:
            continue
    return subfolders

def get_files(folder = None):
        files = list([])
        if folder == None:
            folder = choose_folder()
        else:
            folder = folder    
        paths = os.listdir(folder)
        for i in paths:
            #print(i)
            if os.path.isdir(os.path.join(folder,i))==False:
                files.append(folder + '/' + i)
            else:
                continue
        return files

        
def get_badrows(path):                              # .vpdata files have a lot of bad rows that are metadata etc. that need to be removed, this function indentifies the rows by their index
    file = pd.read_fwf(path,header = None)          # rough import
    badindex = np.array([])
    file2 = file[0]
    for i in file2:
        if "#C Index" in i:                         # header row needs to be excluded from removal
            continue
        elif '#' in i:                              # all bad rows start with #
            index = np.array(file2[file2 == i].index)
            badindex = np.append(badindex,index)
    return np.unique(badindex)                      # a little awkward, duplicates need to be removed because there are many rows with the same name and therefore return their index multiple times

def import_vp(path):                                # turns .vpdata file into a DataFrame
    row_skip = get_badrows(path)
    file = pd.read_csv(path,sep = '\t',skiprows = row_skip, header = 0)
    columns = file.columns
    for i in columns:
        if '.1' in i:
            file.drop(i,axis = 1,inplace = True)    #the MK2 somehow saves rows multiple times.... maybe something with the autosave?
    return file

def vp_to_csv(file,path,newpath):
    file.to_csv(newpath, sep=',',header = True, index = False)

def vp_convert_all(folder,newfolder):
    files = listdir(folder)
    vp_files = [i for i in files if '.vpdata' in i]
    vp_file_paths = [folder + '\\' + i for i in vp_files] #get file paths in original folder
    vp_file_names = [i.rstrip('.vpdata') for i in vp_files]     #get only file names without file appendage
    vp_file_paths_new = [newfolder + '\\' + i + ".txt" for i in vp_file_names] #filepath of converted files
    for i in range(len(vp_files)):
        file = import_vp(vp_file_paths[i])
        vp_to_csv(file,vp_file_paths[i],vp_file_paths_new[i])

def choose_folder():                                    # function to open folder selection dialogue box
    root = Tk()                                         # starts tkinter
    root.withdraw()                                     # hides tkinter initial dialogue box
    root.attributes('-topmost', True)                   # pushes newly opened window to always be on front
    open_file = filedialog.askdirectory(initialdir = dir_path)              # opens folder selection dialogue (from work directory)
    return open_file

def choose_files():                                    # function to open file selection dialogue box
    root = Tk()                                         # starts tkinter
    root.withdraw()                                     # hides tkinter initial dialogue box
    root.attributes('-topmost', True)                   # pushes newly opened window to always be on front
    file_paths = filedialog.askopenfilenames(initialdir = dir_path)              # opens file selection dialogue (from work directory)
    return file_paths                                   # returns tuple of file paths

def vp_convert_all_choose():                            # converts all .vpdata files in chosen folder to proper format
    open_file = choose_folder()
    vp_convert_all(open_file,open_file)


# New attempt at importing and converting all kinds of datasets (STS and TS)

def get_vp_meta(path):              # get bad rows of vp file for import, as well as outputs metadata as a file 
    file = pd.read_csv(path,sep = '::',nrows = 13, skiprows=1,header = None,engine='python')
    return file

def TS_import_help(path):                              # .vpdata files have a lot of bad rows that are metadata etc. that need to be removed, this function indentifies the rows by their index
    file = pd.read_fwf(path,header = None)          # rough import
    badindex = np.array([])
    metaindex = np.array([])
    file2 = file[0]
    for i in file2:
        if "#C Index" in i:                         # header row needs to be excluded from removal
            continue
        elif ":: VP[" and "# S[" in i:
            index = file2[file2==i].index
            metaindex =  np.append(metaindex,index)
            badindex = np.append(badindex,index)
        elif '#' in i:                              # all bad rows start with #
            index = np.array(file2[file2 == i].index)
            badindex = np.append(badindex,index)
    return [np.unique(badindex),metaindex,get_vp_meta(path)]                      # a little awkward, duplicates need to be removed because there are many rows with the same name and therefore return their index multiple times

def import_vp_TS(path):                                # turns .vpdata file into a DataFrame
    aux = TS_import_help(path)
    row_skip = aux[0]
    file = pd.read_csv(path,sep = '\t',skiprows = row_skip, header = 0)
    columns = file.columns
    for i in columns:
        if '.1' in i:
            file.drop(i,axis = 1,inplace = True)    #the MK2 somehow saves rows multiple times.... maybe something with the autosave?
    return [file,aux[1],aux[2]]


def STS_import_help(path):                              # .vpdata files have a lot of bad rows that are metadata etc. that need to be removed, this function indentifies the rows by their index
    file = pd.read_fwf(path,header = None)          # rough import
    badindex = np.array([])
    metaindex = np.array([])
    file2 = file[0]
    for i in file2:
        if "#C Index" in i:                         # header row needs to be excluded from removal
            continue
        elif ":: VP[" and "# S[" in i:
            index = file2[file2==i].index
            metaindex =  np.append(metaindex,index)
            badindex = np.append(badindex,index)
        elif '#' in i:                              # all bad rows start with #
            index = np.array(file2[file2 == i].index)
            badindex = np.append(badindex,index)
    #VT_list = file.loc[metaindex[0]:metaindex[-1]][0]
    #VT_list = VT_list.str.split("  :: VP\[|]=",expand = True)
    meta = get_vp_meta(path)
    meta[1][3] = path
    VT_list = VP_checklist([np.unique(badindex),metaindex,meta],path)
    return [np.unique(badindex),VT_list,meta]                      # a little awkward, duplicates need to be removed because there are many rows with the same name and therefore return their index multiple times

def VP_checklist(aux,path):
    VP_list = pd.read_csv(path,header = None,skiprows = int(aux[1][0]),skipfooter= int(aux[0][-1] - aux[1][-1]),engine='python')
    seps = list(["# |  :: VP\[|]=","=| ",'=| ','=| ','=| ','=| ','=| ','=| ','=| ','=| '])
    inds = list([0,1,2,3,4,5,6,7,8,9])
    col_names = list([])
    for i in range(len(seps)):
        f = lambda x: re.split(seps[inds[i]],x[inds[i]])
        VP_list[inds[i]] = VP_list.apply(f,axis = 1)
        if i ==0:
            col_names.append("Seg")
            col_names.append("Seg_Points")
        if i != 0:
            col_names.append(VP_list[inds[i]][0][2] + VP_list[inds[i]][0][4])
    VP_list.insert(0,"test",np.empty(len(VP_list[0])),True)
    #print('length:',len(VP_list.columns))
    for i in range(len(VP_list[0])):
        for j in VP_list.columns:
            if j == "test":
                VP_list["test"][i] = copy.deepcopy(VP_list[0][i][1])
            elif j == 0:
                VP_list[j][i] = copy.deepcopy(VP_list[j][i][2])
            else:
                VP_list[j][i] = copy.deepcopy(VP_list[j][i][3])
    VP_list.columns = col_names
    return VP_list


def import_vp_STS_fix(path):
    aux = STS_import_help(path)
    row_skip = aux[0]
    file = pd.read_csv(path,sep = '\t',skiprows = row_skip, header = 0)
    columns = file.columns
    for i in columns:
        if '.1' in i:
            file.drop(i,axis = 1,inplace = True) 
    return [file,aux[1],aux[2]]             #aux[1] are vector position list rows, aux[2] is metadata

def check_imp_STSnums(imp,singles_points = 2000):       #gets and checks if number of points of STS import matches expected points
    meta1 = imp[2]
    meta2 = imp[1]
    tot_points = int(meta1[1][10].strip(' N=')) # read total number of points
    IVs = int(meta1[1][7].strip(' #IV='))
    if len(meta2 == 3):                     # just for singles measurmements. In this case segment points have to be input manually
        seg_points = singles_points
    else:
        seg_points= int(meta2["Seg_Points"][3])     #get points a frame should contain
    if IVs*seg_points != tot_points:                #check
        return False
    else:
        return True
    
def check_STSorder(imp):                            #for STS measurments with multiple frames, checks if a frame was skipped or replaced with nonsense frame
    check_arr = np.array([])
    ind_arr = np.array([])
    for i in range(len(imp[1]["Seg"])):
        if i == len(imp[1]["Seg"])-1:
            check_arr = np.append(check_arr, 1)
            ind_arr = np.append(ind_arr,i)
            continue
        else:
            check_arr = np.append(check_arr,order_check(imp[1]["Seg"][i],imp[1]["Seg"][i+1]))
            ind_arr = np.append(ind_arr,i)
    return [check_arr,ind_arr]
        
    
def order_check(entry,next_entry):      #help function for check_STSorder, performs the order check on a segment
    order = ["S[1]","S[4]","S[7]"]
    if entry == order[0] and next_entry == order[1]:
        return True
    elif entry == order[1] and next_entry == order[2]:
        return True
    elif entry == order[2] and next_entry == order[0]:
        return True
    else:
        return False

def check_time(imp):                         #fixing time reset ebug in raw data before removing/treating problem sections
    #print(imp[1][['"Time"ms']])
    #print(pd.to_numeric(imp[1][['"Time"ms']]))    
    diff = pd.to_numeric(imp[1][['"Time"ms']].squeeze()).diff()
    #print(diff.diff())
    diff = diff[diff<0]
    return diff

def check_xyz(imp):                 #checks if controller messed up X,Y or Z piezo voltages during measurement
    x_start = imp[1]['"XS"Å'][0]
    y_start = imp[1]['"YS"Å'][0]
    z_start = imp[1]['"ZS"Å'][0]
    xs = imp[1]['"XS"Å'] 
    ys = imp[1]['"YS"Å']
    zs = imp[1]['"ZS"Å'] 
    x_err = xs[xs!=x_start].index
    y_err = ys[ys!=y_start].index
    z_err = zs[zs!=z_start].index
    if len(x_err) != 0 or len(y_err) != 0 or len(z_err) != 0:
        return True
    else:
        return False

def STSfile_check(imp,V = 0.51):
    check_res = list([]) 
    
    point_check = check_imp_STSnums(imp)
    check_res.append([point_check])
    
    order_check = check_STSorder(imp)
    check_res.append(order_check)
    
    time_check = check_time(imp)
    check_res.append([time_check])
    
    xyz_check = check_xyz(imp)
    check_res.append([xyz_check])
    
    u_check = U_check(imp,V)
    check_res.append([u_check])
    
    check_res.append([str(imp[2][1][3])])
    
    return check_res


def STSfile_allcheck(folder = None):
    if folder == None:  
        folder = choose_folder()
    else:
        folder = folder
    paths = os.listdir(folder)
    point_errs = 0
    point_arr = list([])
    order_errs = 0
    order_arr = list([])
    time_errs = 0
    time_arr = list([])
    err_arr = list([])
    xyz_errs = 0
    xyz_arr = list([])
    U_err = 0
    U_arr = list([])
    for i in paths:
            imp = import_vp_STS_fix(folder+'/'+i)
            check_arr = STSfile_check(imp)
            err_arr.append([check_arr])
            if check_arr[0][0]==False:
                point_errs +=1
                point_arr.append(i)
            if 0 in  check_arr[1][0]:
                order_errs +=1
                order_arr.append(i)
            if len(check_arr[2][0])!= 0:
                time_errs +=1
                time_arr.append(i)
            if check_arr[3][0]==True:
                xyz_errs +=1
                xyz_arr.append(i)
            if len(check_arr[4][0]['Umon (V)']) != 0:
                   U_err +=1
                   U_arr.append(i)
    print('Point Errors: ',point_errs)
    print(point_arr)
    print('Order Errors: ',order_errs)
    print(order_arr)
    print('Time Errors: ',time_errs)
    print(time_arr)
    print('XYZ Errors: ',xyz_errs)
    #print(xyz_arr)
    print('U Errors: ',U_err)
    print(U_arr)

    return err_arr

def U_check(imp,V):                                     # Checks if controller messed up bias Voltage (whether voltage higher than input was applied)
    err_arr = imp[0][abs(imp[0]['Umon (V)']) > V]
    return err_arr

def U_allcheck(V,folder = None):
    if folder == None:
        folder = choose_folder()
    paths = os.listdir(folder)
    err_arr = list([])
    U_err = 0
    U_arr = list([])
    for i in paths:
            imp = import_vp_STS_fix(folder+'/'+i)
            check_arr = U_check(imp,V)
            err_arr.append([check_arr])
            if len(check_arr['Umon (V)']) != 0:
                   U_err +=1
                   U_arr.append(i)
    print('U Errors: ',U_err)
    print(U_arr)

    
# path = "D:/Work/Python_Analysis/Tunneling_Analysis/TS_1000ms_000-VP223-VP.vpdata"
# path = choose_files()[0]
# path = "D:/Work/Python_Analysis/Tunneling_Analysis/STS_100Vs_000-VP188-VP.vpdata"
# STS_imp = import_vp_STS_fix(path)



# file = pd.read_fwf(path,header = None)          # rough import
# file2 = file[0]
# indices = np.array([])
# for i in file2:
#     if ":: VP[" and "# S[" in i:
#         index = file2[file2==i].index
#         indices =  np.append(indices,index)
# file3 = int(get_vp_meta(path)[1][10].lstrip(" N="))    
# # def get_more_meta(path):
#      file = pd.read_fwf(path,header = None)
#      index = file.index(i if '# S' in i)
    
# file = pd.read_fwf(path,header = None)
# file0 = file [0]
# index = [file0[file0 == i].index[0] for i in file0 if "# S" in i]


# file = get_vp_meta(choose_files()[0])

# def import_vp_meta(path):                                # turns .vpdata file into a DataFrame
#     row_skip = get_badrows(path)
#     file = pd.read_csv(path,sep = '\t',skiprows = row_skip, header = 0)
#     columns = file.columns
#     for in columns:
#         if '.1' in i:
#             file.drop(i,axis = 1,inplace = True)    #the MK2 somehow saves rows multiple times.... maybe something with the autosave?
#     return file



# vp_convert_all_STS()

#vp_convert_all_choose()
# vp_convert_all(dir_path + folder_name,dir_path + folder_name)

