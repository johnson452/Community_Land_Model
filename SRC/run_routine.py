#!/usr/bin/env python3
"""
Run routine, main time loop:
Inputs: structures App, State, Grid
Outputs: None (Calls: save to file)

#Requires linking to the defintions:
file_saves, modules: run_XX
"""


def run_clm(App, State, Grid):

    # Run the main timeloop
    for i in Grid.timeloop:

        # Run the modules
        if App.model_cloud:
            run_cloud_model(State, Grid, i)

        if App.model_albedo:
            run_albedo_model(State, Grid, i)

    # Output (App, State, Grid) to a file
    App.save()
    State.save()
    Grid.save()
