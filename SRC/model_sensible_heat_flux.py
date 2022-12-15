#!/usr/bin/env python3
"""
Sensible heat flux model:
Inputs: State, Grid, i
Outputs: None

#Requires linking to the defintions:
"""
import numpy as np
import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, ".", "TABLES")
sys.path.append(mymodule_dir)
import table_2_7_physical_constants as constants


def run_sensible_heat_flux_model(State, Grid, App, i):
    print("Running sensible_heat_flux Model\n")

    # Iteration has been done in the evaporation model.
    # Hence, it does not required iteration here.
    canopy_air_temperature(State, Grid, App, i)
    sensible_heat_flux_v(State, Grid, App, i)
    sensible_heat_flux_tot(State, Grid, App, i)


def sensible_heat_flux_v(State, Grid, App, i):
    Cp = constants.physical_constants().constants["specific heat capacity of dry air"]
    H_v = (
        -1.2
        * Cp
        * (State.L[i] + State.S[i])
        * (State.sensible_heat.T_s[i] - State.radiation.T_v[i])
        / State.evaporation.rb[i]
    )
    State.sensible_heat.H_v[i] = H_v
    return H_v


def sensible_heat_flux_tot(State, Grid, App, i):
    Cp = constants.physical_constants().constants["specific heat capacity of dry air"]
    theta = (2 / 7) * State.evaporation.temperature[i]
    H_tot = -1.2 * Cp * (theta - State.sensible_heat.T_s[i]) / State.evaporation.ra[i]
    State.sensible_heat.H_tot[i] = H_tot
    return H_tot


def canopy_air_temperature(State, Grid, App, i):
    ra = State.evaporation.ra[i]
    rb = State.evaporation.rb[i]
    ra_p = State.evaporation.ra_p[i]
    ca = 1 / ra
    cg = 1 / ra_p
    cv = (State.L[i] + State.S[i]) / rb
    T_s = (
        State.evaporation.temperature[i] * ca
        + State.radiation.T_g[i] * cg
        + State.radiation.T_v[i] * cv
    ) / (ca + cv + cg)
    State.sensible_heat.T_s[i] = T_s
    return T_s
