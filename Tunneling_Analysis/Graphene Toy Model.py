# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 21:28:06 2023

@author: Norman
"""
import scipy.constants as c
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

def D_2d(E,E_f):
    out = 2*abs(E+E_f)/(c.pi * c.hbar**2*(1*10**6)**2)
    return out

def eV_(E):
    return np.multiply(E,c.electron_volt)

def f_0(E,T=0):
    if T == 0:
        if E <= 0:
            return 1
        else:
            return 0
    else:
        exponent = np.divide(E,(c.Boltzmann*T))
        divisor = np.exp(exponent) + 1
        return np.divide(1,divisor)
        
        
        
D_2D = np.vectorize(D_2d)

F_0 = np.vectorize(f_0)

def overlap(E,E_f,V,T=0):
    g1 = D_2d(E-eV_(V)/2,eV_(E_f))
    F1 = F_0(E-eV_(V)/2,T)
    
    g2 = D_2d(E+eV_(V)/2,eV_(E_f))
    F2 = F_0(E+eV_(V)/2,T)
    
    overlap = g2*g1*(F2-F1)
    
    return overlap

def I_(E_start,E_end,E_f,V,T=0,**kwargs):
    E_start = eV_(E_start)
    E_end = eV_(E_end)
    #f = lambda E: overlap(E,E_f,V)
    return integrate.quad(overlap,E_start,E_end,args = (E_f,V,T),**kwargs)

#%%
energies = np.linspace(eV_(-2), eV_(2),num = 10000)
fermi = F_0(energies,300)

plt.plot(energies,fermi)
#%%

energies = np.linspace(eV_(-2), eV_(2),num = 10000)
E_start = eV_(.0025)
overlaps = overlap(E_start,0.2,0.3)

#plt.plot(energies,overlaps)

I_test = I_(-0.1,0.1,0.2,0.00,limit = 1000)

biases = biases = np.linspace(-0.5, 0.5,num = 201)
dopings = np.array([0,0.05,0.1,0.15,0.2,0.25])



for j in dopings:
    IV = list([])
    for i in biases:
        if abs(i) <= 0.1:
            IV.append(-I_(-2*dopings.max(),2*dopings.max(),j,i,limit = 10000,T=300,points = 0)[0])
        else:
            IV.append(-I_(-2,2,j,i,limit = 10000,T=300,points = 0)[0])
    plt.plot(biases , IV)
    plt.title(str(j) + 'V')
    plt.show()
    IV = np.array(IV)
    derivs = np.diff(IV)/np.diff(biases)    
    xs = (biases)[:-1]+np.diff(biases/2)
    plt.plot(xs,derivs)
    plt.show()





#%%
IV = np.array(IV)
derivs = np.diff(IV)/np.diff(biases)
xs = (biases)[:-1]+np.diff(biases/2)
plt.show()
plt.plot(xs,derivs)
plt.show()

IV2 = -IV

derivs2 = np.diff(IV2)/np.diff(biases)

plt.plot(xs,derivs2)
#%%

eV_energies = np.linspace((-2), (2),num = 10000)
energies = np.linspace(eV_(-2), eV_(2),num = 10000)
V_d = np.multiply(0.2,c.electron_volt)
biases = np.linspace(-0.5, 0.5,num = 20)

sums = list([])
for i in biases:
    dV =(2*abs(eV_(i)))
     
    
    densities = D_2d(energies-eV_(i),V_d)
    occupied  = densities * F_0(energies-eV_(i))
    
    densities2 = D_2d(energies+eV_(i),V_d)
    occupied2  = densities2 * F_0(energies+eV_(i))
    
    
    # plt.plot(eV_energies,densities)
    # plt.plot(eV_energies,occupied)
    # plt.show() 
    
    test = densities*densities2*abs(F_0(energies-eV_(i))- F_0(energies+eV_(i)))
    sums.append(test.sum()/dV)
    
    # plt.plot(energies,F_0(energies-eV_(i))- F_0(energies+eV_(i)))
    # plt.plot(energies,test)
    # plt.show() 
    
    # plt.plot(eV_energies,densities2)
    # plt.plot(eV_energies,occupied2)
    # plt.show() 
sums = np.array(sums)
#%%
plt.plot(2*biases,sums)
derivs = np.diff(sums)/np.diff(2*biases)
xs = (2*biases)[:-1]+np.diff(biases)
plt.show()
plt.plot(xs,derivs)

# densities = D_2D(energies-eV_(i))*F_0(energies,-eV_(i),V_d)
# densities2 = D_2D(energies+eV_(i))*F_0(energies,+eV_(i),V_d)
    
# plt.plot(energies,densities)
# plt.plot(energies,densities2)
# plt.show() 
     
#         #plt.plot(energies,np.multiply(densities,densities2))
# plt.show()  
    
