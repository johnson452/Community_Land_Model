#!/usr/bin/env python3
"""
Test for verifying the integration_schemes module

#Requires linking to the defintions:
SRC/METHODS/time_integration.py
"""

import os
import sys
import numpy as np
import pytest

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC/METHODS")
sys.path.append(mymodule_dir)
import time_integration


def test_integration_schemes():
#Testing for time_integration Lorentz Attractor Eqs.

    def F(y):
        f1 = (10*(y[1]-y[0]))
        f2 = (y[0]*(28-y[2])-y[1])
        f3 = (y[0]*y[1]) - ((8/3)*y[2])
        dy_dt = [f1,f2,f3]
        return dy_dt


    #Begin Code
    # At t = 0
    N_eqs = 3
    Y0 = [15,15,36]
    t0 = 0
    tf = 1
    Nt = 60
    s = (N_eqs,Nt)
    dt = (tf-t0)/Nt

    #Startup the AMB method with Euler
    Y_euler = np.zeros(s)
    Y_RK4 = np.zeros(s)
    [t,Y_euler] = time_integration.euler(t0,tf,Y0,Nt,N_eqs,F)
    [t,Y_RK4] = time_integration.RK4(t0,tf,Y0,Nt,N_eqs,F)

    #Tests:
    assert 2.347967745136695 == pytest.approx(Y_euler[0,Nt-1],1e-6)
    assert 3.8753495405996334 == pytest.approx(Y_euler[1,Nt-1],1e-6)
    assert 19.571312790183274 == pytest.approx(Y_euler[2,Nt-1],1e-6)
    assert -8.670923072265706 == pytest.approx(Y_RK4[0,Nt-1],1e-6)
    assert 1.9781532028346487 == pytest.approx(Y_RK4[1,Nt-1],1e-6)
    assert 37.080220186856806 == pytest.approx(Y_RK4[2,Nt-1],1e-6)



if __name__ == "__main__":
    test_integration_schemes()
