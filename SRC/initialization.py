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

        # (Albedo data) cosine of the solar zenith angle
        NT = Grid.NT
        self.mu = np.zeros(NT)
        # (Albedo data) Location
        if parameters.location == "Princeton":
            self.longitude = (
                0.794 * 2.0 * np.pi
            )  # longitude, radians  (positive east of the Greenwich meridian).
            self.latitude = 0.111 * 2.0 * np.pi  # latitude, radians (from equator)
            self.pft = "BDT temperate"  # plant functional type (BD: boreal desiduos)
        else:
            assert "Invalid Location Specified"
        # Temperature as a function of the day in year modeled by KY using 2021 data
        # Misfit of the model is 0.1454, which I (KY) think is acceptable
        self.temperature = (
            55.0901
            - 19.6674 * np.cos(2 * np.pi * Grid.times / 365)
            - 8.6196 * np.sin(2 * np.pi * Grid.times / 365)
        )
        

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
