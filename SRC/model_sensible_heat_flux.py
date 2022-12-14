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
import table_3_1_plant_optics as pft
import table_2_4_atmospheric_forcings as af
import table_5_1_pft_aerodynamic as paero

def run_sensible_heat_flux_model(State, Grid, App, i):
    print("Running sensible_heat_flux Model\n")


def heat_flux_grad(State, Grid, App, i):
    k = constants.physical_constants().constants["von karman constant"]
    Ksi = State.evaporation.Ksi[i]

    if Ksi < -1.574:
        phi = 0.9 * k ** (4 / 3) * ((-Ksi) ** (-1 / 3))
    elif Ksi >= -1.574 and Ksi < 0:
        phi = (1 - 16 * Ksi) ** (-0.5)
    elif Ksi >= 0 and Ksi < 1:
        phi = 1 + 5 * Ksi
    else:
        phi = 5 + Ksi
    State.sensible_heat.phi[i] = phi
    return phi