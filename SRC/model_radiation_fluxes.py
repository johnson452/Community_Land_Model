#!/usr/bin/env python3
"""
Radiation Model model:
Inputs: State, Grid, i
Outputs: None

# Requires linking to the definitions, tables and input data
Follows Chapter 4 of the CLM Documentation
"""
# Modules
import numpy as np
import os
import sys

# Colocated modules
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, ".", "TABLES")
sys.path.append(mymodule_dir)
import table_2_7_physical_constants as constants
import table_3_1_plant_optics as pft


def run_radiation_model(State, Grid, App, i):
    print("Running Radiation Model\n")

    # Save the Radiation Fluxes
    save_radiation_fluxes(State, Grid, App, i)


def save_radiation_fluxes(State, Grid, App, i):
    """Function that fills the STATE variables for use throughout model"""
    (vis_in, vis_out, IR_in, IR_out, T_g) = input_fluxes(State, Grid, App, i)

    # Save the observed fluxes for use later
    State.radiation.vis_in[i] = vis_in
    State.radiation.vis_out[i] = vis_out
    State.radiation.IR_in[i] = IR_in
    State.radiation.IR_out[i] = IR_out
    State.radiation.T_g[i] = T_g

    (
        total_rad_i,
        S_dir_tot,
        S_dif_tot,
        tot_sol_rad_abs_v,
        tot_sol_rad_abs_g,
        theta_sun,
        theta_sha,
    ) = solar_fluxes(State, Grid, App, i)

    # Save the outputs back to the State Variables
    State.radiation.total_solar_radiation[i] = total_rad_i
    State.radiation.solar_dir_tot[i] = S_dir_tot
    State.radiation.solar_dif_tot[i] = S_dif_tot
    State.radiation.tot_sol_rad_abs_v[i] = tot_sol_rad_abs_v
    State.radiation.tot_sol_rad_abs_g[i] = tot_sol_rad_abs_g
    State.radiation.abs_vis_rad_sun[i] = theta_sun
    State.radiation.abs_vis_rad_sha[i] = theta_sha

    (
        lw_net_rad,
        T_rad,
        # T_g, # For Linking to Future Work
        T_v,
        lw_net_rad_gro,
        lw_net_rad_veg,
    ) = longwave_fluxes(State, Grid, App, i)

    State.radiation.lw_net_rad[i] = lw_net_rad
    State.radiation.T_rad[i] = T_rad
    State.radiation.T_v[i] = T_v
    State.radiation.lw_net_rad_gro[i] = lw_net_rad_gro
    State.radiation.lw_net_rad_veg[i] = lw_net_rad_veg


def input_fluxes(State, Grid, App, i):
    """Transforms the dialy input radiation data to match that of the timestep"""
    day = i // (1 / Grid.dt_approx)
    day = int(day)
    vis_in = State.data.vis_in[day]
    vis_out = State.data.vis_out[day]
    IR_in = State.data.IR_in[day]
    IR_out = State.data.IR_out[day]
    T_g = State.data.T_ground[day]

    return (vis_in, vis_out, IR_in, IR_out, T_g)


def solar_fluxes(State, Grid, App, i):
    ## Equation 4.1
    vis_in = State.radiation.vis_in[i]
    IR_in = State.radiation.IR_in[i]
    total_rad_i = vis_in + IR_in

    # Find breakdown  between all direct and all diffuse
    # Equations 33.2 through 33.7
    visible_frac = 0.5  # eq 33.6
    R_vis = r_vis_calc(total_rad_i, visible_frac)  # eq 33.7
    R_nir = r_nir_calc(total_rad_i, visible_frac)  # eq 33.8
    S_dir_vis = R_vis * visible_frac * total_rad_i  # eq 33.2
    S_dir_nir = R_nir * (1 - visible_frac) * total_rad_i  # eq 33.3
    S_dif_vis = (1 - R_vis) * visible_frac * total_rad_i  # eq 33.4
    S_dif_nir = (1 - R_nir) * (1 - visible_frac) * total_rad_i  # eq 33.5

    # Extra Declarations
    S_dir_tot = S_dir_vis + S_dir_nir
    S_dif_tot = S_dif_vis + S_dif_nir

    # Plant Functional Type Data
    Chi_L, alpha, tau = pft.plant_props(State.pft)
    # Calcs borrowed from model_albedo currently
    phi1 = 0.5 - 0.633 * Chi_L - 0.33 * Chi_L * Chi_L
    phi2 = 0.877 * (1 - 2 * phi1)

    # Load in more parameters calculated in initialization State
    mu = State.mu[i]
    mu = abs(mu)  # Debugger
    L = State.L[i]
    S = State.S[i]

    # Recalculate the Optical Depth
    # Equation 4.8
    G_mu = phi1 + phi2 * mu
    K = G_mu / mu
    K_exp = np.exp(-K * (L + S))

    """ Calculate the Total Solar Radiation Absorbed by the Vegetation and Ground """
    if State.radiation.vegetated_surface:
        # Calculate equation 4.1, 4.2
        # All lambdas should be between -1 and 1
        I_lambda_vis_mu = min(1, State.I_lambda_vis_mu[i])
        I_lambda_vis_mu = max(-1, I_lambda_vis_mu)
        I_lambda_nir_mu = min(1, State.I_lambda_nir_mu[i])
        I_lambda_nir_mu = max(-1, I_lambda_nir_mu)
        I_lambda_vis = min(1, State.I_lambda_vis[i])
        I_lambda_vis = max(-1, I_lambda_vis)
        I_lambda_nir = min(1, State.I_lambda_nir[i])
        I_lambda_nir = max(-1, I_lambda_nir)

        tot_sol_rad_abs_v = max(
            0,
            S_dir_vis * I_lambda_vis_mu
            + S_dir_nir * I_lambda_nir_mu
            + S_dif_vis * I_lambda_vis
            + S_dif_nir * I_lambda_nir,
        )
        # Calculate Equation 4.2
        tot_sol_rad_abs_g = max(
            0,
            S_dir_vis * K_exp * (1 - State.a_g_lambda_vis_mu[i])
            + S_dir_nir * K_exp * (1 - State.a_g_lambda_nir_mu[i])
            + (
                S_dir_vis * State.I_down_lambda_vis_mu[i]
                + S_dif_vis * State.I_down_lambda_vis[i]
            )
            * (1 - State.a_g_lambda_vis[i])
            + (
                S_dir_nir * State.I_down_lambda_nir_mu[i]
                + S_dif_nir * State.I_down_lambda_nir[i]
            )
            * (1 - State.a_g_lambda_vis[i]),
        )
    else:
        # Calculate equation 4.3
        tot_sol_rad_abs_v = 0
        tot_sol_rad_abs_g = (
            S_dir_vis * (1 - State.a_g_lambda_vis_mu[i])
            + S_dir_nir * (1 - State.a_g_lambda_nir_mu[i])
            + S_dif_vis * (1 - State.a_g_lambda_vis[i])
            + S_dif_nir * (1 - State.a_g_lambda_vis[i])
        )

    # Sunlit Plant Area Index - # Equation 4.7
    L_sun = (1 - K_exp) / K
    L_sha = L + S - L_sun

    # Calculate absorbed photosynthetically VIS Radiation
    # Eq 4.5
    theta_sun = max(
        0, (State.I_sun_vis_mu[i] * S_dir_vis + State.I_sun_vis[i] * S_dif_vis) / L_sun
    )
    # Eq 4.6
    theta_sha = max(
        0,
        (State.I_shade_vis_mu[i] * S_dir_vis + State.I_shade_vis[i] * S_dif_vis)
        / L_sha,
    )

    return (
        total_rad_i,  # Total Incoming Radiation
        S_dir_tot,  # Total Direct Radiation
        S_dif_tot,  # Total Diffuse Radiation
        tot_sol_rad_abs_v,  # Total Solar Radiation abs. by veg
        tot_sol_rad_abs_g,  # Total Solar Radiation abs. by ground
        theta_sun,  # Absorbed photo active radiation by sunlit canopy
        theta_sha,  # Absorbed photo active radiation by sunlit canopy
    )


def longwave_fluxes(State, Grid, App, i):
    """Second part of Chapter 4"""
    print("Running Longwave Flux Calculator Model\n")
    # Equations 4.9 - 4.20
    lw_down = State.radiation.IR_in[i]
    lw_up = State.radiation.IR_out[i]
    T_g = State.radiation.T_g[i]
    T_g_prev = T_g
    if i > 1:
        T_g_prev = State.radiation.T_g[i - 1]
    T_v_prev = State.radiation.T_v[0]
    if i > 1:
        T_v_prev = State.radiation.T_v[i - 1]

    # Net Longwave radiation at Surface - equation 4.9
    lw_net_rad = lw_up - lw_down

    # Equation 4.10
    # W/m2
    stef_boltz = constants.table_data.constants["stefan-boltzmann constant"]
    #
    T_rad = (lw_up / stef_boltz) ** (1 / 4)

    # Equaition 4.19
    epsilon_soi = 0.96
    epsilon_sno = 0.97
    f_sno = State.fsno[i]
    epsilon_g = epsilon_soi * (1 - f_sno) + epsilon_sno * f_sno
    # Assumption based on literature values
    epsilon_v = 0.957

    # Inputs from State
    L = State.L[i]
    S = State.S[i]
    # Step function for veg 4.12
    step_veg = 0

    # Check if Vegetated Surface or not
    if not State.radiation.vegetated_surface:
        T_v = 0
        lw_net_rad_veg = 0

        # Solve for temperature Ground from 4.12
        # T_g =

        lw_down_blw_veg = 0
    else:
        # Only assume vegetation exists if vegetated_surface flag is turned on
        if (L + S) > 0.05:
            step_veg = 1

        # Equation 4.13 and 4.14
        lw_up_system = lw_up - 4 * epsilon_g * (T_g_prev) ** 3 * (T_g - T_g_prev)
        T_v = (
            (
                lw_up_system
                - (1 - epsilon_g) * (1 - epsilon_v) ** 2 * lw_down
                - epsilon_g * (1 - epsilon_v) * stef_boltz * T_g_prev**4
            )
            / (
                epsilon_v
                * (1 + (1 - epsilon_g) * (1 - epsilon_v))
                * stef_boltz
                * T_v_prev**3
            )
            - T_v_prev
        ) / 4 - T_v_prev

        # Equation 4.16
        lw_down_blw_veg = (
            (1 - epsilon_v) * lw_down
            + epsilon_v * stef_boltz * (T_v_prev) ** 4
            + 4 * epsilon_v * stef_boltz * (T_v_prev**3) * (T_v - T_v_prev)
        )

        # Equation 4.18
        lw_net_rad_veg = (
            2
            - epsilon_v * (1 - epsilon_g) * (epsilon_v * stef_boltz * T_v**4)
            - epsilon_v * epsilon_g * T_g**4
            - epsilon_v * (1 + (1 - epsilon_g) * (1 - epsilon_v)) * lw_down
        )

    # Equation 4.17
    lw_net_rad_gro = (
        epsilon_g * stef_boltz * T_g**4
        - step_veg * epsilon_g * lw_down_blw_veg
        - (1 - step_veg) * epsilon_g * lw_down
    )

    return (
        lw_net_rad,  # Net Longwave Radiation
        T_rad,  # Radiative Temp at Surface (K)
        # T_g, # Temp_ground (K)
        T_v,  # Temp of Vegetation (K)
        lw_net_rad_gro,  # Net Longwave Radiation Flux for ground (W/m2)
        lw_net_rad_veg,  # Net Longwave Radiation Flux for veg (W/m2)
    )


## Helper functions
def r_vis_calc(total_rad_i: float, vis_frac: float) -> float:
    """Find the Ratio of direct to toal incident radiation in the visible - Equation 33.7"""
    a_0 = 0.17639
    a_1 = 0.00380
    a_2 = -9.0039 * 10 ** (-6)
    a_3 = 8.1351 * 10 ** (-9)
    R_vis = (
        a_0
        + a_1 * (vis_frac * total_rad_i)
        + a_2 * (vis_frac * total_rad_i) ** 2
        + a_3 * (vis_frac * total_rad_i) ** 3
    )
    R_vis = max(0.01, R_vis)
    R_vis = min(0.99, R_vis)
    return R_vis


def r_nir_calc(total_rad_i: float, vis_frac: float) -> float:
    """Find Near-Infrared Ratio - Equation 33.8"""
    nir_frac = 1 - vis_frac
    b_0 = 0.29548
    b_1 = 0.00504
    b_2 = -1.4957 * 10 ** (-5)
    b_3 = 1.4881 * 10 ** (-8)
    R_nir = (
        b_0
        + b_1 * (nir_frac * total_rad_i)
        + b_2 * (nir_frac * total_rad_i) ** 2
        + b_3 * (nir_frac * total_rad_i) ** 3
    )
    R_nir = max(0.01, R_nir)
    R_nir = min(0.99, R_nir)
    return R_nir
