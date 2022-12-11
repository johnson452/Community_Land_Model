#!/usr/bin/env python3
"""
Sensible heat flux model:
Inputs: State, Grid, i
Outputs: None

#Requires linking to the defintions:
"""

import os
import sys
import numpy as np
import table_2_7_physical_constants

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, ".", "TABLES")
sys.path.append(mymodule_dir)

def run_sensible_heat_flux_model(State, Grid, App, i):
    print("Running sensible_heat_flux Model\n")

# Disregard the effects of snow and surface water coververed area
def sensible_heat_flux(State,Grid, App, i):
    Cp = table_2_7_physical_constants.physical_constants("specific heat capacity of water")

