#!/usr/bin/env python3
"""
Routines for analysing output data

#Requires linking to the defintions:

"""

import os
import sys
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
mymodule_dir = os.path.join(script_dir, "..", "OUTPUT")
mymodule_dir_output_plot = os.path.join(script_dir, "..", "OUTPUT/PLOTS/")
sys.path.append(mymodule_dir_output_plot)
import input_script
import initialization


def diagnostics():

    # Grab the parameters structure, build App, State and Grid with blank data:
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)

    # Ability to read in / write data
    print("Read in the data")
    App.load()
    State = State.load()
    Grid.load()

    # Build the common plots
    plot_mu(App, State, Grid)


# Build the mu vs t plot and save it
def plot_mu(App, State, Grid):

    # Analyse and plot data
    times = Grid.times
    mu = State.mu

    # Compute quantities on data

    # Plot commonly wanted things (T(t), etc.)
    plt.plot(times, mu)
    plt.xlabel("times")
    plt.ylabel("mu")
    file = mymodule_dir_output_plot + "mu_v_time.png"
    plt.savefig(file)
    print("Saving mu vs t plot\n")


# Assumes the input_script.py holds the model Parameters
print("Reading Parameters from EXAMPLES/input_script.py")

# Run the diagnostics routine
diagnostics()
