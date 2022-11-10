#!/usr/bin/env python3
"""
Initialization routines:
Inputs: structures Parameters
Outputs: structures App, State, Grid

#Requires linking to the defintions:
"""


def initialize_data(parameters):
    App = clm_app(parameters)
    State = clm_State(parameters)
    Grid = clm_grid(parameters)
    return App, State, Grid


class clm_app:
    def __init__(self, parameters):
        self.name = "App_Data"

    # Savedata: https://stackoverflow.com/questions/2345151/how-to-save-read-class-wholly-in-python
    def save(self):
        """save class as self.name.txt"""
        printf("Saving App\n")
        file = open("/OUTPUT/" + self.name + ".txt", "w")
        file.write(cPickle.dumps(self.__dict__))
        file.close()

    def load(self):
        """try load self.name.txt"""
        file = open("/OUTPUT/" + self.name + ".txt")
        dataPickle = file.read()
        file.close()

        self.__dict__ = cPickle.loads(dataPickle)


class clm_state:
    def __init__(self, parameters):
        printf("Nothing in clm_state __init__ yet\n")


class clm_grid:
    def __init__(self, parameters):
        printf("Nothing in clm_grid __init__ yet\n")
