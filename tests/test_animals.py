# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

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
    herb.weight = 2
    print(herb._fitness)
    assert herb.weight == 2


def test_fitness_changes_with_weight():
    herb = animal.Herbivore()
    before_fitness = herb._fitness
    herb.weight = 30
    after_fitness = herb._fitness
    assert before_fitness != after_fitness


def test_animal_fitness():
    herb = animal.Herbivore()
    assert herb._fitness != 0


def test_non_existing_parameter():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"non_exist": 20})
    except ValueError as ve:
        print(ve)


def test_negative_parameter():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"sigma_birth": -20})
    except ValueError as ve:
        print(ve)


def test_eta_greater_than_one():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"eta": 2})
    except ValueError:
        print("Successfully returned ValueError for eta > 1")


def test_move_probability_herb():
    herb = animal.Herbivore()
    bool_val = herb.determine_to_move()
    assert bool_val is True or bool_val is False
