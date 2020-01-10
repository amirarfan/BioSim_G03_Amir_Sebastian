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
    assert herb.weight is not None
    assert herb.weight != 0


def test_change_weight():
    herb = animal.Herbivore()
    first_fitness = herb.fitness
    herb.weight = 2
    assert herb.weight == 2 and first_fitness != herb.fitness


def test_animal_fitness():
    herb = animal.Herbivore()
    assert herb.fitness != 0


def test_move_probability_herb():
    herb = animal.Herbivore()
    bool_val = herb.determine_to_move()
    assert bool_val == True or bool_val == False
