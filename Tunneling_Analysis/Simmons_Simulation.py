# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 20:36:00 2023

@author: Norman
"""
import scipy.constants as c
import numpy as np
import matplotlib.pyplot as plt

#scipy.constants.physical_constants
#Dictionary of physical constants, of the format physical_constants[name] = (value, unit, uncertainty)

class Tip:
    base_x = []
    base_y = []
    base_order = None
    
    shape = []
    
    
    def __init__(self):
        self.shape = []
    
    def base(self,extent,mesh_length,order):
        arr = np.linspace(-extent,extent,mesh_length) * 10**(order)
        self.base_x, self.base_y = np.meshgrid(arr,arr)
        self.base_order = 10**(order)
        
    # def shape_parab(radius,order):
            
        
#tip = Tip()
#tip.base(3,31,-9)
#%%
def Phi_bar(Phi_l,Phi_r):
    return (Phi_l + Phi_r)/2
    
def m_Phi(Phi_l,Phi_r):
    return (Phi_r - Phi_l)

def beta_(Phi_l,Phi_r):
    return (1-1/(8*  Phi_bar(Phi_l,Phi_r)**2) * ((Phi_l - Phi_bar(Phi_l, Phi_r))**2
                                                + m_Phi(Phi_l, Phi_r)*(Phi_l - Phi_bar(Phi_l, Phi_r)) + 1/3 * m_Phi(Phi_l, Phi_r)**2))


Phi_l = 1 * c.physical_constants['electron volt'][0]
Phi_r = 1 * c.physical_constants['electron volt'][0]
d = 1.5 * 10**(-9)
ds = np.linspace(0.5,2.5,40)
ds = ds *10**(-9)

           
def alpha_(beta):
    return(c.e/(4*(c.pi**2)*(beta**2)*c.hbar))

def A_(beta):
    return 2*beta*np.sqrt(c.m_e/c.hbar**2)


def J_(d,V,Phi_l,Phi_r):
    if d == np.nan:
        return np.nan
    P = Phi_bar(Phi_l, Phi_r)
    beta = beta_(Phi_l,Phi_r)
    alpha = alpha_(beta)
    A = A_(beta)
    V = V *c.physical_constants['electron volt'][0]
    
    
    return (alpha/d**2 * ((P-V/2)*np.exp(-A*d*np.sqrt(P-V/2))- (P+V/2)*np.exp(-A*d*np.sqrt(P+V/2))))
    
simm = np.vectorize(J_)
Vs = np.linspace(-0.5,0.5,num =10)

for i in ds:
    test = simm(d = i, V= Vs,Phi_l = Phi_l,Phi_r = Phi_r)

    plt.plot(Vs,test)


x_arr = np.linspace(-30,30,211)
y_arr = np.linspace(-30,30,211)

pixel_area = np.diff(x_arr)[0]*10**(-9)*np.diff(y_arr)[0]*10**(-9)


x_tip, y_tip = np.meshgrid(x_arr,y_arr)

z = (x_tip**2 + y_tip**2)/9 * 0.3 *10**(-9)
z[z>5*10**(-9)] = np.nan

ax = plt.figure().add_subplot(1,1,1,projection='3d')
ax.plot_surface(x_tip*10**(-9),y_tip*10**(-9),z, edgecolor='None', lw=1, rstride=1, cstride=1,cmap='inferno')
ax.set(xlabel='X in nm', ylabel='Y in nm', zlabel='Z in m')
plt.show()

def I_(d,tip,pixel_area,V,Phi_l,Phi_r):
    tip = tip + d
    I_map = simm(tip, V, Phi_l, Phi_r)*pixel_area
    return (np.nansum(I_map))
#%%
Phis = np.linspace(1,7,15)*c.physical_constants['electron volt'][0]

for l in Phis:
    for j in ds:
        IV = list([])
        for i in Vs:
            IV.append(I_(j,z,pixel_area,i,Phi_l=l,Phi_r=l))
        plt.plot(Vs,IV)
        plt.ylim((-8*10**(-9),8*10**(-9)))
    
        plt.title('Phi= '+ str(l/c.physical_constants['electron volt'][0])+', '+'IV')
    plt.show()
    
#%%

from mpl_toolkits.mplot3d import axes3d
from IPython import get_ipython
from matplotlib.pyplot import figure

#
#get_ipython().run_line_magic('matplotlib', 'qt')
get_ipython().run_line_magic('matplotlib', 'inline')

x_arr = np.linspace(-10,10,41)
y_arr = np.linspace(-10,10,41)


cal = 1.5 * 10**(-10)
calx = cal/np.sqrt(2)

pixel_area = np.diff(x_arr)[0]*calx*np.diff(y_arr)[0]*calx*1
x_tip, y_tip = np.meshgrid(x_arr,y_arr)
ass =0 *c.physical_constants['electron volt'][0]

#z = (x_tip**2 + y_tip**2)*cal
z = np.rint(((x_tip)**2+ (y_tip)**2)/1)*cal*10
z[z>10*10**(-9)] = np.nan


x_tip, y_tip = np.meshgrid(x_arr,y_arr)
ax = plt.figure().add_subplot(1,1,1,projection='3d')
ax.plot_surface(x_tip*calx,y_tip*calx,z, edgecolor='None', lw=1, rstride=1, cstride=1,cmap='inferno')
ax.set(xlabel='X in m', ylabel='Y in m', zlabel='Z in m',xlim = (-10*10**(-9),10*10**(-9)),ylim = (-10*10**(-9),10*10**(-9)))
plt.show()

Phis = [5* c.physical_constants['electron volt'][0]]
ds = np.linspace(0.7,2,41)
ds = ds *10**(-9)
Vs = np.linspace(-0.5,0.5,num =21)
get_ipython().run_line_magic('matplotlib', 'qt')
for l in Phis:
    for j in ds:
        IV = list([])
        for i in Vs:
            IV.append(10*I_(j,z,pixel_area,i,Phi_l=l,Phi_r=l+ass))
        plt.plot(Vs,IV)
        plt.ylim((-8*10**(-9),8*10**(-9)))
    
        plt.title('Phi= '+ str(l/c.physical_constants['electron volt'][0])+', '+'IV')
   
    
    plt.show()