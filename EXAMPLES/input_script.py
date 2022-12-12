#!/usr/bin/env python3
"""
Main Project loop:
Inputs: None
Outputs: None

#Requires linking to the definitions:
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

        # Location parameters:
        self.time_start: float = 0
        self.time_end: float = 365
        self.location: str = "Princeton"
        self.vegetated_surface: bool = True

        # Input data parameters/include
        self.data_start: bool = True
        self.data_filename: str = "data.csv"
        self.vis_in_str: str = "Vis_in"
        self.vis_out_str: str = "Vis_out"
        self.IR_in_str: str = "IR_in"
        self.IR_out_str: str = "IR_out"
        self.T_g_str: str = "T_g"

        # Models to include:
        self.model_albedo: bool = True
        self.model_radiation_fluxes: bool = True
        self.model_absorbed_emitted_radiation: bool = True
        self.model_evaporation: bool = True
        self.model_sensible_heat_flux: bool = True

        # Model Parameters
        if self.model_albedo:
            self.default_albedo_conditions: bool = True
        if self.model_radiation_fluxes:
            self.radiation_conditions: bool = True
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
