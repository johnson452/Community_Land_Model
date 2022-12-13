#!/usr/bin/env python3
"""
Test the Radiation Fluxes Module

Based on SRC/model_radiation_fluxes.py

To test specifically
pytest -s -q -rA tests/test_radiation.py
"""

# Load in Modules
import os
import sys
import pytest

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
import model_albedo
import model_radiation_fluxes as mrf

mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization

# Timestep to stop on
dT = 3

@pytest.fixture
def test_run():
    # Initialize Model
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)

    # Run Routine from timestep
    for i in range(dT+1):
        model_albedo.run_albedo_model(State, Grid, App, i)
        mrf.run_radiation_model(State, Grid, App, i)
    #print(State.radiation.T_rad[dT-1])
    #return App, State, Grid
    return State

# Standalone Test
def test_r_vis_calc():
    ''' Tests the r_vis_calc helper function'''
    assert 0.17639 == mrf.r_vis_calc(0, 0)
    assert (mrf.r_vis_calc(100, 0.00) 
        == mrf.r_vis_calc(100, -5))
    assert (mrf.r_vis_calc(100, 1.00) 
        == mrf.r_vis_calc(100, 12))
    #model_radiation_fluxes.r_nir_calc(1, 0.5)
    #State_temp = test_run # Return T
    #print(State_temp.radiation.T_rad[dT-1])

# Standalone Test
def test_r_nir_calc():
    ''' Tests the r_nir_calc helper function'''
    assert 0.29548 == mrf.r_nir_calc(0, 0)
    assert 0.29548 == mrf.r_nir_calc(0, 99999)
    assert 0.29548 == mrf.r_nir_calc(0, -99999)
    assert 0.01 == mrf.r_nir_calc(100,9999)
    assert 0.99 == mrf.r_nir_calc(100,-9999)

# Standalone test
def test_ratio_test():
    ''' Check that r_nir_calc GEQ to r_vis_calc '''
    assert mrf.r_nir_calc(100, 0.5) >= mrf.r_vis_calc(100, 0.5)
    assert mrf.r_nir_calc(50, 0.5) >= mrf.r_vis_calc(50, 0.5)
    assert mrf.r_nir_calc(200, 0.5) >= mrf.r_vis_calc(200, 0.5)
    assert mrf.r_nir_calc(25, 0.5) >= mrf.r_vis_calc(25, 0.5)


# Fixture Test
def test_radiation(test_run):
    ''' 
    Test the STATE variables output 
    from radiation module at timestep specified 
    '''
    State_t = test_run 

    #print(State_t.radiation.T_rad[dT])
    assert 270.2 == pytest.approx(State_t.radiation.T_rad[dT], 10**-2)

# For running solo
if __name__ == "__main__":
    test_radiation()
