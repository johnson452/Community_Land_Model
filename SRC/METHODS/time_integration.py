#!/usr/bin/env python3
"""
Time Integratation

#Requires linking to the defintions:
"""

import numpy as np

def RK4(t0,tmax,Y0,N,N_eqs,F):
    t,dt=np.linspace(t0,tmax,N,retstep=True)
    Y2=np.zeros((N_eqs,N))
    Y2[:,0]=Y0
    dt=(t[-1]-t[0])/N
    for n in range(N-1):
        K1 = F(Y2[:,n])
        K2 = F(Y2[:,n] + np.multiply((dt/2),K1))
        K3 = F(Y2[:,n] + np.multiply((dt/2),K2))
        K4 = F(Y2[:,n] + np.multiply((dt),K3))
        Y2[:,n+1] = Y2[:,n]+np.multiply(dt/6,K1) +np.multiply(dt/3,K2) +np.multiply(dt/3,K3)+np.multiply(dt/6,K4)
    return t,Y2


def euler(t0,tmax,Y0,N,N_eqs,F):
    t,dt=np.linspace(t0,tmax,N,retstep=True)
    s = (N_eqs,N) #Cast the size of the array to be returned
    Y=np.zeros(s)    #Build array
    Y[:,0]=Y0
    for n in range(N-1):
        Y[:,n+1] = Y[:,n] + np.multiply(dt, F(Y[:,n]))
    return t,Y
