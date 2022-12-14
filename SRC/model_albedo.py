#!/usr/bin/env python3
"""
Albedo model:
Inputs: State, Grid, App, i
Outputs: None

#Requires linking to the defintions:
TABLES and METHODS subdirectories
"""
import os
import sys
import numpy as np
import warnings

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, ".", "TABLES")
sys.path.append(mymodule_dir)
import table_3_1_plant_optics

mymodule_dir = os.path.join(script_dir, ".", "METHODS")
sys.path.append(mymodule_dir)
import time_integration


def run_albedo_model(State, Grid, App, i):
    print("Running Albedo Model\n")

    # Solar Radiation:
    solar(State, Grid, App, i)

    # Canopy Radiative Model ( depends on solar mu )
    canopy(State, Grid, App, i)


def canopy(State, Grid, App, i):

    # Run the canopy model for both ir and vis
    for j in range(2):  # [vis/nir model]
        (
            I_up,
            I_down,
            vector_I_sun_lambda_mu,
            vector_I_shade_lambda_mu,
            vector_I_sun_lambda,
            vector_I_shade_lambda,
            vector_I_lambda_mu,
            vector_I_lambda,
            vector_a_g_lambda_mu,
            vector_a_g_lambda,
            I_down_lambda_mu,
            I_down_lambda,
        ) = canopy_model(State, Grid, App, i, j)

        # Save to vis or nir
        if j == 0:
            State.I_up_vis[i] = I_up
            State.I_down_vis[i] = I_down
            State.I_sun_vis_mu[i] = vector_I_sun_lambda_mu
            State.I_shade_vis_mu[i] = vector_I_shade_lambda_mu
            State.I_sun_vis[i] = vector_I_sun_lambda
            State.I_shade_vis[i] = vector_I_shade_lambda
            State.I_lambda_vis_mu[i] = vector_I_lambda_mu
            State.I_lambda_vis[i] = vector_I_lambda
            State.a_g_lambda_vis_mu[i] = vector_a_g_lambda_mu
            State.a_g_lambda_vis[i] = vector_a_g_lambda
            State.I_down_lambda_vis_mu[i] = I_down_lambda_mu
            State.I_down_lambda_vis[i] = I_down_lambda

        if j == 1:
            State.I_up_nir[i] = I_up
            State.I_down_nir[i] = I_down
            State.I_sun_nir_mu[i] = vector_I_sun_lambda_mu
            State.I_shade_nir_mu[i] = vector_I_shade_lambda_mu
            State.I_sun_nir[i] = vector_I_sun_lambda
            State.I_shade_nir[i] = vector_I_shade_lambda
            State.I_lambda_nir_mu[i] = vector_I_lambda_mu
            State.I_lambda_nir[i] = vector_I_lambda
            State.a_g_lambda_nir_mu[i] = vector_a_g_lambda_mu
            State.a_g_lambda_nir[i] = vector_a_g_lambda
            State.I_down_lambda_nir_mu[i] = I_down_lambda_mu
            State.I_down_lambda_nir[i] = I_down_lambda


def solar(State, Grid, App, i):
    State.mu[i] = solar_zenith_angle(State, Grid, App, i)


# From clm5: section 3.1, canopy model/radiative fluxes
def canopy_model(State, Grid, App, i, j):

    # Calculate the bar(mu) average inverse diffuse optical depth per unit leaf and stem area
    # Calculate the optical parameters
    if j == 0:
        (
            I_up,
            I_down,
            vector_I_sun_lambda_mu,
            vector_I_shade_lambda_mu,
            vector_I_sun_lambda,
            vector_I_shade_lambda,
            vector_I_lambda_mu,
            vector_I_lambda,
            vector_a_g_lambda_mu,
            vector_a_g_lambda,
            I_down_lambda_mu,
            I_down_lambda,
        ) = optical_params(State, i, j)

    if j == 1:
        (
            I_up,
            I_down,
            vector_I_sun_lambda_mu,
            vector_I_shade_lambda_mu,
            vector_I_sun_lambda,
            vector_I_shade_lambda,
            vector_I_lambda_mu,
            vector_I_lambda,
            vector_a_g_lambda_mu,
            vector_a_g_lambda,
            I_down_lambda_mu,
            I_down_lambda,
        ) = optical_params(State, i, j)

    return (
        I_up,
        I_down,
        vector_I_sun_lambda_mu,
        vector_I_shade_lambda_mu,
        vector_I_sun_lambda,
        vector_I_shade_lambda,
        vector_I_lambda_mu,
        vector_I_lambda,
        vector_a_g_lambda_mu,
        vector_a_g_lambda,
        I_down_lambda_mu,
        I_down_lambda,
    )


# optical parameters:
def optical_params(State, i, j):

    # Grab the fcan_snow, mu
    fcan_snow = State.fcan_snow[i]
    mu = State.mu[i]

    # Fraction of leaves and stems transmitances, L, S:
    # approximate models:
    L = State.L[i]
    S = State.S[i]

    # Model for the up-down fluxes (1 is more accurate)
    model_up_down_flux = 1

    # pft data
    Chi_L, alpha, tau = table_3_1_plant_optics.plant_props(State.pft)

    # Determine wavelength:
    if j == 0:
        # Grab vis Parameters (Tables 3.1 / 3.2)
        alpha_lambda_leaf = alpha[0]
        alpha_lambda_stem = alpha[2]
        tau_lambda_leaf = tau[0]
        tau_lambda_stem = tau[2]
        omega_lambda_snow = 0.8
        beta_lambda_snow = 0.5
        beta_lambda_snow_0 = 0.5
        # Soil albedos and snow fraction (approximated - average no angle dep)
        # Table 3.3
        a_soi_lambda_mu = 0.25
        a_soi_lambda = a_soi_lambda_mu
        a_sno_lambda_mu = 0.9
        a_sno_lambda = a_sno_lambda_mu
        fsno = State.fsno[i]

    if j == 1:
        # Grab nir Parameters (Tables 3.1 / 3.2)
        alpha_lambda_leaf = alpha[1]
        alpha_lambda_stem = alpha[3]
        tau_lambda_leaf = tau[1]
        tau_lambda_stem = tau[3]
        omega_lambda_snow = 0.4
        beta_lambda_snow = 0.5
        beta_lambda_snow_0 = 0.5
        # Soil albedos and snow fraction (approximated - average no angle dep)
        # Table 3.3
        a_soi_lambda_mu = 0.5
        a_soi_lambda = a_soi_lambda_mu
        a_sno_lambda_mu = 0.5
        a_sno_lambda = a_sno_lambda_mu
        fsno = State.fsno[i]

    # Only valid for -0.4 < Xl < 0.6, but we assume validity to -0.5
    phi1 = 0.5 - 0.633 * Chi_L - 0.33 * Chi_L * Chi_L
    phi2 = 0.877 * (1 - 2 * phi1)

    # Calculate Eq 3.3 relative projected area of leaves and stems in the direction cos−1 𝜇
    G_mu = phi1 + phi2 * mu

    # Calculate the mu_bar_val verage inverse diffuse optical depth per unit leaf and stem area
    mu_bar_val = (1 / phi2) * (1 - (phi1 / phi2) * (np.log((phi1 + phi2) / phi1)))

    # Caluculate weighted leaf and stem contributions
    w_leaf = L / (L + S)
    w_stem = S / (L + S)

    # Calculate [vis nir - wavelength] properties: 3.11, 3.12
    # (alpha, tau -> weighted avgs.)
    alpha_lambda = alpha_lambda_leaf * w_leaf + alpha_lambda_stem * w_stem
    tau_lambda = tau_lambda_leaf * w_leaf + tau_lambda_stem * w_stem
    omega_lambda_veg = alpha_lambda + tau_lambda

    # optical parameters: 3.5
    omega_lambda = omega_lambda_veg * (1 - fcan_snow) + omega_lambda_snow * fcan_snow

    # Calculate the mean leaf inclination angle
    cos_theta_bar = (1 + Chi_L) / 2

    # Calclate the upscatter for diffuse radiation
    omega_lambda_veg_times_beta_lambda_veg = 0.5 * (
        alpha_lambda
        + tau_lambda
        + (alpha_lambda - tau_lambda) * cos_theta_bar * cos_theta_bar
    )

    # single scattering albedo (3.16)
    a_s_mu_lambda = (
        (omega_lambda_veg / 2)
        * (G_mu / np.minimum(mu * phi2 + G_mu, 1e-6))
        * (
            1
            - (mu * phi1 / np.minimum(mu * phi2 + G_mu, 1e-6))
            * (np.log((mu * phi1 + np.minimum(mu * phi2 + G_mu, 1e-6)) / (mu * phi1)))
        )
    )

    # K: optical depth of direct beam per unit leaf and stem area
    K = G_mu / mu

    # Calculate upscatter for direct beam radiation (3.15)
    omega_lambda_veg_times_beta_lambda_veg_0 = (
        (1 + mu_bar_val * K) / (mu_bar_val * K)
    ) * a_s_mu_lambda

    # optical parameters: 3.5 (3.6 - 3.7) & ()3.8 - 3.10)
    omega_lambda_beta_lambda = (
        omega_lambda_veg_times_beta_lambda_veg * (1 - fcan_snow)
        + omega_lambda_snow * beta_lambda_snow * fcan_snow
    )
    omega_lambda_beta_lambda_0 = (
        omega_lambda_veg_times_beta_lambda_veg_0 * (1 - fcan_snow)
        + omega_lambda_snow * beta_lambda_snow_0 * fcan_snow
    )

    # Calculate (Ground albedos Section 3.2)
    a_g_lambda_mu = a_soi_lambda_mu * (1 - fsno) + a_sno_lambda_mu * fsno
    a_g_lambda = a_soi_lambda * (1 - fsno) + a_sno_lambda * fsno

    # Calculate various components, to simplify math: (3.31-3.57)
    c = omega_lambda_beta_lambda
    b = 1 - omega_lambda + c
    d = mu_bar_val * K * omega_lambda_beta_lambda_0
    f = omega_lambda * mu_bar_val * K - d
    h = np.sqrt(b * b - c * c) / mu_bar_val
    sigma = mu_bar_val * mu_bar_val * K * K + c * c - b * b
    u1_mu = b - c / a_g_lambda_mu
    u2_mu = b - c * a_g_lambda_mu
    u3_mu = f + c * a_g_lambda_mu
    u1 = b - c / a_g_lambda
    u2 = b - c * a_g_lambda
    u3 = f + c * a_g_lambda

    # suppress warnings for large values
    warnings.filterwarnings("ignore")
    s1 = np.exp(-np.minimum(h * (L + S), 40))
    s2 = np.exp(-np.minimum(K * (L + S), 40))
    p1 = b + mu_bar_val * h
    p2 = b - mu_bar_val * h
    p3 = b + mu_bar_val * K
    p4 = b - mu_bar_val * K
    d1_mu = p1 * (u1_mu - mu_bar_val * h) / s1 - p2 * (u1_mu + mu_bar_val * h) * s1
    d2_mu = (u2_mu + mu_bar_val * h) / s1 - (u2_mu - mu_bar_val * h) * s1
    d1 = p1 * (u1 - mu_bar_val * h) / s1 - p2 * (u1 + mu_bar_val * h) * s1
    d2 = (u2 + mu_bar_val * h) / s1 - (u2 - mu_bar_val * h) * s1

    # use mu quantities
    h1 = -d * p4 - c * f
    h2 = (1 / d1_mu) * (
        (d - (h1 / sigma) * p3) * ((u1_mu - mu_bar_val * h) / s1)
        - p2 * (d - c - (h1 / sigma) * (u1_mu + mu_bar_val * K)) * s2
    )
    h3 = -(1 / d1_mu) * (
        (d - (h1 / sigma) * p3) * ((u1_mu + mu_bar_val * h) * s1)
        - p1 * (d - c - (h1 / sigma) * (u1_mu + mu_bar_val * K)) * s2
    )
    h4 = -f * p3 - c * d
    h5 = -(1 / d2_mu) * (
        (h4 * (u2_mu + mu_bar_val * h) / (sigma * s1))
        + (u3_mu - (h4 / sigma) * (u2_mu - mu_bar_val * K)) * s2
    )
    h6 = (1 / d2_mu) * (
        (s1 * h4 * (u2_mu - mu_bar_val * h) / (sigma))
        + (u3_mu - (h4 / sigma) * (u2_mu - mu_bar_val * K)) * s2
    )

    # Don't use mu quantities
    h7 = c * (u1 - mu_bar_val * h) / (d1 * s1)
    h8 = -s1 * c * (u1 + mu_bar_val * h) / (d1)
    h9 = (u2 + mu_bar_val * h) / (d2 * s1)
    h10 = -s1 * (u2 - mu_bar_val * h) / (d2)

    a1_mu = (
        (h1 / sigma) * ((1 - s2 * s2) / (2 * K))
        + h2 * ((1 - s2 * s1) / (K + h))
        + h3 * ((1 - s2 / s1) / (K - h))
    )
    a2_mu = (
        (h4 / sigma) * ((1 - s2 * s2) / (2 * K))
        + h5 * ((1 - s2 * s1) / (K + h))
        + h6 * ((1 - s2 / s1) / (K - h))
    )
    a1 = h7 * ((1 - s2 * s1) / (K + h)) + h8 * ((1 - s2 / s1) / (K - h))
    a2 = h9 * ((1 - s2 * s1) / (K + h)) + h10 * ((1 - s2 / s1) / (K - h))

    # Calculate the surface albedos ( 3.17- 3.20)
    # (upward diffuse fluxes per unit incident direct beam and diffuse flux)
    I_up_lambda_mu = h1 / sigma + h2 + h3
    I_up_lambda = h7 + h8

    # (downward diffuse fluxes per unit incident direct beam and diffuse radiation)
    I_down_lambda_mu = (h4 / sigma) * np.exp(-K * (L + S)) + h5 * s1 + h6 / s1
    I_down_lambda = h9 * s1 + h10 / s1

    # Calculate same per incident flux (3.21-3.22 )
    # (direct beam and diffuse fluxes absorbed by the vegetation, per unit incident flux)
    vector_I_lambda_mu = (
        1
        - I_up_lambda_mu
        - (1 - a_g_lambda) * I_down_lambda_mu
        - (1 - a_g_lambda_mu) * np.exp(-K * (L + S))
    )
    vector_I_lambda = 1 - I_up_lambda - (1 - a_g_lambda) * I_down_lambda
    # Save intermediate results
    # State.vector_I_lambda_mu[i] = vector_I_lambda_mu
    # State.vector_I_lambda[i] = vector_I_lambda

    # The absorption of direct beam radiation by sunlit leaves ( 3.23 )
    vector_I_sun_lambda_mu = (1 - omega_lambda) * (
        1 - s2 + (1 / mu_bar_val) * (a1_mu + a2_mu)
    )
    # For shaded leaves is (3.24)
    vector_I_shade_lambda_mu = vector_I_lambda_mu - vector_I_sun_lambda_mu

    # For diffuse radiation, the absorbed radiation for sunlit leaves is (3.27)
    vector_I_sun_lambda = (1 - omega_lambda) * ((1 / mu_bar_val) * (a1 + a2))
    # For shaded leaves ( 3.28 )
    vector_I_shade_lambda = vector_I_lambda - vector_I_sun_lambda

    # Calculate the canopy fluxes with clm5 eq, 3.1/3.2
    # dI/d(L+S) -> fraction transmitted, 1 layer assumption:
    # dI_up/d(L+S) = (L+S)*I_up
    omega = omega_lambda
    Beta = omega_lambda_beta_lambda / omega
    Beta_0 = omega_lambda_beta_lambda_0 / omega

    # Model 0: (dI/d(L+S) -> -I)
    if model_up_down_flux == 0:
        z_minus = -mu_bar_val * (-1) + (1 - (1 - Beta) * omega)
        z_plus = mu_bar_val * (-1) + (1 - (1 - Beta) * omega)
        z1 = omega * mu_bar_val * K * np.exp(-K * (L + S))
        I_up = (1 / (1 - omega * omega * Beta * Beta / (z_minus * z_plus))) * (
            omega * Beta * z1 * (1 - Beta_0) / (z_minus * z_plus)
            + z1 * Beta_0 / z_minus
        )
        I_down = omega * Beta * I_up / z_plus + z1 * (1 - Beta_0) / z_plus

    # Model 1: (dI/d(L+S) -> -I_0 = -1)
    if model_up_down_flux == 1:
        neg = 1
        z0 = 1 - (1 - Beta) * omega
        z1 = omega * mu_bar_val * K * np.exp(-K * (L + S))
        I_down = (1 / (1 - omega * omega * Beta * Beta / (z0 * z0))) * (
            (omega * Beta / z0) * (z1 * (1 - Beta_0) / z0 - mu_bar_val / z0)
            + z1 * (1 - Beta_0) / z0
            + mu_bar_val / z0
        )
        # If it's night, no incoming fluxes
        if mu <= 0.00:
            I_down = 0.0
        I_up = omega * Beta * I_down / z0 + z1 * (Beta_0) / z0 - mu_bar_val / z0

    # Upgrade to Rk4 with better canopy model!!

    # If it's night, no incoming fluxs
    if mu <= 0.00:
        vector_I_sun_lambda_mu = 0.0
        vector_I_shade_lambda_mu = 0.0
        vector_I_sun_lambda = 0.0
        vector_I_shade_lambda = 0.0

    # If close to sunset for fixed output (corrected by atompshere model anyway)
    cuttoff = 2
    if np.fabs(I_up) > cuttoff:
        I_up = I_up / np.fabs(I_up) * (cuttoff)
    if np.fabs(I_down) > cuttoff:
        I_down = I_down / np.fabs(I_down) * (cuttoff)
    if np.fabs(vector_I_sun_lambda_mu) > cuttoff:
        vector_I_sun_lambda_mu = (
            vector_I_sun_lambda_mu / np.fabs(vector_I_sun_lambda_mu) * (cuttoff)
        )
    if np.fabs(vector_I_shade_lambda_mu) > cuttoff:
        vector_I_shade_lambda_mu = (
            vector_I_shade_lambda_mu / np.fabs(vector_I_shade_lambda_mu) * (cuttoff)
        )
    if np.fabs(vector_I_sun_lambda) > cuttoff:
        vector_I_sun_lambda = (
            vector_I_sun_lambda / np.fabs(vector_I_sun_lambda) * (cuttoff)
        )
    if np.fabs(vector_I_shade_lambda) > cuttoff:
        vector_I_shade_lambda = (
            vector_I_shade_lambda / np.fabs(vector_I_shade_lambda) * (cuttoff)
        )

    return (
        I_up,
        I_down,
        vector_I_sun_lambda_mu,
        vector_I_shade_lambda_mu,
        vector_I_sun_lambda,
        vector_I_shade_lambda,
        # Save intermediate results
        vector_I_lambda_mu,
        vector_I_lambda,
        a_g_lambda_mu,
        a_g_lambda,
        I_down_lambda_mu,
        I_down_lambda,
    )


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
