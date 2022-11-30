#!/usr/bin/env python3
"""
Main Project loop:
Inputs: None
Outputs: None

#Requires linking to the defintions:
initialize_data, run_clm
"""
import os
import sys

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
import initialization
import run_routine


### ---------- Sim Params ---------- ###
# Parameters
class clm_parameters:
    def __init__(self):
        # Structure name
        self.name = "Parameter_Data"

        # General parameters:
        self.NZ: int = 10
        self.dz: float = 0.1
        self.time_start: float = 150.5
        self.time_end: float = 151.5
        self.location: string = "Princeton"

        # Models to include:
        self.model_albedo: bool = True
        self.model_absorbed_emitted_radiation: bool = True
        self.model_evaporation: bool = True
        self.model_sensible_heat_flux: bool = True

        # Model Parameters
        if self.model_albedo:
            self.default_albedo_conditions: bool = True
        if self.model_absorbed_emitted_radiation:
            self.absorbed_emitted_radiation_conditions: bool = True
        if self.model_evaporation:
            self.evaporation_conditions: bool = True
        if self.model_sensible_heat_flux:
            self.sensible_heat_conditions: bool = True


### ---------- Main loop ---------- ###
def main():
    # Get the data for the simulation
    parameters = clm_parameters()

    # Build the main structures using the initial data
    App, State, Grid = initialization.initialize_data(parameters)

    # Run the simulation
    run_routine.run_clm(App, State, Grid)


# Run the main code (The if statement allows us to load this file in diagnostics without running main again, while allowing us to run this file as a script)
if __name__ == "__main__":
    main()
