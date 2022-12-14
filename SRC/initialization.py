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
import random


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

        # Move Evaportation STATE Variables to subclass
        self.evaporation = evaporation(parameters, NT, Grid)

        # Move Sensible Heat STATE Variables to subclass
        self.sensible_heat = sensible_heat(parameters, NT, Grid)

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
        # Absorbed Photosynthetically active Radiation for sunlit and shaded canopy
        # Equations 4.5 - 4.8
        self.abs_vis_rad_sun = np.zeros(NT)
        self.abs_vis_rad_sha = np.zeros(NT)

        # Outputs from the LW Flux Calculate
        self.lw_net_rad = np.zeros(NT)
        self.T_rad = np.zeros(NT)
        self.T_v = np.ones(NT) * 273.15
        self.lw_net_rad_gro = np.zeros(NT)
        self.lw_net_rad_veg = np.zeros(NT)

        # Helpful inputs to the Radiation Module
        self.vegetated_surface = parameters.vegetated_surface

        # Convert the input data to fractional data
        self.vis_in = np.zeros(NT)
        self.IR_in = np.zeros(NT)
        self.vis_out = np.zeros(NT)
        self.IR_out = np.zeros(NT)
        self.T_g = np.zeros(NT)


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
        self.datatypes: dict(str, str) = {"Radiation": "W/m2", "Temperature": "K"}
        self.vis_in = np.array(self.df[parameters.vis_in_str])
        self.vis_out = np.array(self.df[parameters.vis_out_str])
        self.IR_in = np.array(self.df[parameters.IR_in_str])
        self.IR_out = np.array(self.df[parameters.IR_out_str])
        self.T_ground = np.array(self.df[parameters.T_g_str])


class evaporation:
    def __init__(self, parameters, NT, Grid):
        """Subclass for Evaporation Model"""
        self.temperature = np.zeros(NT)
        self.zonal_wind = np.zeros(NT)
        self.meridional_wind = np.zeros(NT)
        self.windspeed = np.zeros(NT)
        self.humidity = np.zeros(NT)
        self.specific_humidity = np.zeros(NT)
        self.potential_temperature = np.zeros(NT)
        self.U_av = np.zeros(NT)
        self.rm = np.zeros(NT)
        self.rw = np.zeros(NT)
        self.rh = np.zeros(NT)
        self.phi = np.zeros(NT)
        self.L = np.zeros(NT)
        self.Ksi = np.zeros(NT)
        self.temperature_ratio = np.zeros(NT)
        self.humidity_ratio = np.zeros(NT)
        self.q_sat = np.zeros(NT)
        self.rb = np.zeros(NT)
        self.ra = np.zeros(NT)
        self.q_s = np.zeros(NT)
        self.E = np.zeros(NT)
        self.Ev = np.zeros(NT)
        self.L_E = np.zeros(NT)
        self.ra_p = np.zeros(NT)
        for i in range(NT):
            t = Grid.time(i)
            # Temperature as a function of the day in year modeled using 2021 data
            self.temperature[i] = (
                (
                    55.0901
                    - 19.6674 * np.cos(2 * np.pi * t / 365)
                    - 8.6196 * np.sin(2 * np.pi * t / 365)
                )
                - 32
            ) * (5 / 9) + 273.15
            self.potential_temperature[i] = (2 / 7) * self.temperature[i]
            # Approximated using Gaussian distribution N~(6.66,2.81**2)
            self.windspeed[i] = (
                random.gauss(6.66, 2.81) * 1.6 / 3.6
            )  # convert unit to m/s
            if self.windspeed[i] < 0:
                self.windspeed[i] = 0
            self.U_av[i] = self.windspeed[i]  # initialize U_av
            self.zonal_wind[i] = self.windspeed[i] * np.cos(np.pi * random.random())
            self.meridional_wind[i] = np.sqrt(
                self.windspeed[i] ** 2 - self.zonal_wind[i] ** 2
            )

            # Approximated using Gaussian distribution N~(70.77,16.3)
            self.humidity[i] = random.gauss(70.77, 16.3)
            if self.humidity[i] > 100:
                self.humidity[i] = 100
            # Calculate specific humidity using Tentens equation to compute saturation vapor pressure
            self.specific_humidity[i] = (
                0.622
                * (self.humidity[i] / 100)
                * 610.78
                * np.exp(
                    (17.27 * (self.temperature[i] - 273.15))
                    / (self.temperature[i] + 35.85)
                )
            ) / (
                101325
                - 0.378
                * (self.humidity[i] / 100)
                * 610.78
                * np.exp(
                    (17.27 * (self.temperature[i] - 273.15))
                    / (self.temperature[i] + 35.85)
                )
            )


class sensible_heat:
    def __init__(self, parameters, NT, Grid):
        self.T_s = np.zeros(NT)
        self.H_v = np.zeros(NT)
        self.H_tot = np.zeros(NT)
