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
import model_evaporation as me

mymodule_dir = os.path.join(script_dir, "..", "EXAMPLES")
sys.path.append(mymodule_dir)
import input_script
import initialization


def test_evaporation():
    #Initialize
    parameters = input_script.clm_parameters()
    App, State, Grid = initialization.initialize_data(parameters)

    print(me.air_res(1,2,3)[1])
    #Test helper functions
    assert 4.3328664087712 == pytest.approx(me.psi(-1))
    


if __name__ == "__main__":
    test_evaporation()
