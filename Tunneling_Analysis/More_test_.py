# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:21:42 2023

@author: Norman
"""
#D:\Work\GitHub\Tunneling-Analysis\Tunneling_Analysis
#jupyter notebook --notebook-dir=D:\Work\GitHub\Tunneling-Analysis\Tunneling_Analysis\
#jupyter notebook --notebook-dir=D:\Work\2023_03_23 EQT42vs43\Spot6\ 
#IZ : 

from Import import *
#from Import import import_vp_STS_fix
from Convert import *
from STS_Analysis import *


from tkinter import Tk, filedialog
import os
import pandas as pd
import re
import copy
import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

dir_path = os.path.dirname(os.path.realpath(__file__))



path = choose_files()[0]
file = STS_import_help(path)
print(file)
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
    

# def STS_plot(folder,paths):
#     for i in paths:
#         imp = import_vp_STS_fix(folder + '/' + i)
#         fix_time(imp[0])
#         fig, axes = plt.subplots(nrows=3, ncols=1)
#         imp[0].plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
#         imp[0].plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
#         imp[0].plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)  
#         imp[0].plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)


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

def STS_initial_val(data):
    idx = pd.IndexSlice
    return data.loc[idx[:,0:0],:]

def bin_it(co,diff,x):
    return None

# def STS_2D_bin(Vs,Is,data):
#     Vs_diff = np.divide(np.diff(Vs),2)
#     Is_diff = np.divide(np.diff(Is),2)
#     Vs_co = np.add(Vs[:-1],Vs_diff)
#     Is_co = np.add(Is[:-1],Is_diff)
#     data = data.loc[:,["ADC0-I (nA)","Umon (V)"]]
#     print(data)
#     IV_map = np.empty((len(Is_co),len(Vs_co)))
#     for j in range(len(Is_co)):
#         binned = copy.deepcopy(data[(Is_co[j] - Is_diff[j])<= data["ADC0-I (nA)"]])
#         binned = binned[binned["ADC0-I (nA)"]  < (Is_co[j] + Is_diff[j])]
#         row = np.empty(len(Vs_co))
#         for i in range(len(Vs_co)):
#             binbin = copy.deepcopy(binned[(Vs_co[i] - Vs_diff[i])<= binned["Umon (V)"] ])
#             binbin = binbin[binbin["Umon (V)"] < (Vs_co[i] + Vs_diff[i])]
#             #IV_map[j][i] = len(binned["ADC0-I (nA)"])
#             row[i] = len(binbin["ADC0-I (nA)"])
#             print(i,j)
#         IV_map[j] = row
#     return IV_map
#     # bin_ij = data.loc[]

#(Vs_co[i] - Vs_diff[i]<= data["Umon (V)"] < Vs_co[i] - Vs_diff[i]) 
def get_centers(xs,ys):
    x_diff = np.diff(xs)
    y_diff = np.diff(ys)
    xs = np.add(xs[:-1],np.divide(x_diff,2))
    ys = np.add(ys[:-1],np.divide(y_diff,2))
    return list([xs,ys])

def convert_bin_sSTSset(file,binx,biny):
    Vs = np.linspace(-binx[0],binx[0],binx[1])
    Is = np.linspace(-biny[0],biny[0],biny[1])
    x_co,y_co = get_centers(Vs, Is)
    binned = STS_2D_bin(Vs,Is,file)
    
    return pd.DataFrame(binned,index = y_co,columns = x_co)

# def readin_STS(path = None):
#     if path == None:
#         path = choose_files()[0]
#     else:
#         path = path
#     file = pd.read_csv(path,header = 0,dtype = {"Frames":str}, index_col = [0,1])
#     return file   


def bin_all_sSTSset(binx,biny,folder = None,):
    if folder == None:
        folder = choose_folder()
    else:
        folder = folder
    files = os.listdir(folder)
    for i in files:
        print(i)
        if 'import' in i:
            path = os.path.join(folder,i)
            newpath = path.replace('import','bin')
            file = readin_STS(path)
            binned = convert_bin_sSTSset(file,binx,biny)
            vp_to_csv_index(binned,newpath = newpath)

# def STS_2D_bin(Vs,Is,data):
#     Vs_diff = np.divide(np.diff(Vs),2)
#     Is_diff = np.divide(np.diff(Is),2)
#     Vs_co = np.add(Vs[:-1],Vs_diff)
#     Is_co = np.add(Is[:-1],Is_diff)
#     data = data.loc[:,["ADC0-I (nA)","Umon (V)"]]
#     print(data)
#     IV_map = np.empty((len(Is_co),len(Vs_co)))
#     for j in range(len(Is_co)):
#         binned = copy.deepcopy(data[(Is_co[j] - Is_diff[j])<= data["ADC0-I (nA)"]])
#         binned = binned[binned["ADC0-I (nA)"]  < (Is_co[j] + Is_diff[j])]
#         row = np.empty(len(Vs_co))
#         for i in range(len(Vs_co)):
#             binbin = copy.deepcopy(binned[(Vs_co[i] - Vs_diff[i])<= binned["Umon (V)"] ])
#             binbin = binbin[binbin["Umon (V)"] < (Vs_co[i] + Vs_diff[i])]
#             #IV_map[j][i] = len(binned["ADC0-I (nA)"])
#             row[i] = len(binbin["ADC0-I (nA)"])
#             print(i,j)
#         IV_map[j] = row
#     return IV_map


#%%
#path = choose_files()[0]
imp = readin_STS(path)
STS_plot(imp)
plt.show()

#%%



back,forth = STS_split(imp,333,1000)
STS_plot(back,'bo',markersize = 0.1)
STS_plot(forth,'bo',markersize = 0.1)

#%%




#%%

#bg_path = choose_files()[0]
bg = readin_STS(bg_path)
# STS_plot(bg)
# plt.show()

bg_back,bg_forth = STS_split(bg,333,1000)
STS_plot(bg_back,'bo',markersize = 0.1)
STS_plot(bg_forth,'bo',markersize = 0.1)

bg_avgb = STS_average(bg_back)
plt.plot(bg_avgb[2],bg_avgb[0],'r--')
bg_avgf = STS_average(bg_forth)
plt.plot(bg_avgf[2],bg_avgf[0],'r--')

#%%

back['ADC0-I (nA)'] ,forth['ADC0-I (nA)']  = back['ADC0-I (nA)']- bg_avgb[0],forth['ADC0-I (nA)']-bg_avgf[0]

#%%

STS_plot(back,'bo',markersize = 0.1)
STS_plot(forth,'bo',markersize = 0.1)

#%%

imp_max = imp['ADC0-I (nA)'].max()
imp_min = imp['ADC0-I (nA)'].min()

min_biases = imp['Bias (V)'][imp['ADC0-I (nA)'] == imp_min]
min_bias = min_biases.max()
max_biases = imp['Bias (V)'][imp['ADC0-I (nA)'] == imp_max]
max_bias = max_biases.min()

crop = imp[imp['Bias (V)']<max_bias]
crop = crop[imp['Bias (V)']>min_bias]
#%%
STS_plot(crop,'bo',markersize = 0.1)
plt.show()
#%%
avg = STS_average(crop)
plt.plot(avg[2],avg[0])

#%%

print(file.columns)
#%%
test_file = readin_STS()
bin_map = STS_2D_bin(test_file,points = [100,100])
plot_IVmap(bin_map)

#%%
test_file = readin_STS()
bin_map = STS_2D_bin(test_file,points = [100,100],params=['Time (ms)','ADC0-I (nA)'])
plot_IVmap(bin_map)

#%%
test_file = readin_STS()
bin_map = STS_frame_bin(test_file,points = [None,100])
#%%
plot_IVmap(bin_map,log = False)
#%%
idx = pd.IndexSlice
params=['Time (ms)','ADC0-I (nA)']

bla = test_file.loc[idx[1:1],:][params[0]].max()

#%%
idx = pd.IndexSlice
ind = file.loc[idx[40:100,10:100],:]

frames = file.index.get_level_values('Frames').unique()
frames = frames[frames < 6]
#%%
idx = pd.IndexSlice
ind = file.loc[idx[40:100,10:100],:]

frames = file.index.get_level_values('Frames').unique()
frame_num = len(frames)
data_num = len(file.loc[idx[1:1],:]['Umon (V)'])
Is = copy.deepcopy(file['ADC0-I (nA)']).to_numpy()
Is = np.reshape(Is, (frame_num,data_num)).transpose()
Zs = copy.deepcopy(file['Zmon (Å)']).to_numpy()
Zs = np.reshape(Zs, (frame_num,data_num)).transpose()
print(file.columns)
print(Is)
param  = 'ADC0-I (nA)'
#Fs,Ts = np.meshgrid(file.loc[idx[1:1],:]['Umon (V)'],file.loc[idx[1:1],:]['Time (ms)'])
Fs,Ts = np.meshgrid(frames,file.loc[idx[1:1],:]['Time (ms)'])
Fs,Vs = np.meshgrid(frames,file.loc[idx[1:1],:]['Umon (V)'])

ax = plt.figure().add_subplot(1,1,1,projection='3d')
ax.plot_wireframe(Fs, Vs, Is, rstride=0, cstride=1,lw=0.1)
plt.show()

ax = plt.figure().add_subplot(1,1,1,projection='3d')
ax.plot_wireframe(Fs, Ts, Is, rstride=0, cstride=1,lw=0.1)
plt.show()

ax = plt.figure().add_subplot(1,1,1,projection='3d')
ax.plot_wireframe(Fs, Ts, Zs, rstride=10, cstride=0,lw=0.1)
plt.show()
#%%
#IV_map = read_in_IVmap()

plot_IVmap(IV_normalized, logmod = 1,nozeros = 'False')
#plt.ylim(-3,3)
#%%
#xrange = IV_map.index.astype('float').max()
#yrange = IV_map.columns.astype('float').max()

#plot_IVmap_3D(IV_normalized,xlim = [-0.2,0.2],ylim = [-0.5,0.5],nozeros = True)
plot_IVmap_wireframe(IV_normalized,lw = 0.4,xlim = [-0.1,0.1],ylim = [-0.5,0.5],rstride = 0)
#%%
from mpl_toolkits.mplot3d import axes3d
from IPython import get_ipython

#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt')



X, Y, Z = axes3d.get_test_data(0.05)
ax = plt.figure().add_subplot(1,1,1,projection='3d')

Vs = np.linspace(-0.5, 0.5,100)
Is = np.linspace(-10,10,1000)
x_co,y_co = get_centers(Vs, Is)
X2, Y2 = np.meshgrid(x_co,y_co)

Z2 = IV_normalized.to_numpy()

#ax.plot_surface(X2, Y2, Z2, edgecolor='None', lw=1, rstride=1, cstride=1,
                #alpha=1,cmap='inferno',antialiased=True)
Y2[Y2>3] = np.nan
Y2[Y2<-3] = np.nan
Z2[Z2 == 0] = np.nan
#ax.plot_wireframe(X2, Y2, Z2, rstride=0, cstride=1,lw=0.3)
ax.plot_surface(X2, Y2,Z2, edgecolor='None', lw=1, rstride=1, cstride=1,
                alpha=1,cmap='inferno',antialiased=True)

#ax.contour(X2, Y2, Z2, zdir='z', offset=-1, cmap=plt.cm.coolwarm)
#cset = ax.contour(X2, Y2, Z2, zdir='x', offset=-1, cmap=plt.cm.coolwarm)
#cset = ax.contour(X2, Y2, Z2, zdir='y', offset=5, cmap=plt.cm.coolwarm)
#ax.imshow(IV_normalized,cmap = 'inferno', extent = [-0.5,0.5,-3,3],aspect = 'auto')

ax.set(xlim=(-0.5, 0.5), ylim=(-3, 3),
       xlabel='X', ylabel='Y', zlabel='Z')

# ax.set_xlim3d(-1, 2*1);
# ax.set_ylim3d(0, 3*1);
# ax.set_zlim3d(-1, 2*1);


#%%
IV_map2 = IV_map.iloc[::-1]
IV_sums = IV_map.iloc[:][:].sum()
IV_normalized= IV_map[:][:]/IV_sums[:]

print( IV_normalized.min().min())
print( IV_normalized.max().max())
#%%
plot_IVmap(IV_normalized)
colums = IV_normalized.columns
col_ = colums[0]
col16 = IV_normalized.iloc[:][colums[16]]
plt.plot(col16.index.astype('float'),col16)
#%%
binx = [0.5,100]
biny = [10,1000]
bin_all_sSTSset(binx,biny)

#%%
path = choose_files()[0]
file2 = pd.read_csv(path,header = 0,dtype = {"Frames":str}, index_col = [0,1])
file = pd.read_csv(path,header = 0, index_col = [0,1])
#%%

folder = choose_folder()
subs = subfolders(folder)

for i in range(len(subs)):
    name = 'STS_1Vps_import_' + str(i)
    convert_sSTSset(folder = subs[i],name = name)
    
    
    
#%%
paths = make_folder_paths()
print(paths)

#%%

Stest_3 = STS_combine_all(subfldrs=True)

#%%
newpath = 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3'
newpath = newpath + '/'+'STS_100Vs_import_all.txt'
vp_to_csv_index(Stest_3,newpath = newpath)

#%%
Vs = np.linspace(-0.5, 0.5,100)
Is = np.linspace(-10,10,1000)
x_co,y_co = get_centers(Vs, Is)
bin_test4 = STS_2D_bin(Vs, Is, Stest_3)
bin_df4 = pd.DataFrame(bin_test4,index = y_co,columns = x_co)
newpath = 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3'
newpath = newpath + '/'+'STS_100Vs_bin_all.txt'
vp_to_csv_index(bin_df4,newpath = newpath)


#%%

df_4 = STS_combine_all()

Vs = np.linspace(-0.5, 0.5,100)
Is = np.linspace(-10,10,1000)
grid = np.meshgrid(Vs,Is)

x_co,y_co = get_centers(Vs, Is)

newpath = 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3'
print(newpath)
newpath = newpath + '/'+'STS_100Vs_import_9.txt'

vp_to_csv_index(df_4,newpath = newpath)

bin_test4 = STS_2D_bin(Vs, Is, df_4)

bin_df4 = pd.DataFrame(bin_test4,index = y_co,columns = x_co)
#newpath = choose_folder()
newpath = 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3'
newpath = newpath + '/'+'STS_100Vs_bin_9.txt'

vp_to_csv_index(bin_df4,newpath = newpath)
#%%
flip = np.flipud(bin_test4)


im = plt.imshow(np.flipud(np.add(bin_test4,2)), cmap=plt.cm.inferno,
                interpolation=None,extent=[-0.5,0.5,-10,10],aspect = 0.05, norm = colors.LogNorm(vmin=1, vmax=bin_test4.max()))

plt.colorbar(im)
plt.title('All')
#plt.ylim((-3,3))
#plt.yscale('log')
plt.show()

#%%
hist = np.sum(flip,axis = 1)

plt.plot(y_co,hist)
plt.show()


flip1 = np.flipud(np.multiply(bin_test4,y_co[:,np.newaxis]))

histx = np.sum(flip,axis = 0)

plt.plot(x_co,histx)
plt.show()
#%%
df_2 = STS_combine_all()

#%%
#newpath = choose_folder()
newpath = 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3'
print(newpath)
newpath = newpath + '/'+'STS_100Vs_import_1.txt'

vp_to_csv_index(df_2,newpath = newpath)

#%%

Vs = np.linspace(-0.5, 0.5,100)
Is = np.linspace(-10,10,1000)
grid = np.meshgrid(Vs,Is)

#V_diff = np.diff(Vs)
#I_diff = np.diff(Is)

x_co,y_co = get_centers(Vs, Is)

bin_test1 = STS_2D_bin(Vs, Is, df_2)

#%%

bin_df1 = pd.DataFrame(bin_test3,index = y_co,columns = x_co)
#newpath = choose_folder()
newpath = 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3'
newpath = newpath + '/'+'STS_100Vs_bin_1.txt'

vp_to_csv_index(bin_df1,newpath = newpath)

#%%
Vs = np.linspace(-0.5, 0.5,100)
Is = np.linspace(-10,10,1000)
grid = np.meshgrid(Vs,Is)

#V_diff = np.diff(Vs)
#I_diff = np.diff(Is)

x_co,y_co = get_centers(Vs, Is)

bin_test2 = STS_2D_bin(Vs, Is, df)

#%%

flip = np.flipud(bin_test2)

im = plt.imshow(np.flipud(np.add(bin_test3,2)), cmap=plt.cm.inferno,
                interpolation=None,extent=[-0.5,0.5,-10,10],aspect = 0.05, norm = colors.LogNorm(vmin=1, vmax=bin_test2.max()))

plt.colorbar(im)
plt.title('Letsee2')
plt.show()
#%%

bin_df = pd.DataFrame(bin_test3,index = y_co,columns = x_co)
#newpath = choose_folder()
newpath = 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3'
newpath = newpath + '/'+'STS_100Vs_bin_1.txt'

vp_to_csv_index(bin_df,newpath = newpath)

#%%
flip = np.flipud(bin_test2)

im = plt.imshow(np.flipud(np.add(bin_test2,2)), cmap=plt.cm.inferno,
                interpolation=None,extent=[-0.5,0.5,-10,10],aspect = 0.05, norm = colors.LogNorm(vmin=1, vmax=bin_test2.max()))

plt.colorbar(im)
plt.title('Letsee')
plt.show()
#%%
#paths = choose_files()
paths = ('D:/Work/Stress Test/Advanced_Test/Singles_Test_3/STS_Singles_0_dsp-IV-Slope-  100 Vps    _dsp-IV-rep-  1      _dsp-fbs-bias- 0p2 V    _dsp-fbs-mx0-current-set-   1 nA    _/STS_dsp-IV-Slope-  100 Vps    _000.vpdata', 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3/STS_Singles_0_dsp-IV-Slope-  100 Vps    _dsp-IV-rep-  1      _dsp-fbs-bias- 0p2 V    _dsp-fbs-mx0-current-set-   1 nA    _/STS_dsp-IV-Slope-  100 Vps    _001.vpdata', 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3/STS_Singles_0_dsp-IV-Slope-  100 Vps    _dsp-IV-rep-  1      _dsp-fbs-bias- 0p2 V    _dsp-fbs-mx0-current-set-   1 nA    _/STS_dsp-IV-Slope-  100 Vps    _002.vpdata', 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3/STS_Singles_0_dsp-IV-Slope-  100 Vps    _dsp-IV-rep-  1      _dsp-fbs-bias- 0p2 V    _dsp-fbs-mx0-current-set-   1 nA    _/STS_dsp-IV-Slope-  100 Vps    _003.vpdata', 'D:/Work/Stress Test/Advanced_Test/Singles_Test_3/STS_Singles_0_dsp-IV-Slope-  100 Vps    _dsp-IV-rep-  1      _dsp-fbs-bias- 0p2 V    _dsp-fbs-mx0-current-set-   1 nA    _/STS_dsp-IV-Slope-  100 Vps    _004.vpdata')
print(paths)
df = STS_combine_all()
#names = STS_sframes(len(paths),3)

#%%
newpath = choose_folder()
print(newpath)
newpath = newpath + '/'+'STS_100Vs_import_0.txt'

vp_to_csv_index(df,newpath = newpath)
#%%
fig, axes = plt.subplots(nrows=3, ncols=1)

df.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
df.plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
df.plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)  
df.plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)

#%%

df_no = df[abs(df["ADC0-I (nA)"])<10]
fig, axes = plt.subplots(nrows=3, ncols=1)


df_no.plot.scatter(x = "Time (ms)", y = "ADC0-I (nA)", ax=axes[0],sharex=True,c="DarkBlue",s=0.1)
df_no.plot.scatter(x = "Time (ms)", y = "Zmon (Å)", ax=axes[1],sharex=True,c="DarkBlue",s=0.1)
df_no.plot.scatter(x = "Time (ms)", y = "Umon (V)", ax=axes[2],sharex=True,c="DarkBlue",s=0.1)  
df_no.plot.scatter(x = "Umon (V)", y = "ADC0-I (nA)",c="DarkBlue",s=0.1)



#%%
init = STS_initial_val(df)
init_nooverload = init[abs(init["ADC0-I (nA)"])<10]

xs = np.linspace(1, len(init_nooverload.index),num = len(init_nooverload.index))
plt.plot(xs,init_nooverload["ADC0-I (nA)"]*1000)
plt.plot(xs,init_nooverload["Zmon (Å)"])
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
pd.options.mode.chained_assignment = None
#errs = STSfile_allcheck()
# path = choose_files()[0]
# imp = import_vp_STS_fix(path)
# err = STSfile_check(imp)

folders = subfolders()
for i in folders:
    print(i)
    #STSfile_allcheck(i)
    Zmon_allcheck(i)
#all look good in allcheck
# all look good in Zmon check
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

space = np.linspace(0.01,0.5, 50)
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