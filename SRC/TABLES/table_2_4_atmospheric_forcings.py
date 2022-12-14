#!/usr/bin/env python3
"""
Parts of Table 2.4 Atmospheric inputs;
Names are all lowercases.
"""
import table_2_7_physical_constants as table_2_7
import os
import numpy as np
import sys


script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..")
sys.path.append(mymodule_dir)
import model_albedo as abdo
import initialization


script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "../..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script

# parameters = input_script.clm_parameters()

# App, State, Grid = initialization.initialize_data(parameters)


# class atm_inputs:
#     def __init__(self):
#         self.constants: dict(str, float) = {
#             "specific heat capacity of dry air": 1.00464 * 10**3,
#             "specific heat capacity of water": 4.188 * 10**3,
#             "specific heat capacity of ice": 2.11727 * 10**3,
#             "latent heat of vaporization": 2.501 * 10**6,
#             "latent heat of fusion": 3.337 * 10**5,
#             "latent heat of sublimation": 2.501 * 10**6 + 3.337 * 10**5,
#             "density of ice": 917,
#             "boltzmann constant": 1.38065 * 10 ** (-23),
#             "stefan-boltzmann constant": 5.67 * 10 ** (-8),
#         }

# ##helper functions
# def solar_radiation(State,Grid,App,i):
#     pass

# def cal_temperature(State,Grid,App):
#     for k in range(0,Grid.NT):
#         # Temperature as a function of the day in year modeled by KY using 2021 data
#         # Misfit of the model is 0.1454, which I (KY) think is acceptable
#         State.evaporation.temperature()[k] = (
#             55.0901
#             - 19.6674 * np.cos(2 * np.pi * Grid.times[k] / 365)
#             - 8.6196 * np.sin(2 * np.pi * Grid.times[k] / 365)
#         )
#         # print(State.evaporation.temperature()[k])
#     return State.evaporation.temperature()
# # cal_temperature(State,Grid,App)
# # print(type(State.evaporation.temperature()))
