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
    str_val_x = "time"
    str_val_y = "mu"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_up_vis
    str_val_y = "I_up_vis"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_down_vis
    str_val_y = "I_down_vis"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_up_nir
    str_val_y = "I_up_nir"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_down_nir
    str_val_y = "I_down_nir"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.fcan_snow
    str_val_y = "fcan_snow"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.fsno
    str_val_y = "fsno"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.L
    str_val_y = "L, Leaf Coverage Frac"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.S
    str_val_y = "S, Stem Coverage Frac"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_sun_vis_mu
    str_val_y = "I_sun_vis_mu"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_sun_nir_mu
    str_val_y = "I_sun_nir_mu"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_shade_vis_mu
    str_val_y = "I_sun_vis_mu"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_shade_nir_mu
    str_val_y = "I_sun_nir_mu"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_sun_vis
    str_val_y = "I_sun_vis"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_sun_nir
    str_val_y = "I_sun_nir"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_shade_vis
    str_val_y = "I_sun_vis"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.I_shade_nir
    str_val_y = "I_sun_nir"
    plot_general(X, Y, str_val_x, str_val_y)

    # Radiation Plots
    Y = State.radiation.vis_in
    str_val_y = "Vis_in"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.total_solar_radiation
    str_val_y = "Total_Solar_Radiation"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.solar_dir_tot
    str_val_y = "Total_Dir_Radiation"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.solar_dif_tot
    str_val_y = "Total_Dif_Radiation"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.tot_sol_rad_abs_v
    str_val_y = "Tot_Sol_Rad_Abs_by_Veg"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.tot_sol_rad_abs_g
    str_val_y = "Tot_Sol_Rad_Abs_by_Ground"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.lw_net_rad
    str_val_y = "lw_net_rad"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.T_rad
    str_val_y = "T_rad_K"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.T_v
    str_val_y = "T_v_K"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.T_g
    str_val_y = "T_g_K"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.lw_net_rad_gro
    str_val_y = "lw_net_rad_gro_Wm2"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.radiation.lw_net_rad_veg
    str_val_y = "lw_net_rad_veg_Wm2"
    plot_general(X, Y, str_val_x, str_val_y)


    # Evaporation Plots
        # self.temperature = np.zeros(NT)
        # self.zonal_wind = np.zeros(NT)
        # self.meridional_wind = np.zeros(NT)
        # self.windspeed = np.zeros(NT)
        # self.humidity = np.zeros(NT)
        # self.specific_humidity = np.zeros(NT)
        # self.potential_temperature = np.zeros(NT)
        # self.U_av = np.zeros(NT)
        # self.rm = np.zeros(NT)
        # self.rw = np.zeros(NT)
        # self.rh = np.zeros(NT)
        # self.phi = np.zeros(NT)
        # self.L = np.zeros(NT)
        # self.Ksi = np.zeros(NT)
        # self.temperature_ratio = np.zeros(NT)
        # self.humidity_ratio = np.zeros(NT)
        # self.q_sat = np.zeros(NT)
        # self.rb = np.zeros(NT)
        # self.ra = np.zeros(NT)
        # self.q_s = np.zeros(NT)
        # self.E = np.zeros(NT)
        # self.Ev = np.zeros(NT)
    Y = State.evaporation.U_av
    str_val_y = "Wind velocity incident on the leaves"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.evaporation.L
    str_val_y = "Monin-Obukhov lenghth"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.evaporation.windspeed
    str_val_y = "Windspeed"
    plot_general(X, Y, str_val_x, str_val_y)  

    Y = State.evaporation.phi
    str_val_y = "phi"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.evaporation.q_s
    str_val_y = "Canopy specific humidity"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.evaporation.q_sat
    str_val_y = "Saturation specific humidity"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.evaporation.E
    str_val_y = "Total vapor flux"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.evaporation.Ev
    str_val_y = "Vapor flux from vegetation"
    plot_general(X, Y, str_val_x, str_val_y)

    Y = State.evaporation.L_E
    str_val_y = "Latent heat"
    plot_general(X, Y, str_val_x, str_val_y)


# Build the mu vs t plot and save it
def plot_general(X, Y, str_val_x, str_val_y):

    # Plot commonly wanted things (T(t), etc.)
    plt.plot(X, Y)
    plt.xlabel(str_val_x)
    plt.ylabel(str_val_y)
    file = mymodule_dir_output_plot + str_val_y + "_v_" + str_val_x + ".png"
    plt.savefig(file)
    print("Saving " + str_val_y + " vs " + str_val_x + " plot\n")
    plt.clf()


# Assumes the input_script.py holds the model Parameters
print("Reading Parameters from EXAMPLES/input_script.py")

# Run the diagnostics routine
diagnostics()
