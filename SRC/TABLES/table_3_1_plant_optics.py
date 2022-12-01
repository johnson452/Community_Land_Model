#!/usr/bin/env python3
"""
Plant optical properties
"""

# From CLM5 PFT table 3.1. alpha/ tau go as:
# (1) leaf-vis, leaf-nir, stem-vis, stem-nir
def plant_props(plant_functional_type):
    pft = plant_functional_type
    if pft == "NET temperate":
        Chi_L = 0.01
        alpha = [0.07, 0.35, 0.16, 0.39]
        tau = [0.05, 0.10, 0.001, 0.001]
    if pft == "NET Boreal":
        Chi_L = 0.01
        alpha = [0.07, 0.35, 0.16, 0.39]
        tau = [0.05, 0.10, 0.001, 0.001]
    if pft == "NDT boreal":
        Chi_L = 0.01
        alpha = [0.07, 0.35, 0.16, 0.39]
        tau = [0.05, 0.10, 0.001, 0.001]
    if pft == "BET tropical":
        Chi_L = 0.1
        alpha = [0.1, 0.45, 0.16, 0.39]
        tau = [0.05, 0.25, 0.001, 0.001]
    if pft == "BET temperate":
        Chi_L = 0.1
        alpha = [0.1, 0.45, 0.16, 0.39]
        tau = [0.05, 0.25, 0.001, 0.001]
    if pft == "BDT tropical":
        Chi_L = 0.01
        alpha = [0.1, 0.45, 0.16, 0.39]
        tau = [0.05, 0.25, 0.001, 0.001]
    if pft == "BDT temperate":
        Chi_L = 0.25
        alpha = [0.1, 0.45, 0.16, 0.39]
        tau = [0.05, 0.25, 0.001, 0.001]
    if pft == "BDT Boreal":
        Chi_L = 0.25
        alpha = [0.1, 0.45, 0.16, 0.39]
        tau = [0.05, 0.25, 0.001, 0.001]
    if pft == "BES temperate":
        Chi_L = 0.01
        alpha = [0.07, 0.35, 0.16, 0.39]
        tau = [0.05, 0.10, 0.001, 0.001]
    if pft == "BDS temperate":
        Chi_L = 0.25
        alpha = [0.1, 0.45, 0.16, 0.39]
        tau = [0.05, 0.25, 0.001, 0.001]
    if pft == "BDS Boreal":
        Chi_L = 0.25
        alpha = [0.1, 0.45, 0.16, 0.39]
        tau = [0.05, 0.25, 0.001, 0.001]
    else: #Grasslands and crops
        Chi_L = -0.4
        alpha = [0.11, 0.35, 0.31, 0.53]
        tau = [0.05, 0.34, 0.120, 0.250]
    return Chi_L, alpha, tau
