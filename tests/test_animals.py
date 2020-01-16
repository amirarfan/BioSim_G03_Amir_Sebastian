# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

import biosim.animals as animal


def test_herbivore_age():
    # Test for animal age is equal to 0
    herb = animal.Herbivore()
    assert herb.age == 0


def test_herbivore_actually_ages():
    herb = animal.Herbivore()
    first_age = herb.age
    herb.add_age()
    second_age = herb.age
    assert first_age < second_age

def test_herbivore_continual_aging():
    herb = animal.Herbivore()
    for i in range(10):
        herb.add_age()
        assert i+1 == herb.age



def test_herbivore_weight():
    herb = animal.Herbivore()
    assert herb.weight is not None
    assert herb.weight != 0


def test_herbivore_change_weight():
    herb = animal.Herbivore()
    herb.weight = 2
    print(herb._fitness)
    assert herb.weight == 2


def test_herbivore_fitness_changes_with_weight():
    herb = animal.Herbivore()
    before_fitness = herb._fitness
    herb.weight = 30
    after_fitness = herb._fitness
    assert before_fitness != after_fitness


def test_herbivore_fitness():
    herb = animal.Herbivore()
    assert herb._fitness != 0


def test_non_existing_parameter_herbivore():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"non_exist": 20})
    except ValueError as ve:
        print(ve)


def test_negative_parameter_herbivore():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"sigma_birth": -20})
    except ValueError as ve:
        print(ve)


def test_eta_greater_than_one_herbivore():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"eta": 2})
    except ValueError:
        print("Successfully returned ValueError for eta > 1")


def test_move_probability_herb():
    herb = animal.Herbivore()
    bool_val = herb.determine_to_move()
    assert bool_val is True or bool_val is False


def test_carnivore_age():
    carn = animal.Carnivore()
    assert carn.age == 0


def test_carnivore_fitness_change_when_eat():
    carn = animal.Carnivore()
    prev_fitness = carn.fitness
    carn.increase_eat_weight(20)
    assert carn.fitness != prev_fitness


def test_carnivore_weight_change_when_eat():
    carn = animal.Carnivore()
    prev_weight = carn.weight
    carn.increase_eat_weight(10)
    assert prev_weight < carn.weight


def test_carnivore_actually_ages():
    carn = animal.Carnivore()
    prev_age = carn.age
    carn.add_age()
    assert carn.age > prev_age


def test_bool_carnivore_det_kill():
    carn = animal.Carnivore()
    kill_prob = carn.determine_kill(0.20)
    assert kill_prob == True or kill_prob == False
