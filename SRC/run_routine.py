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

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
import model_albedo
import model_absorbed_emitted_radiation
import model_evaporation
import model_sensible_heat_flux


def run_clm(App, State, Grid):

    # Print statement
    print("Running: run_clm\n")

    # Run the main timeloop
    for i in range(Grid.timeloop):

        # Run the modules
        if App.model_albedo:
            model_albedo.run_albedo_model(State, Grid, i)
            print("Running: run_clm - model_albedo, iteration: " + str(i) + "\n")

        if App.model_absorbed_emitted_radiation:
            model_absorbed_emitted_radiation.run_absorbed_emitted_radiation_model(
                State, Grid, i
            )
            print(
                "Running: run_clm - model_absorbed_emitted_radiation, iteration: "
                + str(i)
                + "\n"
            )

        if App.model_evaporation:
            model_evaporation.run_evaporation_model(State, Grid, i)
            print("Running: run_clm - model_evaporation, iteration: " + str(i) + "\n")

        if App.model_sensible_heat_flux:
            model_sensible_heat_flux.run_sensible_heat_flux_model(State, Grid, i)
            print(
                "Running: run_clm - model_sensible_heat_flux, iteration: "
                + str(i)
                + "\n"
            )

    # Output (App, State, Grid) to a file
    App.save()
    State.save()
    Grid.save()
