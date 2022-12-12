#!/usr/bin/env python3
"""
Parts of Table 2.7 Physical constants;
Names are all lowercases.
"""

# From CLM5 PFT table 2.7.
""" def physical_constants(constant):
    c = constant
    if c == "specific heat capacity of dry air":
        k = 1.00464 * 10 ** 3
    if c == "specific heat capacity of water":
        k = 4.188 * 10 ** 3
    if c == "specific heat capacity of ice":
        k = 2.11727 * 10 ** 3
    if c == "latent heat of vaporization":
        k = 2.501 * 10 ** 6
    if c == "latent heat of fusion":
        k = 3.337 * 10 ** 5
    if c == "latent heat of sublimation":
        k = 2.501 * 10 ** 6 + 3.337 * 10 ** 5
    if c == "density of ice":
        k = 917
    if c == "boltzmann constant":
        k = 1.38065 * 10 ** (-23)
    if c == "stefan-boltzmann constant":
        k = 5.67 * 10 ** (-8)
    return k
 """


class physical_constants:
    def __init__(self):
        self.constants: dict(str, float) = {
            "specific heat capacity of dry air": 1.00464 * 10**3,
            "specific heat capacity of water": 4.188 * 10**3,
            "specific heat capacity of ice": 2.11727 * 10**3,
            "latent heat of vaporization": 2.501 * 10**6,
            "latent heat of fusion": 3.337 * 10**5,
            "latent heat of sublimation": 2.501 * 10**6 + 3.337 * 10**5,
            "density of ice": 917,
            "boltzmann constant": 1.38065 * 10 ** (-23),
            "stefan-boltzmann constant": 5.67 * 10 ** (-8),
        }


table_data = physical_constants()
