# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 11:51:10 2022

@author: Norman
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:25:46 2022

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
from pandas.core.base import PandasObject
from Import import import_vp, vp_to_csv, choose_folder, import_vp_TS, import_vp_STS_fix
# import xarray as xr

dir_path = os.path.dirname(os.path.realpath(__file__)) # working folder path (folder that this file sits in)
# segment_number = 3                                     # number of segments used for a single STS - curve

def choose_files():                                    # function to open file selection dialogue box
    root = Tk()                                         # starts tkinter
    root.withdraw()                                     # hides tkinter initial dialogue box
    root.attributes('-topmost', True)                   # pushes newly opened window to always be on front
    file_paths = filedialog.askopenfilenames(initialdir = dir_path)              # opens file selection dialogue (from work directory)
    return file_paths                                   # returns tuple of file paths

def test_read(path,**kwargs): #read file from path
    file = pd.read_csv(path,**kwargs)
    return file

def data_array(paths):
    frames_list = []
    for i in paths:
        frames_list.append(test_read(i))
    return frames_list

def vp_to_csv_index(file,path,newpath):
    file.to_csv(newpath, sep=',',header = True, index = True)
    
    
#############################################################################
#############################################################################

#   Converting STS_(...).vpdata files to .txt for subsequent analysis

##############################################################################
##############################################################################

# Data is assumed to consist of 3 segments per STS curve, each segment containing 1000 datapoints


# get number of frames, i.e. number of curves in the file
def get_frames(STS_set,segment_number):
    if isinstance (STS_set,list) == True:
        frame_number = []
        for i in STS_set:
            frame_number.append(int((i["Block-Start-Index"][i.index[-1]]+1000)/(segment_number * 1000)))
            # frame_number = [int(j) for j in frame_number]
        return frame_number
    else:
            frame_number = (STS_set["Block-Start-Index"][STS_set.index[-1]]+1000)/(segment_number * 1000)
            return int(frame_number)
        
#   function to adjust indices so that each frame/curve has restarting indices
def index_change(x,segment_number):                                #readjust dataframe indices according to number of data sets in file (for STS there are 3 segments per set)
    number = int((x)/segment_number / 1000)         #gives set number (starting from 0)
    out = x - number * segment_number * 1000
    return out

#   makes list of names for indexing of curve, i.e. curve number
def get_frame_names(frame_number,segment_number):
    frame_names = []
    string_size = 3                                     #assumed to have at max 999 curves
    for i in range(1,frame_number+1,1):                 #loop adds leading 0s
        string = str(i)
        while (len(string) < string_size):
            string = '0'+string
        for j in range(segment_number *1000):
            frame_names.append(string)
    return frame_names


#   adds multi-index to imported file, i.e. adds individual curve data point numbers and indices to identify seperate curves
def set_STS_frames(STS_set):
    file = STS_set
    number = get_frames(file,3)                  
    old_idx = file.index.to_frame()             #convert indices of file to a dataframe for better handling
    old_idx[0] = old_idx[0].map(lambda x: index_change(x,3))     #adjust indices so that each frame/curve has restarting indices
    frame_names = get_frame_names(number,3)
    mismatch = len(old_idx) - len(frame_names)  #for some reason GXSM3 appears to sometimes record to many segments, this cuts the data as a provisional bugfix
    if mismatch > 0:
        print(old_idx.tail(mismatch).index)
        print(old_idx)
        print(file)
        file.drop(old_idx.tail(mismatch).index,inplace = True)
        old_idx.drop(old_idx.tail(mismatch).index,inplace = True)
        print(file)
    old_idx.insert(0,"Frames",frame_names)
    file.index = pd.MultiIndex.from_frame(old_idx)  #replaces index of file with adjusted multiindex
    file = fix_STS(file, 3000)
    return file

def fix_STS(file,datapoints):                                        #controller sometimes resets clock between sets, this function fixes the time values
    index = file.index.get_level_values("Frames").unique()          #get "Frames" indices
    idx = pd.IndexSlice
    for i in range(len(index)-1):                                   #go through indices and compare last time value of each set with first time value of next, if time reset, then add previous time to all subsequent entries
        for j in range(2):
            f = int(datapoints*(j+1)/3)
            diffj = file.loc[index[i],f]["Time (ms)"]-file.loc[index[i],f-1]["Time (ms)"]
            if  diffj < 0:
                print(i," seg =",file.loc[index[i],f]["Time (ms)"]-file.loc[index[i],f-1]["Time (ms)"])
                print(file.loc[idx[index[i]:index[i],f:datapoints-1],:]["Time (ms)"])
                file.loc[idx[index[i]:index[i],f:datapoints-1],["Time (ms)"]] -= diffj
                print(file.loc[idx[index[i]:index[i],f:datapoints-1],:]["Time (ms)"])
                file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] -= diffj
            if i == len(index)-2:
                diffj = file.loc[index[i+1],f]["Time (ms)"]-file.loc[index[i+1],f-1]["Time (ms)"]
                file.loc[idx[index[i+1]:index[i+1],f:datapoints-1],["Time (ms)"]] -= diffj
        diffi = file.loc[index[i+1],0]["Time (ms)"]-file.loc[index[i],datapoints-1]["Time (ms)"]
        if diffi <0:
            print (i," between =", file.loc[index[i+1],0]["Time (ms)"]-file.loc[index[i],2999]["Time (ms)"])
            file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] -= diffi      
    return file

#   self-explanatory
def import_vp_STS(path):
    file = import_vp(path)
    file = set_STS_frames(file)
    return file

#   converts all STS_(...).vpdata in chosen folder
def vp_convert_all_STS():
    folder = choose_folder()
    files = listdir(folder)
    vp_files = [i for i in files if '.vpdata' and 'STS_' in i]
    vp_file_paths = [folder + '\\' + i for i in vp_files] #get file paths in original folder
    vp_file_names = [i.rstrip('.vpdata') for i in vp_files]     #get only file names without file appendage
    vp_file_paths_new = [folder + '\\' + i + ".txt" for i in vp_file_names] #filepath of converted files
    for i in range(len(vp_files)):
        file = import_vp_STS(vp_file_paths[i])
        vp_to_csv_index(file,vp_file_paths[i],vp_file_paths_new[i])
        
def vp_convert_all_STS_fast(): #not much faster if at all haha
    folder = choose_folder()
    files = listdir(folder)
    for i in files:
        if '.vpdata' and 'STS_' in i:
            vp_file_path = folder + '\\' + i #get file paths in original folder
            vp_file_name = i.rstrip('.vpdata')     #get only file names without file appendage
            vp_file_path_new = folder + '\\' + vp_file_name + ".txt" #filepath of converted files
            file = import_vp_STS(vp_file_path)
            vp_to_csv_index(file,vp_file_path,vp_file_path_new)


##############################################################################
##############################################################################

#   Converting TS_(...).vpdata files to .txt for easier analysis

##############################################################################
##############################################################################

def get_frame_names_TS(frame_number,segment_number,datapoints):
    frame_names = []
    string_size = 3                                     #assumed to have at max 999 curves
    for i in range(1,frame_number+1,1):                 #loop adds leading 0s
        string = str(i)
        while (len(string) < string_size):
            string = '0'+string
        for j in range(segment_number *datapoints):
            frame_names.append(string)
    return frame_names

def get_frames_TS(TS_set,segment_number,datapoints):
    if isinstance (TS_set,list) == True:
        frame_number = []
        for i in TS_set:
            frame_number.append(int((i["Block-Start-Index"][i.index[-1]]+datapoints)/(segment_number * datapoints)))
            # frame_number = [int(j) for j in frame_number]
        return frame_number
    else:
            frame_number = (TS_set["Block-Start-Index"][TS_set.index[-1]]+datapoints)/(segment_number * datapoints)
            return int(frame_number)
        
def index_change_TS(x,segment_number,datapoints):                                #readjust dataframe indices according to number of data sets in file (for STS there are 3 segments per set)
    number = int((x)/segment_number / datapoints)         #gives set number (starting from 0)
    out = x - number * segment_number * datapoints
    return out
        
def set_TS_frames(TS_imp):
    file = TS_imp[0]
    number = len(TS_imp[1])
    datapoints = int(int((TS_imp[2])[1][10].lstrip(" N="))/number)                 
    old_idx = file.index.to_frame()             #convert indices of file to a dataframe for better handling
    old_idx[0] = old_idx[0].map(lambda x: index_change_TS(x,1,datapoints))     #adjust indices so that each frame/curve has restarting indices
    frame_names = get_frame_names_TS(number,1,datapoints)
    mismatch = len(old_idx) - len(frame_names)  #for some reason GXSM3 appears to sometimes record to many segments, this cuts the data as a provisional bugfix
    if mismatch > 0:
        old_idx.drop(old_idx.tail(mismatch).index,inplace = True)
        file.drop(old_idx.tail(mismatch).index,inplace = True)
    old_idx.insert(0,"Frames",frame_names)
    file.index = pd.MultiIndex.from_frame(old_idx)          #replaces index of file with adjusted multiindex
    # file = fix_TS(file,datapoints)
    return file

def fix_TS(file,datapoints):                                        #controller sometimes resets clock between sets, this function fixes the time values
    index = file.index.get_level_values("Frames").unique()          #get "Frames" indices
    idx = pd.IndexSlice
    for i in range(len(index)-1):                                   #go through indices and compare last time value of each set with first time value of next, if time reset, then add previous time to all subsequent entries
        diffi = file.loc[index[i+1],0]["Time (ms)"]-file.loc[index[i],datapoints-1]["Time (ms)"]
        if diffi < 0:
            file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] -= diffi
    return file
    

def import_TS(path):
    TS_imp = import_vp_TS(path)
    file = set_TS_frames(TS_imp)
    return file

def vp_convert_all_TS_fast(): #not much faster if at all haha
    folder = choose_folder()
    files = listdir(folder)
    for i in files:
        if '.vpdata' and 'TS_' and 'ms_' in i:
            vp_file_path = folder + '\\' + i #get file paths in original folder
            vp_file_name = i.rstrip('.vpdata')     #get only file names without file appendage
            vp_file_path_new = folder + '\\' + vp_file_name + ".txt" #filepath of converted files
            file = import_TS(vp_file_path)
            vp_to_csv_index(file,vp_file_path,vp_file_path_new)

#############################################################################
#############################################################################

#   Converting STS_(...).vpdata files to .txt for subsequent analysis, while trying to catch errors

##############################################################################
##############################################################################



def fix_time_brute(file):                   #brute force attempt (not finished)
    index = file.index
    for i in range(1000,len(index),1000):
        diffi = file.loc[index[i]]["Time (ms)"]-file.loc[index[i-1]]["Time (ms)"] 
        if diffi < 0:
            print (i," diff = ",diffi)

def fix_time(file):                         #fixing time reset ebug in raw data before removing/treating problem sections
    diff = file[["Time (ms)"]].diff()
    diff = diff[diff["Time (ms)"]<0]
    for i in diff.index:
        file.loc[file.index[file.index >= i],"Time (ms)"] -= diff.loc[i,"Time (ms)"]
    return file

def find_STS_error(meta):                   # it seems like error sections in STS data can be found in the metadata, namely segments associated with rows contaun S[0]
    repl_error = []
    add_error = []
    err_file = meta.loc[["# S[0]" in j for j in meta[0]],:]
    for i in err_file.index:
        if "7" in meta.loc[i-1,0] and "1" in meta.loc[i+1,0]:
            add_error.append(meta.loc[i,1])
        else:
            repl_error.append(meta.loc[i,1])
    return ([add_error,repl_error])

def check_error(STS_imp):
    err_file = find_STS_error(STS_imp[1])
    if err_file == [[],[]]:
        return (False,err_file)
    else:
        return (True,err_file)

def drop_error_STS(STS_imp,err_file):
    file =STS_imp[0]
    segment_number = 3
    frame_number = int(STS_imp[2][1][7].lstrip(" #IV="))
    total_data = int(STS_imp[2][1][10].lstrip(" N="))
    meta = STS_imp[1]
    datapoints = int(meta.loc[meta.index[1],1])
    t_datapoints = frame_number*segment_number*datapoints
    if t_datapoints < total_data:
        for i in err_file[0]:
            # test = file.loc[:,"Block-Start-Index"]==int(i)
            file.drop(file[file.loc[:,"Block-Start-Index"]==int(i)].index,inplace = True)
    return file

def get_frame_names_STS_nope(STS_imp):                          #getting number of frames/IV curves from meta data, makes an array with unique string names including leading 0s
    frame_names = []
    string_size = 3                                     #assumed to have at max 999 curves
    frame_number = int(STS_imp[2][1][7].lstrip(" #IV="))                                
    for i in range(1,frame_number+1,1):                 #loop adds leading 0s
        string = str(i)
        while (len(string) < string_size):
            string = '0'+string
        frame_names.append(string)
    return frame_names

def get_frame_names_STS(frame_number,segment_number,datapoints):
    frame_names = []
    string_size = 3                                     #assumed to have at max 999 curves
    for i in range(1,frame_number+1,1):                 #loop adds leading 0s
        string = str(i)
        while (len(string) < string_size):
            string = '0'+string
        for j in range(segment_number *datapoints):
            frame_names.append(string)
    return frame_names

def index_change_STS(x,segment_number,datapoints):                                #readjust dataframe indices according to number of data sets in file (for STS there are 3 segments per set)
    number = int((x/segment_number / datapoints))         #gives set number (starting from 0)
    out = x - number * segment_number * datapoints
    return out

def set_STS_frames(STS_imp,err_check,segment_number,datapoints):
    STS_imp = STS_imp
    STS_imp[0] = fix_time(STS_imp[0])
    if err_check[0] == True:
        file = drop_error_STS(STS_imp,err_check[1])
    segment_number = 3
    frame_number = int(STS_imp[2][1][7].lstrip(" #IV="))
    total_data = int(STS_imp[2][1][10].lstrip(" N="))
    meta = STS_imp[1]
    datapoints = int(meta.loc[meta.index[1],1])
    frame_names = get_frame_names_STS(frame_number,segment_number,datapoints)                   
    old_idx = file.index.to_frame()             #convert indices of file to a dataframe for better handling
    old_idx[0] = old_idx[0].map(lambda x: index_change_STS(x,segment_number,datapoints))     #adjust indices so that each frame/curve has restarting indices
    old_idx.insert(0,"Frames",frame_names)
    file.index = pd.MultiIndex.from_frame(old_idx)  #replaces index of file with adjusted multiindex
    return file

def import_STS_fix(path):
    STS_imp = import_vp_STS_fix(path)
    segment_number = 3
    # frame_number = int(STS_imp[2][1][7].lstrip(" #IV="))
    meta = STS_imp[1]
    datapoints = int(meta.loc[meta.index[1],1])
    err_check = check_error(STS_imp)
    file = set_STS_frames(STS_imp,err_check, segment_number, datapoints)
    return (file,err_check[0])

def vp_convert_all_STS_fix(): #not much faster if at all haha
    folder = choose_folder()
    files = listdir(folder)
    for i in files:
        if '.vpdata' and 'STS_' in i:
            vp_file_path = folder + '\\' + i #get file paths in original folder
            vp_file_name = i.rstrip('.vpdata')     #get only file names without file appendage
            vp_file_path_new = folder + '\\' + vp_file_name + ".txt" #filepath of converted files
            data = import_STS_fix(vp_file_path)
            file = data[0]
            if data[1] == True:
                vp_file_path_new = folder + '\\' + vp_file_name +"_fixed" + ".txt"
                vp_file_path_err = folder + '\\' + vp_file_name +"_err" + ".txt"
            vp_to_csv_index(file[0],vp_file_path,vp_file_path_new)
            file[1].to_frame().to_csv(vp_file_path_err, sep=',')


# def fix_TS(file):
#     for i in file.index.unique:
# path = "D:/Work/Python_Analysis/Tunneling_Analysis/TS_1000ms_000-VP223-VP.vpdata"
# path = "D:/Work/EC_Data_analysis/Data/22_08_23 Twisted Edge EQT0xx/EQT008 vs EQT010/Spot1/setpoint 0,5 nA/TS_1000ms_000-VP221-VP.vpdata"
# path = "D:/Work/Python_Analysis/Tunneling_Analysis/STS_100Vs_000-VP188-VP.vpdata"

# file_test = import_STS_fix(path)
# file = file_test[0]


# err_file = find_STS_error(STS_imp[1])
# file = fix_time(STS_imp[0])
# segment_number = 3
# frame_number = int(STS_imp[2][1][7].lstrip(" #IV="))
# total_data = int(STS_imp[2][1][10].lstrip(" N="))
# meta = STS_imp[1].str.split("  :: VP\[|]=",expand = True)
# segment_points = int(meta.loc[meta.index[1],1])
# datapoints = frame_number*segment_number*segment_points
# if datapoints < total_data:
#     err_file = find_STS_error(STS_imp[1])
#     for i in err_file[0]:
#        test = file.loc[:,"Block-Start-Index"]==int(i)
#        file.drop(file[file.loc[:,"Block-Start-Index"]==int(i)].index,inplace = True)



# fig, axes = plt.subplots(nrows=3, ncols=1)

# file.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
# file.plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
# file.plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)  
# file.plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)



# print("go")
# # fix_time_brute(STS_imp[0])

# print(file)
# meta = STS_imp[1]
# meta = meta.str.split("  :: VP\[|]=",expand = True)
# for i in meta[0]:
#     if "# S[0]" in i:
#        print (i)
# data = meta.loc[["# S[0]" in j for j in meta[0]],:]
# for i in data.index:
#     if "7" in meta.loc[i-1,0] and "1" in meta.loc[i+1,0]:
#         print (meta.loc[i,:])
# data2 = meta[meta == meta.loc[41,0]].index
# data3 = meta.loc[:,0].index
# data = [meta.loc[i][0] for i in meta.index if "S[0]" in meta.loc[i][0]]
# data2 =meta.index[[meta[i]  for i in meta.index if "S[0]" in meta[i]]

# path = choose_files()[0]
# file = import_vp(path)
# file = set_STS_frames(file)
# index = file.index.get_level_values("Frames").unique()          #get "Frames" indices
# idx = pd.IndexSlice
# datapoints = 3000
# test = file.loc[idx["001":"001",2000:2930],:]["Time (ms)"]
# test2 = file.loc["001",1000]["Time (ms)"]-file.loc["001",999]["Time (ms)"]
# for i in range(len(index)-1):
#     for j in range(2):
#         f = int(datapoints*(j+1)/3)
#         diffj = file.loc[index[i],f]["Time (ms)"]-file.loc[index[i],f-1]["Time (ms)"]
#         if  diffj < 0:
#             print(i," seg =",file.loc[index[i],f]["Time (ms)"]-file.loc[index[i],f-1]["Time (ms)"])
#             file.loc[idx[index[i]:index[i],f:datapoints-1],:]["Time (ms)"] -= diffj
#             file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] -= diffj
#     diffi = file.loc[index[i+1],0]["Time (ms)"]-file.loc[index[i],datapoints-1]["Time (ms)"]
#     if diffi <0:
#         print (i," between =", file.loc[index[i+1],0]["Time (ms)"]-file.loc[index[i],2999]["Time (ms)"])
#         file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] -= diffi
    
# for i in range(len(index)-1):                                   #go through indices and compare last time value of each set with first time value of next, if time reset, then add previous time to all subsequent entries  
#     for j in range(2):
#              f = int(datapoints*(j+1)/3)
#              if file.loc[index[i],f]["Time (ms)"]-file.loc[index[i],f-1]["Time (ms)"]<0:
#                      file.loc[idx[index[i]:index[i],f:datapoints-1],:]["Time (ms)"] += file.loc[index[i],f-1]["Time (ms)"]
#                      file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] += file.loc[index[i],f-1]["Time (ms)"]
#     if file.loc[index[i+1],datapoints-1]["Time (ms)"]-file.loc[index[i],datapoints-1]["Time (ms)"]<0:
#             file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] += file.loc[index[i],datapoints-1]["Time (ms)"]
            
            
# TS_imp = import_vp_TS(path)
# file = import_TS(path)
#
# file = set_TS_frames(TS_imp)
# index = file.index.get_level_values("Frames").unique()
# blub = index[2]
# idx = pd.IndexSlice
# # test = file.loc[idx["001":"001",7499:7499],"Time (ms)"][0]
# # test2=  file.loc[idx["002":"002",7499:7499],"Time (ms)"][0]
# test3 = file.loc[index[0],7499]["Time (ms)"]

# for i in range(len(index)-1):
#     if file.loc[index[i+1],7499]["Time (ms)"]-file.loc[index[i],7499]["Time (ms)"]<0:
#         file.loc[idx[index[i+1]:index[len(index)-1]],:]["Time (ms)"] += file.loc[index[i],7499]["Time (ms)"]
#         print (file.loc[index[i+1],7499]["Time (ms)"])
    
# for i in index:
#     print(file[])
# vp_convert_all_TS_fast()

# string = getfram





# file = import_vp_STS(choose_files()[0])
    


# file = test_read(choose_files()[0])
# file = import_vp(choose_files()[0])
# number = get_frames(file)
# old_idx = file.index.to_frame()
# old_idx[0] = old_idx[0].map(lambda x: index_change(x,segment_number))
# frame_names = get_frame_names(number)
# mismatch = len(old_idx) - len(frame_names)
# old_idx.drop(old_idx.tail(mismatch).index,inplace = True)
# old_idx.insert(0,"Frames",frame_names)
# file.drop(old_idx.tail(mismatch).index,inplace = True)
# file.index = pd.MultiIndex.from_frame(old_idx)
# # files = data_array(choose_files())
# number = get_frames(file)
# old_idx = file.index.to_frame()
# old_idx[0] = old_idx[0].map(lambda x: index_change(x,segment_number))
# frame_names = get_frame_names(number)
# old_idx.insert(0,"Frames",frame_names)
# file.index = pd.MultiIndex.from_frame(old_idx)


# file = test_read(choose_files()[0])
# file2 = test_read(choose_files()[0])
# listtest = []
# listtest.append(file)
# listtest.append(file2)
