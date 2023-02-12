# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:21:42 2023

@author: Norman
"""
from Import import *
#from Import import import_vp_STS_fix

from Convert import *

from tkinter import Tk, filedialog
import os
import pandas as pd
import re
import copy
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

# def choose_files():                                    # function to open file selection dialogue box
#     root = Tk()                                         # starts tkinter
#     root.withdraw()                                     # hides tkinter initial dialogue box
#     root.attributes('-topmost', True)                   # pushes newly opened window to always be on front
#     file_paths = filedialog.askopenfilenames(initialdir = dir_path)              # opens file selection dialogue (from work directory)
#     return file_paths 
# # path = choose_files()[0]

# def VP_checklist(aux):
#     VP_list = pd.read_csv(path,header = None,skiprows = int(aux[1][0]),skipfooter= int(aux[0][-1] - aux[1][-1]))
#     seps = list(["# |  :: VP\[|]=","=| ",'=| ','=| ','=| ','=| ','=| ','=| ','=| ','=| '])
#     inds = list([0,1,2,3,4,5,6,7,8,9])
#     col_names = list([])
#     for i in range(len(seps)):
#         f = lambda x: re.split(seps[inds[i]],x[inds[i]])
#         VP_list[inds[i]] = VP_list.apply(f,axis = 1)
#         if i ==0:
#             col_names.append("Seg")
#             col_names.append("Seg_Points")
#         if i != 0:
#             col_names.append(VP_list[inds[i]][0][2] + VP_list[inds[i]][0][4])
#     VP_list.insert(0,"test",np.empty(len(VP_list[0])),True)
#     #print('length:',len(VP_list.columns))
#     for i in range(len(VP_list[0])):
#         for j in VP_list.columns:
#             if j == "test":
#                 VP_list["test"][i] = VP_list[0][i][1]
#             elif j == 0:
#                 VP_list[j][i] = VP_list[j][i][2]
#             else:
#                 VP_list[j][i] = VP_list[j][i][3]
#     VP_list.columns = col_names
#     return VP_list

# def check_imp_STSnums(imp):
#     meta1 = imp[2]
#     meta2 = imp[1]
#     tot_points = int(meta1[1][10].strip(' N='))
#     IVs = int(meta1[1][7].strip(' #IV='))
#     seg_points= int(meta2["Seg_Points"][3])
#     if IVs*seg_points != tot_points:
#         return False
#     else:
#         return True
    
# def check_STSorder(imp):
#     check_arr = np.array([])
#     ind_arr = np.array([])
#     for i in range(len(imp[1]["Seg"])):
#         if i == len(imp[1]["Seg"])-1:
#             check_arr = np.append(check_arr, 1)
#             ind_arr = np.append(ind_arr,i)
#             continue
#         else:
#             check_arr = np.append(check_arr,order_check(imp[1]["Seg"][i],imp[1]["Seg"][i+1]))
#             ind_arr = np.append(ind_arr,i)
#     return [check_arr,ind_arr]
        
    
# def order_check(entry,next_entry):
#     order = ["S[1]","S[4]","S[7]"]
#     if entry == order[0] and next_entry == order[1]:
#         return True
#     elif entry == order[1] and next_entry == order[2]:
#         return True
#     elif entry == order[2] and next_entry == order[0]:
#         return True
#     else:
#         return False

# def check_time(imp):                         #fixing time reset ebug in raw data before removing/treating problem sections
#     #print(imp[1][['"Time"ms']])
#     #print(pd.to_numeric(imp[1][['"Time"ms']]))    
#     diff = pd.to_numeric(imp[1][['"Time"ms']].squeeze()).diff()
#     #print(diff.diff())
#     diff = diff[diff<0]
#     return diff

# def check_xyz(imp):
#     x_start = imp[1]['"XS"Å'][0]
#     y_start = imp[1]['"YS"Å'][0]
#     z_start = imp[1]['"ZS"Å'][0]
#     xs = imp[1]['"XS"Å'] 
#     ys = imp[1]['"YS"Å']
#     zs = imp[1]['"ZS"Å'] 
#     x_err = xs[xs!=x_start].index
#     y_err = ys[ys!=y_start].index
#     z_err = zs[zs!=z_start].index
#     if len(x_err) != 0 or len(y_err) != 0 or len(z_err) != 0:
#         return True
#     else:
#         return False

# def STSfile_check(imp):
#     check_res = list([]) 
    
#     point_check = check_imp_STSnums(imp)
#     check_res.append([point_check])
    
#     order_check = check_STSorder(imp)
#     check_res.append(order_check)
    
#     time_check = check_time(imp)
#     check_res.append([time_check])
    
#     xyz_check = check_xyz(imp)
#     check_res.append([xyz_check])
    
#     check_res.append([str(imp[2][1][3])])
    
#     return check_res


# def STSfile_allcheck():
#     folder = choose_folder()
#     paths = os.listdir(folder)
#     point_errs = 0
#     point_arr = list([])
#     order_errs = 0
#     order_arr = list([])
#     time_errs = 0
#     time_arr = list([])
#     err_arr = list([])
#     xyz_errs = 0
#     xyz_arr = list([])
#     for i in paths:
#             imp = import_vp_STS_fix(folder+'/'+i)
#             check_arr = STSfile_check(imp)
#             err_arr.append([check_arr])
#             if check_arr[0][0]==False:
#                 point_errs +=1
#                 point_arr.append(i)
#             if 0 in  check_arr[1][0]:
#                 order_errs +=1
#                 order_arr.append(i)
#             if len(check_arr[2][0])!= 0:
#                 time_errs +=1
#                 time_arr.append(i)
#             if check_arr[3][0]==True:
#                 xyz_errs +=1
#                 xyz_arr.append(i)
#     print('Point Errors: ',point_errs)
#     print(point_arr)
#     print('Order Errors: ',order_errs)
#     print(order_arr)
#     print('Time Errors: ',time_errs)
#     print(time_arr)
#     print('XYZ Errors: ',xyz_errs)
#     print(xyz_arr)
#     return err_arr

def Zmon_check(imp):
    if "Zmon (Å)" in imp[0].columns:
        return imp[0][imp[0]["Zmon (Å)"] != imp[0]["Zmon (Å)"][0]]
    

def Zmon_check_err(folder,paths):
    for i in paths:
        path = folder + i
        imp = import_vp_STS_fix(path)
        fix_time(imp[0])
        check = Zmon_check(imp)
        check.plot.scatter(x = "Time (ms)", y = "Zmon (Å)",sharex=True,c="DarkBlue",s=1)

def Zmon_allcheck(folder = None):
    if folder == None:
        folder = choose_folder()
    paths = os.listdir(folder)
    err_arr = list([])
    zmon_err = 0
    zmon_arr = list([])
    for i in paths:
            imp = import_vp_STS_fix(folder+'/'+i)
            check_arr = Zmon_check(imp)
            err_arr.append([check_arr])
            if len(check_arr["Zmon (Å)"]) != 0:
                   zmon_err +=1
                   zmon_arr.append(i)
                   check_arr.plot.scatter(x = "Time (ms)", y = "Zmon (Å)",c="DarkBlue",s=1)
    print('Zmon Errors: ',zmon_err)
    print(zmon_arr)
    

def STS_plot(folder,paths):
    for i in paths:
        imp = import_vp_STS_fix(folder + '/' + i)
        fix_time(imp[0])
        fig, axes = plt.subplots(nrows=3, ncols=1)
        imp[0].plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
        imp[0].plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
        imp[0].plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)  
        imp[0].plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)


def U_check(imp,V):
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
#%%

#Singles Test 1
#errs = STSfile_allcheck()
#Zmon_allcheck()
U_allcheck(0.51)

# 100 V/s [0,0,0,414] : [point,order,time,xyz] , no Zmon, no U
# 80 V/s [0,0,0,421] : [point,order,time,xyz] , no Zmon, no U
# 60 V/s [0,0,0,417] : [point,order,time,xyz] , no Zmon, no U
# 50 V/s [0,0,0,537] : [point,order,time,xyz] , no Zmon, no U



#%%
path = choose_files()[0]
imp = import_vp_STS_fix(path)
U_err = U_check(imp, 0.5)


#%%
folder = choose_folder()
paths = os.listdir(folder)
STS_plot(folder, paths)

#%%
err_paths_1 = ['STS_dsp-IV-Slope-  100 Vps    _000.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _001.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _002.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _003.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _004.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _005.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _006.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _007.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _008.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _009.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _010.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _011.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _012.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _013.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _015.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _016.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _017.vpdata', 'STS_dsp-IV-Slope-  100 Vps    _018.vpdata']
folder = choose_folder()+'/'
Zmon_check_err(folder,err_paths_1)

print(folder)

#%%


folder = choose_folder()
err_paths_2 = os.listdir(folder)
folder = folder + '/'
Zmon_check_err(folder,err_paths_2)

print(folder)

#%%


folder = choose_folder()
err_paths_3 = os.listdir(folder)
folder = folder + '/'
Zmon_check_err(folder,err_paths_3)

print(folder)


#%% 
Zmon_allcheck()

#%%
folder = 'D:/Work/Stress Test/Test2 - Switch Ramp/'
err_paths = ['STS_set_test_002-VP110-VP.vpdata', 'STS_set_test_002-VP121-VP.vpdata', 'STS_set_test_002-VP126-VP.vpdata', 'STS_set_test_002-VP127-VP.vpdata', 'STS_set_test_002-VP128-VP.vpdata', 'STS_set_test_002-VP129-VP.vpdata', 'STS_set_test_002-VP131-VP.vpdata', 'STS_set_test_002-VP137-VP.vpdata', 'STS_set_test_002-VP177-VP.vpdata', 'STS_set_test_002-VP178-VP.vpdata']
Zmon_check_err(folder,err_paths)

#%%
folder = 'D:/Work/Stress Test/Test2 - Switch Ramp/'
Zmon_allcheck(folder)
z_errs = ['STS_set_test_002-VP110-VP.vpdata', 'STS_set_test_002-VP121-VP.vpdata', 'STS_set_test_002-VP123-VP.vpdata', 'STS_set_test_002-VP129-VP.vpdata', 'STS_set_test_002-VP131-VP.vpdata', 'STS_set_test_002-VP137-VP.vpdata', 'STS_set_test_002-VP177-VP.vpdata', 'STS_set_test_002-VP178-VP.vpdata']
ord_errs = ['STS_set_test_002-VP110-VP.vpdata', 'STS_set_test_002-VP121-VP.vpdata', 'STS_set_test_002-VP126-VP.vpdata', 'STS_set_test_002-VP127-VP.vpdata', 'STS_set_test_002-VP128-VP.vpdata', 'STS_set_test_002-VP129-VP.vpdata', 'STS_set_test_002-VP177-VP.vpdata', 'STS_set_test_002-VP178-VP.vpdata']
point_errs = ['STS_set_test_002-VP110-VP.vpdata', 'STS_set_test_002-VP121-VP.vpdata', 'STS_set_test_002-VP126-VP.vpdata', 'STS_set_test_002-VP127-VP.vpdata', 'STS_set_test_002-VP128-VP.vpdata', 'STS_set_test_002-VP129-VP.vpdata', 'STS_set_test_002-VP131-VP.vpdata', 'STS_set_test_002-VP137-VP.vpdata', 'STS_set_test_002-VP177-VP.vpdata', 'STS_set_test_002-VP178-VP.vpdata']
Time_errs = ['STS_set_test_002-VP110-VP.vpdata', 'STS_set_test_002-VP121-VP.vpdata', 'STS_set_test_002-VP126-VP.vpdata', 'STS_set_test_002-VP127-VP.vpdata', 'STS_set_test_002-VP128-VP.vpdata', 'STS_set_test_002-VP129-VP.vpdata', 'STS_set_test_002-VP131-VP.vpdata', 'STS_set_test_002-VP137-VP.vpdata', 'STS_set_test_002-VP177-VP.vpdata', 'STS_set_test_002-VP178-VP.vpdata']
#%%    
path = 'D:/Work/Stress Test/Test2 - Switch Ramp/STS_set_test_002-VP110-VP.vpdata'
imp1 = import_vp_STS_fix(path)
#aux = STS_import_help(path)
path2 = 'D:/Work/Stress Test/Test2 - Switch Ramp/STS_set_test_002-VP111-VP.vpdata'
imp2 = import_vp_STS_fix(path2)

#%%

check = Zmon_check(imp1)
check.plot.scatter(x = "Time (ms)", y = "Zmon (Å)",sharex=True,c="DarkBlue",s=1)

#%%


imp1_fix = fix_time(imp1[0])

fig, axes = plt.subplots(nrows=3, ncols=1)

imp1_fix.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
imp1_fix.plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
imp1_fix.plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)  
imp1_fix.plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)


imp2_fix = fix_time(imp2[0])
fig, axes = plt.subplots(nrows=3, ncols=1)
imp2_fix.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
imp2_fix.plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
imp2_fix.plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)  
imp2_fix.plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)


#%%
x_start = check_xyz(imp1)


#%%
print(check_imp_STSnums(imp1))
#array_check1 = check_STSorder(imp1) 
array_check1 = STSfile_check(imp1)
time_check1 = check_time(imp1)

#%%
paths = STSfile_allcheck()

#%%
print(check_imp_STSnums(imp2))
#array_check2 = check_STSorder(imp2) 
array_check2 = STSfile_check(imp2)
#VP_list = VP_checklist(aux)
#bla = VP_list["test"]
#na = VP_list[0]

#VP_c1 = VP_test[1][0]



#f =lambda x: re.split("# |  :: VP\[|]=",x[0])

#VP_list = VP_list.apply(f,axis = 1)