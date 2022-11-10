#!/usr/bin/env python3
"""
Run routine, main time loop:
Inputs: structures App, State, Grid
Outputs: None (Calls: save to file)

#Requires linking to the defintions:
file_saves, modules: run_XX
"""

import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'SRC' )
sys.path.append( mymodule_dir )
import model_albedo
import model_cloud


def run_clm(App, State, Grid):

    #Print statement
    print("Running: run_clm\n")

    # Run the main timeloop
    for i in range(Grid.timeloop):

        # Run the modules
        if App.model_cloud:
            model_cloud.run_cloud_model(State, Grid, i)
            print("Running: run_clm - model_cloud, iteration: "+str(i)+"\n")

        if App.model_albedo:
            model_albedo.run_albedo_model(State, Grid, i)
            print("Running: run_clm - model_albedo, iteration: "+str(i)+"\n")

    # Output (App, State, Grid) to a file
    App.save()
    State.save()
    Grid.save()

    #Test loading the files:
    App.load()
    State.load()
    Grid.load()
