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


def test_gen_fodder_savannah():
    savannah_cell = cell.Savannah()
    assert savannah_cell.current_fodder == 300


def test_aging():
    jungle_cell = cell.Jungle()
    jungle_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
        ]
    )
    jungle_cell.aging()
    for class_name in jungle_cell.animal_classes.values():
        for animal in class_name:
            assert animal.age == 6


def test_annual_weightloss():
    jungle_cell = cell.Jungle()
    jungle_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
        ]
    )
    jungle_cell.annual_weight_loss()
    for class_name in jungle_cell.animal_classes.values():
        for animal in class_name:
            assert animal.weight != 20


def test_propensity():
    ocean_cell = cell.Ocean()
    ocean_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
        ]
    )
    for class_list in ocean_cell.animal_classes.values():
        for animal in class_list:
            assert ocean_cell.propensity(specie=animal) == 0
