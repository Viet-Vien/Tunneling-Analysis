# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 00:13:41 2022

@author: Norman
"""
import pandas as pd
from Import import choose_files
import matplotlib.pyplot as plt

##############################################################################
##############################################################################

#   Reading In  

##############################################################################
##############################################################################

#  "Umon (V)", "ADC0-I (nA)" , "Time (ms)"

def read_in(path,**kwargs): #read file from path
    file = pd.read_csv(path,**kwargs)
    return file

def read_in_TS(path):       #fix to annoying fact that indices consisting of numbers cannot be imported as string intuitively
    file = read_in(path,header = 0,dtype = {"Frames":str}, index_col = [1])         #keep numeric index level, import other index level as str valued column with dtype
    index = file.index.to_frame()                                                   #convert index to DataFrame (easier to handle)
    index.insert(0,"Frames",file["Frames"])                                         #take str column and add to index
    file.drop("Frames",axis = 1, inplace = True)                                    #drop string column from file
    file.index = pd.MultiIndex.from_frame(index)                                    #add correct index
    return file

def data_plot(data, x_string, y_string, **kwargs):                  #input: data = dataframe, x_string = column name string of x data, y_string = column name string of y data
    plot = plt.plot(x_string,y_string,data = data,**kwargs)
    return plot

path = "D:/Work/EC_Data_analysis/Data/22_08_23 Twisted Edge EQT0xx/EQT008 vs EQT010/Spot1/setpoint 0,5 nA/TS_1000ms_000-VP221-VP.txt"
path = choose_files()[0]
file = read_in_TS(path)
# file = read_in_TS(path)

fig, axes = plt.subplots(nrows=3, ncols=1)
# file.plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)
file.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
file.plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
file.plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)
