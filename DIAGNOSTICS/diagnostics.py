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
import initialization

def diagnostics():
    # Ability to read in / write data
    App.load()
    State.load()
    Grid.load()

    print("Read in the data properly")

    # Analyse and plot data


    # Compute quanitities on data


    # Plot commonly wanted things (T(t), etc.)
