#!/usr/bin/env python3
"""
Test the Radiation Fluxes Module

Based on SRC/model_radiation_fluxes.py

To test specifically
pytest -s -q -rA tests/test_radiation.py
"""

# Load in Modules
import os
import sys
import pytest

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "SRC")
sys.path.append(mymodule_dir)
import model_albedo
import model_radiation_fluxes as mrf

mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization

# Timestep to stop on
# dT = 1200
dT = 10000


@pytest.fixture
def test_run():
    # Initialize Model
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)

    # Run Routine from timestep
    for i in range(dT + 1):
        model_albedo.run_albedo_model(State, Grid, App, i)
        mrf.run_radiation_model(State, Grid, App, i)
    # print(State.radiation.T_rad[dT-1])
    # return App, State, Grid
    return State, Grid


# Standalone Test
def test_r_vis_calc():
    """Tests the r_vis_calc helper function"""
    assert 0.17639 == mrf.r_vis_calc(0, 0)
    assert mrf.r_vis_calc(100, 0.00) == mrf.r_vis_calc(100, -5)
    assert mrf.r_vis_calc(100, 1.00) == mrf.r_vis_calc(100, 12)
    # model_radiation_fluxes.r_nir_calc(1, 0.5)
    # State_temp = test_run # Return T
    # print(State_temp.radiation.T_rad[dT-1])


# Standalone Test
def test_r_nir_calc():
    """Tests the r_nir_calc helper function"""
    assert 0.29548 == mrf.r_nir_calc(0, 0)
    assert 0.29548 == mrf.r_nir_calc(0, 99999)
    assert 0.29548 == mrf.r_nir_calc(0, -99999)
    assert 0.01 == mrf.r_nir_calc(100, 9999)
    assert 0.99 == mrf.r_nir_calc(100, -9999)


# Standalone test
def test_ratio_test():
    """Check that r_nir_calc GEQ to r_vis_calc"""
    assert mrf.r_nir_calc(100, 0.5) >= mrf.r_vis_calc(100, 0.5)
    assert mrf.r_nir_calc(50, 0.5) >= mrf.r_vis_calc(50, 0.5)
    assert mrf.r_nir_calc(200, 0.5) >= mrf.r_vis_calc(200, 0.5)
    assert mrf.r_nir_calc(25, 0.5) >= mrf.r_vis_calc(25, 0.5)


# Fixture Test
def test_radiation_hard_code(test_run):
    """
    Test the STATE variables output
    from radiation module at timestep specified
    Output based tests

    The point of this test is to make sure nobody else's changes messes with the Radiation Script
    """
    # Hard Coded for dT = 1200
    dt = 1200

    # STATE output from fixture
    State_t, Grid_t = test_run

    # Initial Results test
    # To make sure that future changes do not change the results
    # print(State_t.radiation.vis_in[dt])
    # print(State_t.radiation.vis_out[dt])
    # print(State_t.radiation.IR_in[dt])
    # print(State_t.radiation.IR_out[dt])
    # print(State_t.radiation.T_g[dt])
    # print(State_t.radiation.total_solar_radiation[dt])
    # print(State_t.radiation.solar_dir_tot[dt])
    # print(State_t.radiation.solar_dif_tot[dt])
    # print(State_t.radiation.tot_sol_rad_abs_v[dt])
    # print(State_t.radiation.tot_sol_rad_abs_g[dt])
    # print(State_t.radiation.abs_vis_rad_sun[dt])
    # print(State_t.radiation.abs_vis_rad_sha[dt])
    # print(State_t.radiation.lw_net_rad[dt])
    # print(State_t.radiation.T_rad[dt])
    # print(State_t.radiation.T_v[dt])
    # print(State_t.radiation.lw_net_rad_gro[dt])
    # print(State_t.radiation.lw_net_rad_veg[dt])

    results_dt = [
        48.04740972,
        39.91779167,
        266.2020833,
        277.0527778,
        272.05,
        314.24949302000005,
        213.4671559390681,
        100.78233708093195,
        0.0,
        18.828683416743658,
        0.0,
        0.0,
        10.850694499999975,
        264.3899011648312,
        264.2755229359296,
        33.26005597707024,
        -21.399412698558734,
    ]

    assert results_dt[0] == pytest.approx(State_t.radiation.vis_in[dt], 10**-4)
    assert results_dt[1] == pytest.approx(State_t.radiation.vis_out[dt], 10**-4)
    assert results_dt[2] == pytest.approx(State_t.radiation.IR_in[dt], 10**-4)
    assert results_dt[3] == pytest.approx(State_t.radiation.IR_out[dt], 10**-4)
    assert results_dt[4] == pytest.approx(State_t.radiation.T_g[dt], 10**-4)
    assert results_dt[5] == pytest.approx(
        State_t.radiation.total_solar_radiation[dt], 10**-4
    )
    assert results_dt[6] == pytest.approx(State_t.radiation.solar_dir_tot[dt], 10**-4)
    assert results_dt[7] == pytest.approx(State_t.radiation.solar_dif_tot[dt], 10**-4)
    assert results_dt[8] == pytest.approx(
        State_t.radiation.tot_sol_rad_abs_v[dt], 10**-4
    )
    assert results_dt[9] == pytest.approx(
        State_t.radiation.tot_sol_rad_abs_g[dt], 10**-4
    )
    assert results_dt[10] == pytest.approx(
        State_t.radiation.abs_vis_rad_sun[dt], 10**-4
    )
    assert results_dt[11] == pytest.approx(
        State_t.radiation.abs_vis_rad_sha[dt], 10**-4
    )
    assert results_dt[12] == pytest.approx(State_t.radiation.lw_net_rad[dt], 10**-4)
    assert results_dt[13] == pytest.approx(State_t.radiation.T_rad[dt], 10**-4)
    assert results_dt[14] == pytest.approx(State_t.radiation.T_v[dt], 10**-4)
    assert results_dt[15] == pytest.approx(
        State_t.radiation.lw_net_rad_gro[dt], 10**-4
    )
    assert results_dt[16] == pytest.approx(
        State_t.radiation.lw_net_rad_veg[dt], 10**-4
    )
    # assert 264.39 == pytest.approx(State_t.radiation.T_rad[dT], 10**-2)

    # Make sure nobody changed the deltaT
    assert 0.01 == Grid_t.dt_approx

    # Original test
    assert 264.39 == pytest.approx(State_t.radiation.T_rad[dt], 10**-2)


def test_radiation_soft_code(test_run):
    """
    Test the STATE variables output
    from radiation module at timestep specified
    Logic based tests
    """
    # STATE output from fixture
    State_t, Grid_t = test_run

    # Timestep
    ts = Grid_t.dt_approx

    # Make sure the input data is read in correctly
    assert State_t.data.vis_in[1] == State_t.radiation.vis_in[int(1 / ts)]
    assert State_t.data.vis_in[12] == State_t.radiation.vis_in[int(12 / ts)]
    assert State_t.data.vis_in[50] == State_t.radiation.vis_in[int(50 / ts)]
    assert State_t.data.vis_out[2] == State_t.radiation.vis_out[int(2 / ts)]
    assert State_t.data.vis_out[15] == State_t.radiation.vis_out[int(15 / ts)]
    assert State_t.data.vis_out[17] == State_t.radiation.vis_out[int(17 / ts)]
    assert State_t.data.IR_in[4] == State_t.radiation.IR_in[int(4 / ts)]
    assert State_t.data.IR_in[43] == State_t.radiation.IR_in[int(43 / ts)]
    assert State_t.data.IR_out[33] == State_t.radiation.IR_out[int(33 / ts)]
    assert State_t.data.IR_out[77] == State_t.radiation.IR_out[int(77 / ts)]

    # Tests to Run
    """ Need to parameterize these so they rerun for all dTs """
    assert State_t.radiation.lw_net_rad[dT] == pytest.approx(
        (State_t.radiation.lw_net_rad_gro[dT] + State_t.radiation.lw_net_rad_veg[dT]),
        0.1,
    )
    assert State_t.radiation.total_solar_radiation[dT] == pytest.approx(
        (State_t.radiation.solar_dir_tot[dT] + State_t.radiation.solar_dif_tot[dT]),
        0.0001,
    )
    assert State_t.radiation.tot_sol_rad_abs_v[dT] == pytest.approx(
        (State_t.radiation.abs_vis_rad_sun[dT] + State_t.radiation.abs_vis_rad_sha[dT]),
        0.0001,
    )
    assert State_t.radiation.T_rad[dT] > State_t.radiation.T_v[dT]


# For running solo
if __name__ == "__main__":
    # @pytest.fixture
    test_run()
    test_r_vis_calc()
    test_r_nir_calc()
    test_ratio_test()
    test_radiation_hard_code(test_run())
    test_radiation_soft_code(test_run())
