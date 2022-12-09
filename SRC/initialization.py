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

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "OUTPUT")


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

        # (Albedo data)
        # mu: cosine of the solar zenith angle
        # L_up/ L_down Radiation through the canopy
        # fcan_snow Snow covering of the canopy
        # L, S, fraction of ground covered by Leafs, and Stems
        NT = Grid.NT
        self.mu = np.zeros(NT)
        self.I_up = np.zeros(NT)
        self.I_down = np.zeros(NT)
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
                    np.sin(phase + np.pi / 2) * np.sin(phase + np.pi / 2)
                )
                self.fsno[i] = 0.3 * (
                    np.sin(phase + np.pi / 2) * np.sin(phase + np.pi / 2)
                )
                self.L[i] = 0.15 + 0.8 * (np.sin(phase) * np.sin(phase))
                self.S[i] = 0.05 + 0.25 * (
                    np.sin(phase + np.pi / 2) * np.sin(phase + np.pi / 2)
                )
        else:
            assert "Invalid Location Specified"

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
        dt_approx = 0.1
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
