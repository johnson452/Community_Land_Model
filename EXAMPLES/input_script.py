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

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'SRC' )
sys.path.append( mymodule_dir )
import initialization
import run_routine


### ---------- Sim Params ---------- ###
# Parameters
class clm_parameters:
    def __init__(self):

        # General parameters:
        self.NZ: int = 10
        self.NT: int = 10
        self.dz: float = 0.1
        self.dt: float = 0.1

        # Models to include:
        self.model_albedo: bool = True
        self.model_cloud: bool = False

        # Model Parameters
        if self.model_albedo:
            self.default_albedo_conditions: bool = True

        if self.model_cloud:
            self.default_cloud_conditions: bool = True


### ---------- Main loop ---------- ###
def main():
    # Get the data for the simulation
    parameters = clm_parameters()

    # Build the main structures using the initial data
    App, State, Grid = initialization.initialize_data(parameters)

    # Run the simulation
    run_routine.run_clm(App, State, Grid)


# Run the main code
main()
