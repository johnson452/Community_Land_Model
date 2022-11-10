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

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'OUTPUT' )

def initialize_data(parameters):
    App = clm_app(parameters)
    State = clm_state(parameters)
    Grid = clm_grid(parameters)
    return App, State, Grid


class clm_app:
    def __init__(self, parameters):
        self.name = "App_Data"
        self.model_cloud = parameters.model_cloud
        self.model_albedo = parameters.model_albedo

    # Savedata: https://stackoverflow.com/questions/2345151/how-to-save-read-class-wholly-in-python
    def save(self):
        """save class as self.name.txt"""
        print("Saving App\n")
        file = open("/"+mymodule_dir + "/"+self.name + ".txt", "wb")
        pickle.dump(self,file)
        file.close()

    def load(self):
        """try load self.name.txt"""
        print("Loading App\n")
        file = open("/"+mymodule_dir + "/"+ self.name + ".txt", "rb")
        dataPickle = file.read()
        file.close()

        self = pickle.loads(dataPickle)


class clm_state:
    def __init__(self, parameters):
        print("Nothing in clm_state __init__ yet\n")


class clm_grid:
    def __init__(self, parameters):
        self.timeloop: int = 3
        print("Nothing in clm_grid __init__ yet\n")
