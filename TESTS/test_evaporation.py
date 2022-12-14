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
import model_evaporation as me

mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization


def test_evaporation():
    # Initialize
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)
    # State class that is held constant for testing purposes
    State_t = State_test(parameters, Grid)

    # run initialization once to initialize the simulated data with randomness involved

    # Test helper functions
    assert 4.3328664087712 == pytest.approx(me.psi(-1))

    # Test state dependent functions
    k = 1

    # WARNING: These functions are interrelated. If the order of the tests is changed, the
    # tests would fail. If any of the functions is called prior to the tests, the tests, would
    # fail.

    assert (0.00130419499303, 38337.82545) == pytest.approx(
        me.MO_length(State_t, Grid, App, k)
    )
    assert 91179.39029978047 == pytest.approx(
        me.friction_velocity(State_t, Grid, App, k, k)
    )
    assert 91179.39029978047 == pytest.approx(
        me.temperature_ratio(State_t, Grid, App, k, k)
    )
    assert 91179.39029978047 == pytest.approx(
        me.humidity_ratio(State_t, Grid, App, k, k)
    )
    assert (91179.39029978047, 91179.39029978047, 91179.39029978047) == pytest.approx(
        me.air_res(State_t, Grid, App, k)
    )
    assert 1 == pytest.approx(me.U_av(State_t, Grid, App, k))
    assert 0.00404212491432716 == pytest.approx(me.q_sat(State_t, Grid, App, k))
    assert 20.0 == pytest.approx(me.r_b(State_t, Grid, App, k))
    assert 100.0 == pytest.approx(me.ra(State_t, Grid, App, k))
    assert 0.800967491922388 == pytest.approx(
        me.canopy_specific_humidity(State_t, Grid, App, k)
    )
    assert -1094.1526835973655 == pytest.approx(
        me.water_vapor_flux(State_t, Grid, App, k)
    )
    assert -9.553550853243485e-06 == pytest.approx(
        me.vegetation_water_vapor_flux(State_t, Grid, App, k)
    )


class State_test:
    def __init__(self, parameters, Grid):
        NT = Grid.NT
        self.evaporation = evaporation(parameters, NT, Grid)
        self.pft = "BDT temperate"


# Make the variable with randomness constant at 1 for testing
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


if __name__ == "__main__":
    test_evaporation()
