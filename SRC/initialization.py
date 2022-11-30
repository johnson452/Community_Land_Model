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

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "OUTPUT")


def initialize_data(parameters):
    App = clm_app(parameters)
    State = clm_state(parameters)
    Grid = clm_grid(parameters)
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


class clm_state:
    def __init__(self, parameters):
        self.name = "State_Data"

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


class clm_grid:
    def __init__(self, parameters):
        self.timeloop: int = 3
        self.name = "Grid_Data"

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
