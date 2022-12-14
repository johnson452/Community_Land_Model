#!/usr/bin/env python3
"""
Evaporation model:
Inputs: State, Grid, i
Outputs: None

#Requires linking to the defintions:
"""
import numpy as np
import os
import sys

# Colocated modules
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, ".", "TABLES")
sys.path.append(mymodule_dir)
import table_2_7_physical_constants as constants
import table_3_1_plant_optics as pft
import table_2_4_atmospheric_forcings as af
import table_5_1_pft_aerodynamic as paero


def run_evaporation_model(State, Grid, App, i):
    print("Running evaporation Model\n")


def water_vapor_flux(State, Grid, App, i):
    E = -1.2 * State.evaporation.humidity_ratio[i] / State.evaporation.ra[i]
    State.evaporation.E[i] = E
    return E


def latent_heat_water_vapor_flux(State, Grid, App, i):
    lmd = constants.physical_constants().constants("latent heat of vaporization")
    L_E = lmd * State.evaporation.E[i]
    State.evaporation.L_E[i] = L_E
    return L_E


def vegetation_water_vapor_flux(State, Grid, App, i):
    q_s = State.evaporation.q_s[i]
    q_sat = State.evaporation.q_sat[i]
    Ev = (
        -1.2
        * (q_s - q_sat)
        / ((1000 * State.evaporation.ra[i]) + State.evaporation.ra[i])
    )
    State.evaporation.Ev[i] = Ev
    return Ev


# Equation 5.46, 5.48 with modification using AMS infomation
def MO_length(State, Grid, App, i):
    z = af.atm_inputs().constants("thickness")
    Tv = 1.38 * State.evaporation.temperature[i]
    theta_v = 1.38 * State.evaporation.potential_temperature[i]
    R_iB = ((9.8 / Tv) * theta_v * z) / State.evaporation.windspeed[i] ** 2
    if R_iB < 0:
        Ksi = R_iB * np.log(z)
    else:
        Ksi = (R_iB * np.log(z)) / (1 - 5 * min(R_iB, 0.19))
    L = z / Ksi
    State.evaporation.L[i] = L
    State.evaporation.Ksi[i] = Ksi
    return (L, Ksi)


# Assume roughness length is 1
def friction_velocity(State, Grid, App, i, psi):
    """
    L = MO_length(State,Grid,App,i)[1]
    Ksi = MO_length(State,Grid,App,i)[2]
    psi = psi(ksi)

    """
    L = State.evaporation.L[i]
    Ksi = State.evaporation.Ksi[i]
    z = af.atm_inputs().constants("thickness")
    z0 = af.atm_inputs().constants("roughness length")
    k = constants.physical_constants().constants("von karman constant")
    if Ksi < -1.574:
        Va = (
            State.evaporation.U_av[i]
            / k
            * (
                (np.log(-1.574 * L / z0) - psi(-1.574))
                + 1.14 * ((-Ksi) ** (1 / 3) - (1.574) ** (1 / 3))
                + psi(z0 / L)
            )
        )
    elif Ksi >= -1.574 and Ksi < 0:
        Va = State.evaporation.U_av[i] / k * ((np.log(z / z0) - psi(Ksi)) + psi(z0 / L))
    elif Ksi >= 0 and Ksi < 1:
        Va = State.evaporation.U_av[i] / k * (np.log(z / z0) + 5 * Ksi - 5 * z0 / L)
    else:
        Va = (
            State.evaporation.U_av[i]
            / k
            * (np.log(L / z0) + 5 + 5 * np.log(Ksi) + Ksi - 1 - 5 * z0 / L)
        )
    State.evaporation.windspeed[i] = Va
    return Va


def q_sat(State, Grid, App, i):
    T = State.evaporation.temperature[i]
    P = constants.physical_constants().constants("atmosphere pressure")
    e_sat = 100 * (6.11 + 0.444 * T + 0.0143 * (T**2) + 0.000264 * (T**2))
    q_sat = (0.622 * e_sat) / (P - 0.378 * e_sat)
    State.evaporation.q_sat[i] = q_sat
    return q_sat


def heat_flux_grad(State, Grid, App, i):
    k = constants.physical_constants().constants("von karman constant")
    Ksi = State.evaporation.Ksi[i]

    if Ksi < -1.574:
        phi = 0.9 * k ** (4 / 3) * ((-Ksi) ** (-1 / 3))
    elif Ksi >= -1.574 and Ksi < 0:
        phi = (1 - 16 * Ksi) ** (-0.5)
    elif Ksi >= 0 and Ksi < 1:
        phi = 1 + 5 * Ksi
    else:
        phi = 5 + Ksi
    return phi


def humidity_ratio(State, Grid, App, i, L, Ksi, psi):
    """
    L = MO_length(State,Grid,App,i)[1]
    Ksi = MO_length(State,Grid,App,i)[2]
    psi = psi(ksi)

    """
    z0 = af.atm_inputs().constants("roughness length")
    z = af.atm_inputs().constants("thickness")
    k = constants.physical_constants().constants("von karman constant")
    if Ksi < -1.574:
        del_q = (
            State.evaporation.specific_humidity[i]
            / k
            * (
                (np.log(-1.574 * L / z0) - psi(-1.574))
                + 1.14 * ((-Ksi) ** (1 / 3) - (1.574) ** (1 / 3))
                + psi(z0 / L)
            )
        )
    elif Ksi >= -1.574 and Ksi < 0:
        del_q = (
            State.evaporation.specific_humidity[i]
            / k
            * ((np.log(z / z0) - psi(Ksi)) + psi(z0 / L))
        )
    elif Ksi >= 0 and Ksi < 1:
        del_q = (
            State.evaporation.specific_humidity[i]
            / k
            * (np.log(z / z0) + 5 * Ksi - 5 * z0 / L)
        )
    else:
        del_q = (
            State.evaporation.specific_humidity[i]
            / k
            * (np.log(L / z0) + 5 + 5 * np.log(Ksi) + Ksi - 1 - 5 * z0 / L)
        )
    State.evaporation.humidity_ratio[i] = del_q
    return del_q


def temperature_ratio(State, Grid, App, i, L, Ksi, psi):
    """
    L = MO_length(State,Grid,App,i)[1]
    Ksi = MO_length(State,Grid,App,i)[2]
    psi = psi(ksi)

    """
    z0 = af.atm_inputs().constants("roughness length")
    z = af.atm_inputs().constants("thickness")
    k = constants.physical_constants().constants("von karman constant")
    if Ksi < -1.574:
        del_t = (
            State.evaporation.potential_temperature[i]
            / k
            * (
                (np.log(-1.574 * L / z0) - psi(-1.574))
                + 1.14 * ((-Ksi) ** (1 / 3) - (1.574) ** (1 / 3))
                + psi(z0 / L)
            )
        )
    elif Ksi >= -1.574 and Ksi < 0:
        del_t = (
            State.evaporation.potential_temperature[i]
            / k
            * ((np.log(z / z0) - psi(Ksi)) + psi(z0 / L))
        )
    elif Ksi >= 0 and Ksi < 1:
        del_t = (
            State.evaporation.potential_temperature[i]
            / k
            * (np.log(z / z0) + 5 * Ksi - 5 * z0 / L)
        )
    else:
        del_t = (
            State.evaporation.potential_temperature[i]
            / k
            * (np.log(L / z0) + 5 + 5 * np.log(Ksi) + Ksi - 1 - 5 * z0 / L)
        )
    State.evaporation.temperature_ratio[i] = del_t
    return del_t


def U_av(State, Grid, App, i, Va, rm):
    U_av = Va * np.sqrt(1 / (rm * Va))
    State.evaporation.U_av[i] = U_av
    return U_av


def r_b(State, Grid, App, i):
    Rz, Rd, d_leaf = paero.plant_aero(State.pft)
    r_b = ((State.evaporation.U_av[i] / d_leaf) ** (-0.5)) / 0.01
    State.evaporation.rb[i] = r_b
    return r_b


# rah = raw, eqs 5.122
def ra(State, Grid, App, i, U_av):
    ra = 1 / (0.01 * State.evaporation.U_av[i])
    State.evaporation.ra[i] = ra
    return ra


def canopy_specific_humidity(State, Grid, App, i):
    ca = 1 / State.evaporation.ra[i]
    cg = 1 / (
        (1000 * State.evaporation.ra[i]) + State.evaporation.ra[i]
    )  # resistance in soil is empirically estimated to be 1000 times of the resistance in air
    cv = (0.05) / State.evaporation.rb[i]
    q_atm = State.evaporation.specific_humidity[i]
    q_sat = State.evaporation.q_sat[i]
    q_s = ((ca + cg) * q_atm + cv * q_sat) / (
        ca + cg + cv
    )  # humidity of soil is assumed to be the same as in atm
    State.evaporation.q_s[i] = q_s
    return q_s


# helper function

# eqs 5.36
def psi(ksi):
    x = (1 - 16 * ksi) ** (1 / 4)
    return (
        2 * np.log(1 + x / 2)
        + np.log((1 + x**2) / 2)
        - 2 * (1 / np.tan(x))
        + np.pi / 2
    )


def air_res(del_q, Va, del_T):
    k = constants.physical_constants().constants("von karman constant")
    rw = del_q / (k ** (2) * k)
    rm = Va / (k ** (2) * k)
    rh = del_T / (k ** (2) * k)
    return (rw, rm, rh)


# eqs5.21
# def phi_integrated(State,Grid,App,i,y,x):
#     k = constants.physical_constants().constants("von karman constant")
#     Ksi = MO_length(State,Grid,App,i)[2]
#     if Ksi < -1.574:
#         phi_itg = (y  + 1.35 * k ** (2/3) * (y)**(2/3) -
#                     (x  + 1.35 * k ** (2/3) * (x)**(2/3)))
#     elif Ksi >= -1.574 and Ksi < 0:
#         phi_itg = (y + ((1 - 16 * y)**(0.5))/8 -
#                     x + ((1 - 16 * x)**(0.5))/8)
#     elif Ksi >= 0 and Ksi <1:
#         phi_itg = (y + 2.5 * y ** (2) -
#                     (x + 2.5 * x ** (2)))
#     else:
#         phi_itg = (5 * y + 0.5 * y ** (2) -
#                     (5 * x + 0.5 * x ** (2) ))
#     return phi_itg
