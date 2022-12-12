#!/usr/bin/env python3
"""
Initialization routines:
Inputs: structures Parameters
Outputs: structures App, State, Grid

#Requires linking to the defintions:
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "OUTPUT")
datamodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(datamodule_dir)


def initialize_data(parameters):
    Grid = clm_grid(parameters)
    State = clm_state(parameters, Grid)
    App = clm_app(parameters)
    return App, State, Grid


class clm_app:
    def __init__(self, parameters):
        self.name = "App_Data"
        self.model_evaporation = parameters.model_evaporation
        self.model_albedo = parameters.model_albedo
        self.model_radiation_fluxes = parameters.model_radiation_fluxes
        self.model_sensible_heat_flux = parameters.model_sensible_heat_flux
        self.model_absorbed_emitted_radiation = (
            parameters.model_absorbed_emitted_radiation
        )

    # Savedata: https://stackoverflow.com/questions/2345151/how-to-save-read-class-wholly-in-python
    def save(self):
        """save class as self.name.txt"""
        print("Saving App\n")
        file = open("/" + mymodule_dir + "/" + self.name, "wb")
        pickle.dump(self, file)
        file.close()

    def load(self):
        """try load self.name.txt"""
        print("Loading App\n")
        file = open("/" + mymodule_dir + "/" + self.name, "rb")
        dataPickle = file.read()
        file.close()

        self = pickle.loads(dataPickle)
        return self


class clm_state:
    def __init__(self, parameters, Grid):
        self.name = "State_Data"

        # Number of timesteps
        NT = Grid.NT

        # Load in the Data.CSV file
        if parameters.data_start:
            self.data = input_data(parameters, NT)
        """ Returns an instance of a load_data object"""
        # Currently just runs for a whole year

        # (Albedo data)
        # mu: cosine of the solar zenith angle
        # L_up/ L_down Radiation through the canopy
        # fcan_snow Snow covering of the canopy
        # L, S, fraction of ground covered by Leafs, and Stems
        self.mu = np.zeros(NT)
        self.I_up_vis = np.zeros(NT)
        self.I_down_vis = np.zeros(NT)
        self.I_up_nir = np.zeros(NT)
        self.I_down_nir = np.zeros(NT)

        self.I_sun_vis_mu = np.zeros(NT)
        self.I_sun_nir_mu = np.zeros(NT)
        self.I_shade_vis_mu = np.zeros(NT)
        self.I_shade_nir_mu = np.zeros(NT)
        self.I_sun_vis = np.zeros(NT)
        self.I_sun_nir = np.zeros(NT)
        self.I_shade_vis = np.zeros(NT)
        self.I_shade_nir = np.zeros(NT)

        self.fcan_snow = np.zeros(NT)
        self.fsno = np.zeros(NT)
        self.L = np.zeros(NT)
        self.S = np.zeros(NT)

        # (Albedo data) Location
        if parameters.location == "Princeton":
            # Locational parameters
            self.longitude = (
                0.794 * 2.0 * np.pi
            )  # longitude, radians  (positive east of the Greenwich meridian).
            self.latitude = 0.111 * 2.0 * np.pi  # latitude, radians (from equator)
            self.pft = "BDT temperate"  # plant functional type (BD: boreal desiduos)
            # Assumes identical snow models
            # 95% leaf coverage mid summer, 15% winter
            # 5% stem coverage mid summer, 30% winter
            # 0% snow summer, 30% winter
            for i in range(NT):
                t = Grid.time(i)
                phase = np.pi * (t / 365.25)
                self.fcan_snow[i] = 0.3 * (
                    np.sin(phase + np.pi / 2)
                    * np.sin(phase + np.pi / 2)
                    * np.sin(phase + np.pi / 2)
                    * np.sin(phase + np.pi / 2)
                )
                self.fsno[i] = 0.3 * (
                    np.sin(phase + np.pi / 2)
                    * np.sin(phase + np.pi / 2)
                    * np.sin(phase + np.pi / 2)
                    * np.sin(phase + np.pi / 2)
                )
                self.L[i] = 0.15 + 0.5 * (np.sin(phase) * np.sin(phase))
                self.S[i] = 0.05 + 0.25 * (
                    np.sin(phase + np.pi / 2) * np.sin(phase + np.pi / 2)
                )
        else:
            assert "Invalid Location Specified"

        # Additional intermediate albedo results for data handoffs
        # self.vector_I_lambda_mu = np.zeros(NT)
        # self.vector_I_lambda = np.zeros(NT)
        self.I_lambda_vis_mu = np.zeros(NT)
        self.I_lambda_vis = np.zeros(NT)
        self.I_lambda_nir_mu = np.zeros(NT)
        self.I_lambda_nir = np.zeros(NT)
        self.a_g_lambda_vis_mu = np.zeros(NT)
        self.a_g_lambda_vis = np.zeros(NT)
        self.a_g_lambda_nir_mu = np.zeros(NT)
        self.a_g_lambda_nir = np.zeros(NT)
        self.I_down_lambda_vis_mu = np.zeros(NT)
        self.I_down_lambda_vis = np.zeros(NT)
        self.I_down_lambda_nir_mu = np.zeros(NT)
        self.I_down_lambda_nir = np.zeros(NT)

        # Move Radiation STATE Variables to subclass
        self.radiation = radiation(parameters, NT)

    def save(self):
        """save class as self.name.txt"""
        print("Saving state\n")
        file = open("/" + mymodule_dir + "/" + self.name, "wb")
        pickle.dump(self, file)
        file.close()

    def load(self):
        """try load self.name.txt"""
        print("Loading state\n")
        file = open("/" + mymodule_dir + "/" + self.name, "rb")
        dataPickle = file.read()
        file.close()

        self = pickle.loads(dataPickle)
        return self


class clm_grid:
    def __init__(self, parameters):
        self.name = "Grid_Data"

        self.time_start: float = parameters.time_start
        self.time_end: float = parameters.time_end
        self.total_time: float = parameters.time_end - parameters.time_start
        dt_approx = 0.01  # 0.01  # 0.1, 0.01
        self.dt_approx = dt_approx
        self.NT: int = int(np.ceil(self.total_time / dt_approx))
        times, dt = np.linspace(self.time_start, self.time_end, self.NT, retstep=True)
        self.times: float = times
        self.dt: float = dt  # day fraction, perhaps replace with cfl cond.?

    # Return the times in fractional days
    def time(self, i):
        return self.times[i]

    def save(self):
        """save class as self.name.txt"""
        print("Saving Grid\n")
        file = open("/" + mymodule_dir + "/" + self.name, "wb")
        pickle.dump(self, file)
        file.close()

    def load(self):
        """try load self.name.txt"""
        print("Loading Grid\n")
        file = open("/" + mymodule_dir + "/" + self.name, "rb")
        dataPickle = file.read()
        file.close()

        self = pickle.loads(dataPickle)
        return self


class radiation:
    def __init__(self, parameters, NT):
        """Subclass for Radiation Model"""
        # Arrays to be filled in by the Radiation_Fluxes module
        self.total_solar_radiation = np.zeros(NT)
        self.solar_dir_tot = np.zeros(NT)
        self.solar_dif_tot = np.zeros(NT)
        self.tot_sol_rad_abs_v = np.zeros(NT)  # Vegetation Radiation
        self.tot_sol_rad_abs_g = np.zeros(NT)  # Ground Radiation

        # Helpful inputs to the Radiation Module
        self.vegetated_surface = parameters.vegetated_surface

        # self.stefan_boltzmann = # W/m2/k4

        # Convert the input data to fractional data
        self.vis_in = np.zeros(NT)
        self.IR_in = np.zeros(NT)


class input_data:
    def __init__(self, parameters, NT):
        """Returns npArrays for each input dataset"""
        # Read in CSV
        csv_loc = parameters.data_filename
        csv_start = parameters.time_start
        csv_end = parameters.time_end
        self.df = pd.read_csv(datamodule_dir + "/" + csv_loc)
        self.df = self.df[csv_start:csv_end]

        # Save all data as np.arrays for ease of use
        self.vis_in = np.array(self.df[parameters.vis_in_str])
        self.vis_out = np.array(self.df[parameters.vis_out_str])
        self.IR_in = np.array(self.df[parameters.IR_in_str])
        self.IR_out = np.array(self.df[parameters.IR_out_str])
