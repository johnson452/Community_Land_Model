#!/usr/bin/env python3
"""
Test for verifying the albedo module

#Requires linking to the defintions:
SRC/model_albedo.py
"""

import os
import sys
import pytest
import pandas
import numpy as np
import random

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
import model_sensible_heat_flux as ms

mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization


def test_sensible_heat():
    # Initialize
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)
    # State class that is held constant for testing purposes
    State_t = State_test(parameters, Grid)


    # Test state dependent functions
    k = 1

    # WARNING: These functions are interrelated. If the order of the tests is changed, the
    # tests would fail. 

    assert 1 == ms.canopy_air_temperature(State_t,Grid,App,k)
    assert 0 == ms.sensible_heat_flux_v(State_t,Grid,App,k)
    assert 861.12 == ms.sensible_heat_flux_tot(State_t,Grid,App,k)

# Make the variable with randomness fixed at 1 for testing
class State_test:
    def __init__(self, parameters, Grid):
        NT = Grid.NT
        self.evaporation = evaporation(parameters, NT, Grid)
        self.radiation = radiation(parameters,NT,Grid)
        self.sensible_heat = sensible_heat(parameters,NT,Grid)
        self.pft = "BDT temperate"
        self.L = np.ones(NT)
        self.S = np.ones(NT)


class evaporation:
    def __init__(self, parameter, NT, Grid):
        """Subclass for Evaporation Model"""
        self.temperature = np.ones(NT)
        self.zonal_wind = np.ones(NT)
        self.meridional_wind = np.ones(NT)
        self.windspeed = np.ones(NT)
        self.humidity = np.ones(NT)
        self.specific_humidity = np.ones(NT)
        self.potential_temperature = np.ones(NT)
        self.U_av = np.ones(NT)
        self.rm = np.ones(NT)
        self.rw = np.ones(NT)
        self.rh = np.ones(NT)
        self.phi = np.ones(NT)
        self.L = np.ones(NT)
        self.Ksi = np.ones(NT)
        self.temperature_ratio = np.ones(NT)
        self.humidity_ratio = np.ones(NT)
        self.q_sat = np.ones(NT)
        self.rb = np.ones(NT)
        self.ra = np.ones(NT)
        self.q_s = np.ones(NT)
        self.E = np.ones(NT)
        self.Ev = np.ones(NT)
        self.ra_p = np.ones(NT)

class radiation:
    def __init__(self, parameter, NT, Grid):
        self.T_v = np.ones(NT)
        self.T_g = np.ones(NT)

class sensible_heat:
    def __init__(self, parameters, NT, Grid):
        self.T_s = np.ones(NT)
        self.H_v = np.ones(NT)
        self.H_tot = np.ones(NT)


if __name__ == "__main__":
    test_sensible_heat()