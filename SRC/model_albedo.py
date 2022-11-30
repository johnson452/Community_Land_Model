#!/usr/bin/env python3
"""
Albedo model:
Inputs: State, Grid, i
Outputs: None

#Requires linking to the defintions:
"""

import numpy as np


def run_albedo_model(State, Grid, App, i):
    print("Running Alebedo Model\n")

    # Solar Radiation:
    solar(State, Grid, App, i)


def solar(State, Grid, App, i):
    State.mu[i] = solar_zenith_angle(State, Grid, App, i)


# From clm5: section 3.3
def solar_zenith_angle(State, Grid, App, i):
    d = Grid.time(i)  # day of the year
    phi = State.latitude
    eps = 23.44 * (2 * np.pi / 360)  # Earth's obliquity (Approximately constant)
    lbda = lambda_val(d)  # true longitude of the Earth
    # Eq 3.78 for solar declination
    delta = np.arcsin(np.sin(eps) * np.sin(lbda))
    theta = State.longitude
    # Eq 3.77 for solar hour angle
    h = 2 * np.pi * d + theta

    # Eq 3.76 for solar zenith angle, mu
    mu = np.sin(phi) * np.sin(delta) - np.cos(phi) * np.cos(delta) * np.cos(h)
    return mu


# true longitude of the Earth
def lambda_val(d):
    e = 0.01671  # Earth's Eccetricity
    dve = 80.5  # Vernal Equinox
    Beta = np.sqrt(1 - e**2)
    omega_tilde = 3.392506 * (2 * np.pi / 360)
    lbda_m0 = 2 * (
        (0.5 * e + 0.125 * (e**3)) * (1 - Beta) * np.sin(omega_tilde)
        - 0.25 * (e**2) * (0.5 + Beta) * np.sin(2 * omega_tilde)
        + 0.125 * (e**3) * ((1 / 3) + Beta) * np.sin(3 * omega_tilde)
    )
    lbda_m = lbda_m0 + (2 * np.pi / 365.25) * (d - dve)
    lbda = (
        lbda_m
        + (2 * e - 0.25 * (e**3)) * np.sin(lbda_m - omega_tilde)
        + (5 / 4) * (e**2) * np.sin(2 * (lbda_m - omega_tilde))
        + (13 / 12) * (e**3) * np.sin(3 * (lbda_m - omega_tilde))
    )
    return lbda
