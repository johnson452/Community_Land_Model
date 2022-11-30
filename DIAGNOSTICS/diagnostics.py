#!/usr/bin/env python3
"""
Routines for analysing output data

#Requires linking to the defintions:

"""

import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization


def diagnostics():

    # Grab the parameters structure, build App, State and Grid with blank data:
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)

    # Ability to read in / write data
    App.load()
    State.load()
    Grid.load()

    print("Read in the data properly")

    # Analyse and plot data

    # Compute quanitities on data

    # Plot commonly wanted things (T(t), etc.)


# Assumes the input_script.py holds the model Parameters
print("Reading Parameters from EXAMPLES/input_script.py")

# Run the diagnostics routine
diagnostics()
