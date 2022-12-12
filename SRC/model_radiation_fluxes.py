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
    (
        total_rad_i,
        S_dir_tot,
        S_dif_tot,
        tot_sol_rad_abs_v,
        tot_sol_rad_abs_g,
        vis_in,
        IR_in,
        theta_sun,
        theta_sha,
    ) = solar_fluxes(State, Grid, App, i)

    # Save the outputs back to the State Variables
    State.radiation.total_solar_radiation[i] = total_rad_i
    State.radiation.solar_dir_tot[i] = S_dir_tot
    State.radiation.solar_dif_tot[i] = S_dif_tot
    State.radiation.tot_sol_rad_abs_v[i] = tot_sol_rad_abs_v
    State.radiation.tot_sol_rad_abs_g[i] = tot_sol_rad_abs_g
    State.radiation.vis_in[i] = vis_in
    State.radiation.IR_in[i] = IR_in
    State.radiation.abs_vis_rad_sun[i] = theta_sun
    State.radiation.abs_vis_rad_sha[i] = theta_sha


def solar_fluxes(State, Grid, App, i):
    ## Equation 4.1
    # Find the total incoming solar radiation
    # Convert the daily input data to fractional day
    day = i // (1 / Grid.dt_approx)
    day = int(day)
    vis_in = State.data.vis_in[day]
    IR_in = State.data.IR_in[day]
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
        # State.radiation.tot_sol_rad_abs_v[i] = (
        #    S_dir_tot * State.vector_I_lambda_mu[i] +
        #    S_dif_tot * State.vector_I_lambda[i])
        # Calculate Equation 4.1

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
    # Equ 4.5
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
        vis_in,  # Visible Incoming Radiation
        IR_in,  # IR Incoming Radiation
        theta_sun,  # Absorbed photo active radiation by sunlit canopy
        theta_sha,  # Absorbed photo active radiation by sunlit canopy
    )


def longwave_fluxes(State, Grid, App, i):
    """Second part of Chapter 4"""
    print("Running Longwave Flux Calculator Model\n")


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


#     ### The entire script should return the following
#     State.tot_sol_rad_abs_v[i]
#     State.tot_sol_rad_abs_g[i]
#     # The above come from inputs, section 3, etc...
#     # Equation 4.1, 4.2, 4.3
#     # Check so the test which you should print out
#     State.tot_sol_rad_abs[i]
#     # Equation 4.4
#     # Equation 4.5
#     State.tot_abs_photo_active_rad_sun[i]
#     # Equation 4.6
#     State.tot_abs_photo_active_rad_sha[i]
#     # Equation 4.7
#     State.plant_area_index_sun[i]
#     State.plant_area_index_sha[i]
#     # Equation 4.8
#     State =
#     print("Running radiation Model\n")
# def calc_radiation_fluxes(State, i):
#     ## Radiation subclass
#     Radiation = State.radiation
#     # Check if vegetated
#     if State.vegetated_surface:
#         # Equation 4.1, 4.2
#     else:
#         # Equation 4.3
#     # Equation 4.1
#     S_atm_t = State.solar_flux
#     downward__A = # Incident Direct
#     sol_flux_inc_beam_t = State.sol_flux_inc_beam[i]
#     sol_flux_dif_beam_t = State.sol_flux_dif_beam[i]
#     ### The entire script should return the following
#     State.tot_sol_rad_abs_v[i] = sol_flux_inc_beam_t + sol_flux_dif_beam_t
#     State.tot_sol_rad_abs_g[i]
#     # The above come from inputs, section 3, etc...
#     # Equation 4.1, 4.2, 4.3
#     State.sol_flux_inc_beam = GIVEN
#     State.sol_flux_dif_beam = GIVEN
#     # Check so the test which you should print out
#     State.tot_sol_rad_abs[i]
#     # Equation 4.4
#     # Equation 4.5
#     State.tot_abs_photo_active_rad_sun[i]
#     # Equation 4.6
#     State.tot_abs_photo_active_rad_sha[i]
#     # Equation 4.7
#     State.plant_area_index_sun[i]
#     State.plant_area_index_sha[i]
#     # Equation 4.8
#     State.optical_depth[i]
#     ## Longwave Fluxes
#     # Equation 4.9
#     State.net_lw_rad[i] =
#     # Equation 4.10
#     stef_boltzmann = constants.table_data.constants["stefan-boltzmann constant"]
#     State.temp_rad[i] = (State.net_lw_rad[i]/stef_boltzmann) **(1/4)
