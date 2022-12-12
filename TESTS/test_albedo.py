#!/usr/bin/env python3
"""
Test for verifying the albedo module

#Requires linking to the defintions:
SRC/model_albedo.py
"""

import os
import sys
import pytest
import pandas

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
import model_albedo

mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization


def test_albedo():

    # Build empty structures, App, State and Grid with blank data:
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)

    # Test standalone functions
    # print(str(model_albedo.lambda_val(5)))
    # print(str(model_albedo.lambda_val(7.5)))
    assert -1.3316125255128681 == pytest.approx(model_albedo.lambda_val(5), 1e-6)
    assert -1.288300049079258 == pytest.approx(model_albedo.lambda_val(7.5), 1e-6)

    # Test integrated function: *MAY FAIL IF PARAMETERS (dt,t0,tf) ARE ALTERED*
    # print(str(model_albedo.solar_zenith_angle(State, Grid, App, 0)))
    assert -0.44487413335802434 == pytest.approx(
        model_albedo.solar_zenith_angle(State, Grid, App, 0), 1e-6
    )
    # print(str(model_albedo.solar_zenith_angle(State, Grid, App, 10)))
    assert -0.8066245054020273 == pytest.approx(
        model_albedo.solar_zenith_angle(State, Grid, App, 10), 1e-6
    )

    # Solar Radiation:
    indx = 70  # choose something near mid-day
    model_albedo.solar(State, Grid, App, indx)

    # Canopy Radiative Model ( depends on solar mu )
    model_albedo.canopy(State, Grid, App, indx)

    # Test the outputs of the canopy model:
    # 1. Once verified these ouputs serve as our test comparisons / can be commented out
    # print(str(State.I_up_vis[indx]))
    # print(str(State.I_down_vis[indx]))
    # print(str(State.I_sun_vis_mu[indx]))
    # print(str(State.I_shade_vis_mu[indx]))
    # print(str(State.I_sun_vis[indx]))
    # print(str(State.I_shade_vis[indx]))
    # print(str(State.I_up_nir[indx]))
    # print(str(State.I_down_nir[indx]))
    # print(str(State.I_sun_nir_mu[indx]))
    # print(str(State.I_shade_nir_mu[indx]))
    # print(str(State.I_sun_nir[indx]))
    # print(str(State.I_shade_nir[indx]))
    results = [
        -0.7099550814113347,
        1.3608317801719236,
        0.27647399421923796,
        0.01789068813909972,
        0.1991337578687506,
        0.0562570423467294,
        -0.3800334786255217,
        1.508396203018973,
        0.19820921243675127,
        0.014941171424787958,
        0.14646425511922867,
        0.041630625045135705,
    ]

    # Test integrated function: *MAY FAIL IF PARAMETERS (dt,t0,tf) ARE ALTERED*
    assert results[0] == pytest.approx(State.I_up_vis[indx], 1e-6)
    assert results[1] == pytest.approx(State.I_down_vis[indx], 1e-6)
    assert results[2] == pytest.approx(State.I_sun_vis_mu[indx], 1e-6)
    assert results[3] == pytest.approx(State.I_shade_vis_mu[indx], 1e-6)
    assert results[4] == pytest.approx(State.I_sun_vis[indx], 1e-6)
    assert results[5] == pytest.approx(State.I_shade_vis[indx], 1e-6)
    assert results[6] == pytest.approx(State.I_up_nir[indx], 1e-6)
    assert results[7] == pytest.approx(State.I_down_nir[indx], 1e-6)
    assert results[8] == pytest.approx(State.I_sun_nir_mu[indx], 1e-6)
    assert results[9] == pytest.approx(State.I_shade_nir_mu[indx], 1e-6)
    assert results[10] == pytest.approx(State.I_sun_nir[indx], 1e-6)
    assert results[11] == pytest.approx(State.I_shade_nir[indx], 1e-6)


if __name__ == "__main__":
    test_albedo()
