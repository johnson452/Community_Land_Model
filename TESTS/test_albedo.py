#!/usr/bin/env python3
"""
Test for verifying the albedo module

#Requires linking to the defintions:
SRC/model_albedo.py
"""

import os
import sys
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
import model_albedo
mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization

def test_albedo():

        # Build empty structures, App, State and Grid with blank data:
        parameters = input_script.clm_parameters()
        App, State, Grid = initialization.initialize_data(parameters)

        # Maybe have a test_parameters script for an easy case

        # Assert values for verified outputs (say for mu)
