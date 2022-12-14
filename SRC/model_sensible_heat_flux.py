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
import TABLES.table_2_7_physical_constants as table_2_7

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, ".", "TABLES")
sys.path.append(mymodule_dir)


def run_sensible_heat_flux_model(State, Grid, App, i):
    print("Running sensible_heat_flux Model\n")
