#!/usr/bin/env python3
"""
Parts of Table 2.4 Atmospheric inputs;
Names are all lowercases.
"""
class atm_inputs:
    def __init__(self):
        self.constants: dict(str, float) = {
            "thickness" : 50,
            "roughness length":0.5
        }
