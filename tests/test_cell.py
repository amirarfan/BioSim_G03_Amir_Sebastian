# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

import biosim.cell as cell


def test_fodder_Mountain():
    mountain_cell = cell.Mountain()
    assert mountain_cell.current_fodder == 0

def test_fodder_Ocean():
    ocean_cell = cell.Ocean()
    assert ocean_cell.current_fodder == 0


def test_gen_fodder_jung():
    jun_cell = cell.Jungle()
    jun_cell.current_fodder = 700
    jun_cell.gen_fodder_jung()
    assert jun_cell.current_fodder == jun_cell.param["f_max"]



def test_gen_fodder_Savannah():
    savannah_cell = cell.Savannah()
    assert savannah_cell.current_fodder == 300
