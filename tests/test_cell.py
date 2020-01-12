# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

import biosim.cell as cell

def test_fodder_Mountain():
    mountain_cell = cell.Mountain()
    assert mountain_cell.current_fodder == 0

def test_add_animal():
    cell.Cell
    assert ValueError # Hva er hensikten her??

def test_fodder_Ocean():
    ocean_cell = cell.Ocean()
    assert ocean_cell.relevant_fodder == 0

def test_gen_fodder_jung():
    jun_cell = cell.Jungle()
    assert jun_cell.current_fodder == fodder.param["f_max"]
    assert jun_cell.current_fodder != 0 # Denne blir unødvendig da du allerede tester at det er en verdi

def test_gen_fodder_Savannah():
    savannah_cell = cell.Savannah()
    assert savannah_cell.current_fodder == 300
    assert savannah_cell.current_fodder != None # Denne også
