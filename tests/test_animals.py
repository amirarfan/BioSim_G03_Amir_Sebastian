# -*- coding: utf-8 -*-

__author__ = 'Amir Arfan, Sebastian Becker'
__email__ = 'amar@nmbu.no, sebabeck@nmbu.no'

import biosim.animals as animal


def test_Herbivore_age():
    # Test for animal age is equal to 0
    herb = animal.Herbivore()
    assert herb.age == 0


def test_animal_actually_ages():
    herb = animal.Herbivore()
    first_age = herb.age
    herb.add_age()
    second_age = herb.age
    assert first_age < second_age


def test_animal_weight():
    herb = animal.Herbivore()
    assert herb.weight != None
    assert herb.weight != 0


def test_animal_fitness():
    herb = animal.Herbivore()
    assert herb.fitness != 0


def test_move_probability_herb():
    herb = animal.Herbivore()
    bool_val = herb.move_probability()
    assert bool_val == True or bool_val == False
