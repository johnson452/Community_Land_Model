#!/usr/bin/env python3
"""
Plant functional type aerodynamic parameters
"""

# From CLM5 table 5.1.
def plant_aero(plant_functional_type):
    pft = plant_functional_type
    if pft == "NET temperate":
        Rz = 0.055
        Rd = 0.67
        d_leaf = 0.04
    if pft == "NET Boreal":
        Rz = 0.055
        Rd = 0.67
        d_leaf = 0.04
    if pft == "NDT boreal":
        Rz = 0.055
        Rd = 0.67
        d_leaf = 0.04
    if pft == "BET tropical":
        Rz = 0.075
        Rd = 0.67
        d_leaf = 0.04
    if pft == "BET temperate":
        Rz = 0.075
        Rd = 0.67
        d_leaf = 0.04
    if pft == "BDT tropical":
        Rz = 0.055
        Rd = 0.67
        d_leaf = 0.04
    if pft == "BDT temperate":
        Rz = 0.055
        Rd = 0.67
        d_leaf = 0.04
    if pft == "BDT Boreal":
        Rz = 0.055
        Rd = 0.67
        d_leaf = 0.04
    if pft == "BES temperate":
        Rz = 0.12
        Rd = 0.68
        d_leaf = 0.04
    if pft == "BDS temperate":
        Rz = 0.12
        Rd = 0.68
        d_leaf = 0.04
    if pft == "BDS Boreal":
        Rz = 0.12
        Rd = 0.68
        d_leaf = 0.04
    else:  # Grasslands and crops
        Rz = 0.12
        Rd = 0.68
        d_leaf = 0.04
    return Rz, Rd, d_leaf
