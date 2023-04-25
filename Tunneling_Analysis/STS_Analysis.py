# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 21:13:57 2023

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

##############################################################################
##############################################################################


# Analysis of STS Spectra (may involve different kinds of spectroscopies as well) #


##############################################################################
##############################################################################


# reading in STS files from .txt as pandas dataframe (after conversion from VP.data using Import and Convert)
def readin_STS(path = None):
    if path == None:
        path = choose_files()[0]
    else:
        path = path
    file = pd.read_csv(path,header = 0,dtype = {"Frames":int}, index_col = [0,1])
    return file

def read_in_IVmap(path = None):
    if path == None:
        path = choose_files()[0]
    else:
        path = path
    file = pd.read_csv(path,header = 0, index_col = [0])
    return file

# dataframe of first index, all columns
def STS_initial_val(data):
    idx = pd.IndexSlice
    return data.loc[idx[:,0:0],:]

# datafram of choses index, all columns
def STS_get_val(data,index):
    idx = pd.IndexSlice
    return data.loc[idx[:,index:index],:]

# Plotting IV_sets

def STS_plot(imp,**kwargs):
    plt.plot(imp['Bias (V)'],imp["ADC0-I (nA)"], **kwargs)
    
# Averaging and Fitting STS sets

def STS_average(imp):
    idx = pd.IndexSlice
    frame_number = imp.index.get_level_values(0)[-1]
    frame_len = len(imp.loc[idx[1:1,:],'ADC0-I (nA)'])
    biases = imp.loc[idx[1:1,:],'Bias (V)']

    trial = np.array([])
    for i in range(frame_number):
        trial = np.append(trial,imp.loc[idx[i+1:i+1,0:],'ADC0-I (nA)'].to_numpy())
    
    trial = trial.reshape(frame_number,frame_len)
    df = pd.DataFrame(trial)
    med = df.median()
    dev = df.std()
    avg = [med,dev,biases]
    return avg

def STS_logavg(imp):
    idx = pd.IndexSlice
    frame_number = imp.index.get_level_values(0)[-1]
    frame_len = len(imp.loc[idx[1:1,:],'ADC0-I (nA)'])
    biases = imp.loc[idx[1:1,:],'Bias (V)']

    trial = np.array([])
    for i in range(frame_number):
        trial = np.append(trial,imp.loc[idx[i+1:i+1,0:],'ADC0-I (nA)'].to_numpy())
    
    trial = trial.reshape(frame_number,frame_len)
    df = pd.DataFrame(trial)
    med = df.median()
    dev = df.std()
    avg = [med,dev,biases]
    return avg


def STS_splitavg(avg,startpoints = 333, midpoints = 1000):
    med = avg[0]
    dev = avg[1]
    biases = avg[2]
    back = med[startpoints-1:startpoints-1 + midpoints]
    backdev = dev[startpoints-1:startpoints-1 + midpoints]  
    backbiases = biases[startpoints-1:startpoints-1 + midpoints]
    forth = med[startpoints-1 + midpoints:startpoints-1 + 2* midpoints]  
    forthdev = dev[startpoints-1:startpoints-1 + midpoints]
    forthbiases= biases[startpoints-1 + midpoints:startpoints-1 + 2* midpoints]  
    return [[back,backdev,backbiases],[forth,forthdev,forthbiases]]


#def STS_framearrange(imp,colum = "ADC0-I (nA)"):
    #frames = imp['Frames'][:]



# bins data according to binning arrays defined by I's and V's (only current and voltage)

### Obsolete
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

def STS_2D_bin(file,points = [100,1000],params = ["Umon (V)","ADC0-I (nA)"], xrange = [None,None], yrange = [None,None]):
    idx = pd.IndexSlice
    if xrange == [None,None]:
        x_start = file.loc[idx[1:1],:][params[0]].min()
        x_stop = file.loc[idx[1:1],:][params[0]].max()
        xrange = [x_start,x_stop]
        
    if yrange == [None,None]:
        y_start = file[params[1]].min()
        y_stop = file[params[1]].max()
        yrange = [y_start,y_stop]
        
    Xs = np.linspace(xrange[0], xrange[1],points[0])
    Ys = np.linspace(yrange[0], yrange[1],points[1])
    
    Xs_diff = np.divide(np.diff(Xs),2)
    Xs_co = np.add(Xs[:-1],Xs_diff)
    Xs_col = np.subtract(Xs_co,Xs_diff)
    Xs_cor = np.add(Xs_co,Xs_diff)
    
    Ys_diff = np.divide(np.diff(Ys),2)
    Ys_co = np.add(Ys[:-1],Ys_diff)
    Ys_col = np.subtract(Ys_co,Ys_diff)
    Ys_cor = np.add(Ys_co,Ys_diff)
    
    data = copy.deepcopy(file.loc[:,[params[1],params[0]]])
    bin_map = np.empty((len(Ys_co),len(Xs_co)))
    
    for j in range(len(Ys_co)):
        binned = copy.deepcopy(data[(Ys_col[j])<= data[params[1]]])
        binned = binned[binned[params[1]]  < (Ys_cor[j])]
        row = np.empty(len(Xs_co))
        for i in range(len(Xs_co)):
            binbin = copy.deepcopy(binned[Xs_col[i]<= binned[params[0]] ])
            binbin = binbin[binbin[params[0]] < Xs_cor[i]]
            row[i] = len(binbin[params[1]])
            #print(i,j)
        bin_map[j] = row
    return pd.DataFrame(bin_map,index = Ys_co,columns = Xs_co)

def STS_frame_bin(file,points = [None,100],param = 'Zmon (Å)', xrange = [None,None], yrange = [None,None]):
    idx = pd.IndexSlice
    if xrange == [None,None]:
        frames = file.index.get_level_values('Frames').unique()
        x_start = frames[0]
        x_stop = frames[-1]
        xrange = [x_start,x_stop]
        
    if yrange == [None,None]:
        y_start = file[param].min()
        y_stop = file[param].max()
        yrange = [y_start,y_stop]
    
    if points[0] == None:
        points[0] = len(frames)
    Xs = np.linspace(xrange[0], xrange[1],points[0])
    Ys = np.linspace(yrange[0], yrange[1],points[1])
    
    Xs_diff = np.divide(np.diff(Xs),2)
    Xs_co = np.add(Xs[:-1],Xs_diff)
    Xs_col = np.subtract(Xs_co,Xs_diff)
    Xs_cor = np.add(Xs_co,Xs_diff)
    
    Ys_diff = np.divide(np.diff(Ys),2)
    Ys_co = np.add(Ys[:-1],Ys_diff)
    Ys_col = np.subtract(Ys_co,Ys_diff)
    Ys_cor = np.add(Ys_co,Ys_diff)
    
    data = copy.deepcopy(file.loc[:,[param]])
    bin_map = np.empty((len(Xs_co),len(Ys_co)))
    for j in range(len(Xs_co)):
        binbin = copy.deepcopy(data)
        frame = frames[frames >= Xs_col[j]]
        frame = frame[frame <Xs_cor[j]]
        framel = frame[0]
        framer = frame[-1]
        binbin = data.loc[idx[framel:framer,:],:]
        row = np.empty(len(Ys_co))
        for i in range(len(Ys_co)):
            binned = copy.deepcopy(binbin[(Ys_col[i])<= data[param]])
            binned = binned[binned[param]  < (Ys_cor[i])]
            row[i] = len(binned[param])
            #print(i,j)
        bin_map[j] = row
    return pd.DataFrame(bin_map,index = Xs_co,columns = Ys_co).transpose()


# makes an array with the centers of the binning arrays
def get_centers(xs,ys):
    x_diff = np.diff(xs)
    y_diff = np.diff(ys)
    xs = np.add(xs[:-1],np.divide(x_diff,2))
    ys = np.add(ys[:-1],np.divide(y_diff,2))
    return list([xs,ys])

# returns binned data as pandas dataframe ()
# def convert_bin_sSTSset(file,binx,biny):    ### OBSOLETE
#     Vs = np.linspace(-binx[0],binx[0],binx[1])
#     Is = np.linspace(-biny[0],biny[0],biny[1])
#     x_co,y_co = get_centers(Vs, Is)
#     binned = STS_2D_bin(Vs,Is,file)
    
#     return pd.DataFrame(binned,index = y_co,columns = x_co)

def convert_bin_sSTSset(file,params = ["Umon (V)","ADC0-I (nA)"],**kwargs):
    if params[0] == 'Frames':
        binned = STS_frame_bin(file,param = params[1],**kwargs)
    else:
        binned = STS_2D_bin(file,params = params,**kwargs)
    return binned


# finds all STS imports in folder and bins them into IV-map according to bin array x and y,
# saves data as .txt
# def bin_all_sSTSset(binx,biny,folder = None): ###OBSOLETE
#     if folder == None:
#         folder = choose_folder()
#     else:
#         folder = folder
#     files = os.listdir(folder)
#     for i in files:
#         print(i)
#         if 'import' in i:
#             path = os.path.join(folder,i)
#             newpath = path.replace('import','bin')
#             file = readin_STS(path)
#             binned = convert_bin_sSTSset(file,binx,biny)
#             vp_to_csv_index(binned,newpath = newpath)

def bin_all_sSTSset(folder = None, params = ["Umon (V)","ADC0-I (nA)"],equal_range = False, **kwargs):
    Types = {'ADC0-I (nA)':'I','Zmon (Å)':'Z', 'Umon (V)':'Vm', 'Time (ms)':'T','Bias (V)':'V','LockIn A-1st (dV)':'dIdV','LockIn B-1st (dV)':'dIdV_B','LockIn A-2nd (ddV)':'dIddV','LockIn B-2nd (ddV)':'dIddV_B','LockIn0 (V)':'Lock_0','Frames':'F'}
    name = Types[params[1]] + Types[params[0]] + 'bin'
    if folder == None:
        folder = choose_folder()
    else:
        folder = folder
    files = os.listdir(folder)
    if equal_range == False:
        for i in files:
            print(i)
            if 'import' in i:
                        path = os.path.join(folder,i)
                        newpath = path.replace('import',name)
                        file = readin_STS(path)
                        binned = convert_bin_sSTSset(file,params,**kwargs)
                        vp_to_csv_index(binned,newpath = newpath)
    else:
        imports = list([])
        maxs = list([])
        mins = list([])
        newpaths = list([])
        for i in files:         
           if 'import' in i:
                    print(i)
                    path = os.path.join(folder,i)
                    newpaths.append(path.replace('import',name))
                    file = readin_STS(path)
                    imports.append(file)
                    maxs.append(file[params[1]].max())
                    mins.append(file[params[1]].min())
           else:
               continue
        yrange = [min(mins),max(maxs)]         
        for j in range(len(imports)):
                   print(j)
                   binned = convert_bin_sSTSset(imports[j],params,yrange = yrange,**kwargs)
                   vp_to_csv_index(binned,newpath = newpaths[j])
           
def IVmap_normalize(IV_map):
    IV_sums = IV_map.iloc[:][:].sum()
    IV_normalized= IV_map[:][:]/IV_sums[:]
    return IV_normalized


def plot_IVmap(IV_map, xrange = 'auto' , yrange = 'auto', aspect = None, log = True, logmod = 1,nozeros = False):
    IV_map = copy.deepcopy(IV_map.iloc[::-1])
    if yrange == 'auto':
        y_start = IV_map.index.astype('float').min()
        y_stop = IV_map.index.astype('float').max()
        yrange = [y_start,y_stop]
    if xrange == 'auto':
        x_start = IV_map.columns.astype('float').min()
        x_stop = IV_map.columns.astype('float').max()
        xrange = [x_start,x_stop]
    if nozeros == True:
        IV_map[IV_map == 0] = np.nan
    if aspect == None:
        aspect = abs(xrange[1]-xrange[0])/abs(yrange[1] - yrange[0])
    if log == True:
        IV_map = IV_map * logmod + 1
        plt.imshow(IV_map,cmap=plt.cm.inferno,
                    interpolation=None,extent=[xrange[0],xrange[1],yrange[0],yrange[1]],aspect = aspect, norm = colors.LogNorm(vmin=IV_map.min().min(), vmax=IV_map.max().max()))
    else:
        plt.imshow(IV_map,cmap=plt.cm.inferno, extent=[xrange[0],xrange[1],yrange[0],yrange[1]],aspect = aspect)

    
def plot_IVmaps(paths = None,**kwargs):
    if paths == None:
        paths = choose_files()
    else:
        paths = paths
    for i in paths:
        IV_map = read_in_IVmap(i)
        im  = plot_IVmap(IV_map,**kwargs)
        plt.colorbar(im)
        plt.title(str(i))
        plt.show()

def plot_IVmap_3D(IV_map, xrange = 'auto', yrange = 'auto',xlim = [None, None],ylim =[None,None],zlim = [None,None],nozeros = False,cmap = 'inferno',
                      lw = 1, rstride = 1, cstride =1,**kwargs):
    IV_map = copy.deepcopy(IV_map.iloc[::-1])
    X,Y = np.meshgrid(IV_map.columns.astype('float'),IV_map.index.astype('float'))
    Z = IV_map
    if xrange == 'auto':
        xrange = (IV_map.index.astype('float').min(),IV_map.index.astype('float').max())
    if yrange == 'auto':
        yrange = IV_map.columns.astype('float').min(),IV_map.columns.astype('float').max()
        
    if xlim != [None,None]:
        X[X<xlim[0]] = np.nan
        X[X>xlim[1]] = np.nan
        #xlim[0] = xrange[0]
        #xlim[0] = xrange[1]
    if ylim != [None,None]:
        Y[Y<ylim[0]] = np.nan
        Y[Y>ylim[1]] = np.nan
        #ylim[0] = yrange[0]
        #ylim[0] = yrange[1]
    if zlim != [None,None]:
        Z[Z<zlim[0]] = np.nan
        Z[Z>zlim[1]] = np.nan
    if nozeros == True:
        Z[Z == 0] = np.nan
    ax = plt.figure().add_subplot(1,1,1,projection='3d')
    ax.plot_surface(X, Y,Z, edgecolor='None', lw=lw, rstride=rstride, cstride=cstride,cmap=cmap,**kwargs)
    ax.set(xlim=xlim, ylim=ylim,
           xlabel='X', ylabel='Y', zlabel='Z')

def plot_IVmap_wireframe(IV_map, xrange = 'auto', yrange = 'auto',xlim = [None, None],ylim =[None,None],zlim = [None,None],nozeros = False,cmap = 'inferno',
                      lw = 0.1, rstride = 1, cstride =1,**kwargs):
    IV_map = copy.deepcopy(IV_map.iloc[::-1])
    X,Y = np.meshgrid(IV_map.columns.astype('float'),IV_map.index.astype('float'))
    Z = IV_map
    if xrange == 'auto':
        xrange = (IV_map.index.astype('float').min(),IV_map.index.astype('float').max())
    if yrange == 'auto':
        yrange = IV_map.columns.astype('float').min(),IV_map.columns.astype('float').max()
        
    if xlim != [None,None]:
        X[X<xlim[0]] = np.nan
        X[X>xlim[1]] = np.nan
        #xlim[0] = xrange[0]
        #xlim[0] = xrange[1]
    if ylim != [None,None]:
        Y[Y<ylim[0]] = np.nan
        Y[Y>ylim[1]] = np.nan
        #ylim[0] = yrange[0]
        #ylim[0] = yrange[1]
    if zlim != [None,None]:
        Z[Z<zlim[0]] = np.nan
        Z[Z>zlim[1]] = np.nan
    if nozeros == True:
        Z[Z == 0] = np.nan
    ax = plt.figure().add_subplot(1,1,1,projection='3d')
    ax.plot_wireframe(X, Y,Z, lw=lw, rstride=rstride, cstride=cstride,**kwargs)
    ax.set(xlim=xlim, ylim=ylim,
           xlabel='X', ylabel='Y', zlabel='Z')
    
#def plot_imp_wireframe(imp,x_name,y_name):
    