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

    # Build the desired plots
    X = Grid.times
    Y = State.mu
    str_val_x = str("time")
    str_val_y = str("mu")
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.L_up
    str_val_y = str("L_up")
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.L_down
    str_val_y = str("L_down")
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.fcan_snow
    str_val_y = str("fcan_snow")
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.fsno
    str_val_y = str("fsno")
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.L
    str_val_y = str("L, Leaf Coverage Frac")
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.S
    str_val_y = str("S, Stem Coverage Frac")
    plot_general(X, Y, str_val_x, str_val_y)



# Build the mu vs t plot and save it
def plot_general(X, Y, str_val_x, str_val_y):

    # Plot commonly wanted things (T(t), etc.)
    plt.plot(X, Y)
    plt.xlabel(str_val_x)
    plt.ylabel(str_val_y)
    file = mymodule_dir_output_plot + str_val_y + "_v_" + str_val_x + ".png"
    plt.savefig(file)
    print("Saving "+str_val_y+" vs " + str_val_x + " plot\n")



# Assumes the input_script.py holds the model Parameters
print("Reading Parameters from EXAMPLES/input_script.py")

# Run the diagnostics routine
diagnostics()
