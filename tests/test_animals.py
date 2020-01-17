# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from biosim.animals import Herbivore, Carnivore
import numpy
import pytest


@pytest.fixture
def plain_herbivore():
    return Herbivore()


def test_herbivore_age(plain_herbivore):
    # Test for animal age is equal to 0
    assert plain_herbivore.age == 0


def test_herbivore_custom_neg_age(plain_herbivore):
    try:
        plain_herbivore(age=-1)
    except ValueError as ve:
        print(ve)


def test_herbivore_custom_pos_age():
    herb = Herbivore(age=2)
    assert herb.age == 2


def test_herbivore_setter_method_age(plain_herbivore):
    plain_herbivore.age = 2
    assert plain_herbivore.age == 2


def test_herbivore_setter_method_neg_age(plain_herbivore):
    try:
        plain_herbivore.age = -1
    except ValueError as ve:
        print(ve)


def test_herbivore_non_int_setter_age(plain_herbivore):
    try:
        plain_herbivore.age = 2.1
    except ValueError as ve:
        print(ve)


def test_herbivore_actually_ages(plain_herbivore):
    first_age = plain_herbivore.age
    plain_herbivore.add_age()
    second_age = plain_herbivore.age
    assert first_age < second_age


def test_herbivore_continual_aging():
    herb = Herbivore()
    for i in range(10):
        herb.add_age()
        assert i + 1 == herb.age


def test_herbivore_weight(plain_herbivore):
    assert plain_herbivore.weight is not None
    assert plain_herbivore.weight != 0


def test_herbivore_change_weight(plain_herbivore):
    plain_herbivore.weight = 2
    assert plain_herbivore.weight == 2


def test_herbivore_neg_weight():
    # One could also use try except here
    with pytest.raises(ValueError) as ve:
        Herbivore(-1)


def test_herbivore_custom_pos_weight():
    herb = Herbivore(weight=20)
    assert herb.weight == 20


def test_herbivore_custom_weight_setter(plain_herbivore):
    with pytest.raises(ValueError) as ve:
        plain_herbivore.weight = -20


def test_herbivore_fitness_changes_with_weight(plain_herbivore):
    before_fitness = plain_herbivore.fitness
    plain_herbivore.weight = 30
    after_fitness = plain_herbivore.fitness
    assert before_fitness != after_fitness


def test_herbivore_fitness_not_zero():
    herb = Herbivore()
    assert herb._fitness != 0


def test_fitness_setter_negval(plain_herbivore):
    with pytest.raises(ValueError) as ve:
        plain_herbivore.fitness = -1


def test_non_existing_parameter_herbivore(plain_herbivore):
    with pytest.raises(ValueError):
        plain_herbivore.update_parameters({"non_exist": 20})


def test_negative_parameter_herbivore(plain_herbivore):
    with pytest.raises(ValueError):
        plain_herbivore.update_parameters({"sigma_birth: -20"})
   


def test_eta_greater_than_one_herbivore():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"eta": 2})
    except ValueError:
        print("Successfully returned ValueError for eta > 1")


def test_deltaphimax_negative():
    herb = animal.Herbivore()
    try:
        herb.update_parameters({"DeltaPhiMax": -1})
    except ValueError as ve:
        print(ve)


def test_parameters_actually_update():
    herb = animal.Herbivore()
    prev_param = herb.param.copy()
    herb.update_parameters({"DeltaPhiMax": 5})
    assert prev_param != herb.param


def test_determine_death_zero_fitness():
    herb = animal.Herbivore()
    herb.fitness = 0
    assert herb.determine_death() is True


def test_determine_death_is_bool():
    herb = animal.Herbivore()
    assert type(herb.determine_death()) == numpy.bool_


def test_determine_birth_no_animals():
    herb = animal.Herbivore()
    assert herb.determine_birth(0) is False


def test_determine_birth_is_bool():
    herb = animal.Herbivore()
    herb.weight = 100
    assert type(herb.determine_birth(100)) == numpy.bool_


def test_move_probability_herb():
    herb = animal.Herbivore()
    bool_val = herb.determine_to_move()
    assert type(bool_val) == numpy.bool_


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


def test_carnivore_birth_decrease_weight():
    carn = animal.Carnivore()
    prev_weight = carn.weight
    carn.decrease_birth_weight(20)
    assert carn.weight < prev_weight


def test_decrease_annual_weight():
    carn = animal.Carnivore()
    prev_weight = carn.weight
    carn.decrease_annual_weight()
    assert carn.weight < prev_weight


def test_kill_probability_gfherb():
    # Herbivore has greater fitness
    carn = animal.Carnivore()
    prob = carn._compute_kill_prob(0.4, 0.9, 10)
    assert prob == 0


def test_kill_probability_gfcarn():
    # Carnivore has greater fitness
    carn = animal.Carnivore()
    prob = carn._compute_kill_prob(10, 0.1, 5)
    assert prob == 1


def test_bool_carnivore_det_kill():
    carn = animal.Carnivore()
    kill_prob = carn.determine_kill(0.20)
    assert type(kill_prob) is numpy.bool_


def test_fitness_weight_zero():
    herb = animal.Herbivore()
    assert herb._calculate_fitness(0, 1) == 0
