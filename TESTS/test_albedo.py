#!/usr/bin/env python3
"""
Test for verifying the albedo module

#Requires linking to the defintions:
SRC/model_albedo.py
"""

import os
import sys
import pytest

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
    assert -1.3316125255128681 == pytest.approx(model_albedo.lambda_val(5), 1e-6)
    assert -1.288300049079258 == pytest.approx(model_albedo.lambda_val(7.5), 1e-6)

    # Test integrated function: *MAY FAIL IF PARAMETERS ARE ALTERED*
    assert -0.44487413335802434 == pytest.approx(
        model_albedo.solar_zenith_angle(State, Grid, App, 0), 1e-6
    )
    assert -0.8066919738836718 == pytest.approx(
        model_albedo.solar_zenith_angle(State, Grid, App, 1), 1e-6
    )


if __name__ == "__main__":
    test_albedo()
