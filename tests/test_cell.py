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

def test_fodder_savannah():
    savannah_cell = cell.Savannah()
    assert savannah_cell.current_fodder == 300

def test_gen_fodder_savannah():
    savannah_cell = cell.Savannah()
    savannah_cell.update_parameters({"f_max": 300, "alpha": 0})
    savannah_cell.gen_fodder_sav()
    assert savannah_cell.current_fodder == 300

def test_gen_fodder_jung():
    jun_cell = cell.Jungle()
    jun_cell.current_fodder = 700
    jun_cell.gen_fodder_jung()
    assert jun_cell.current_fodder == jun_cell.param["f_max"]


def test_aging():
    jungle_cell = cell.Jungle()
    jungle_cell.add_animal(
        [
            {"species": "Carnivore", "age": 10, "weight": 20},
            {"species": "Carnivore", "age": 10, "weight": 20},
            {"species": "Herbivore", "age": 10, "weight": 20},
        ]
    )
    jungle_cell.aging()
    for class_name in jungle_cell.animal_classes.values():
        for animal in class_name:
            assert animal.age == 11



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


def test_propensity_ocean_cell():
    ocean_cell = cell.Ocean()
    ocean_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Herbivore", "age": 5, "weight": 20},
        ]
    )
    for class_list in ocean_cell.animal_classes.values():
        for animal in class_list:
            assert ocean_cell.propensity(specie=animal) == 0

def test_propensity():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 20}])
    for class_list in savannah_cell.animal_classes.values():
        for animal_class in class_list:

            savannah_cell.compute_relative_abundance(animal_class)
            assert savannah_cell.propensity(animal_class) == 1

def test_update_parameters():
    savannah_cell = cell.Savannah()
    savannah_cell.update_parameters({"f_max": 200, "alpha": 0.4})
    assert savannah_cell.param["f_max"] == 200 and savannah_cell.param["alpha"] == 0.4

def test_update_parameters_try_except():
    savannah_cell = cell.Savannah()
    try:
        savannah_cell.update_parameters({"max": 200, "lpha": 0.4})
    except ValueError as ve:
        print(ve)

def test_update_parameters_neg():
    savannah_cell = cell.Savannah()
    try:
        savannah_cell.update_parameters({"f_max": -200, "alpha": -0.4})
    except ValueError as ve:
        print(ve)

def test_add_animal_none_species():
    savannah_cell = cell.Savannah()
    try:
        savannah_cell.add_animal([{"species": "Amir", "age": 10, "weight": 20}])
    except ValueError as ve:
        print(ve)
def test_add_animal_none_age_and_weight():
    savannah_cell = cell.Savannah()
    try:
        savannah_cell.add_animal([{"species": "Carnivore"}])
    except KeyError as ve:
        print(ve)
def test_num_animals_per_cell():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Herbivore", "age": 5, "weight": 20},
        ]
    )
    assert savannah_cell.num_animals_per_cell() == 3

def test_num_sepcies_per_cell():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Herbivore", "age": 5, "weight": 20},
        ]
    )
    assert savannah_cell.num_sepcies_per_cell() == (1,2)

def test_compute_relative_abundance_Herbivore():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal([{"species": "Herbivore", "age": 5, "weight": 20}])
    for class_list in savannah_cell.animal_classes.values():
        for animal_class in class_list:
            assert savannah_cell.compute_relative_abundance(animal_class) == 0

def test_compute_relative_abundance_Carnivore():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal(
        [
         {"species": "Carnivore", "age": 5, "weight": 10},
         ])
    for class_list in savannah_cell.animal_classes.values():
        for animal_class in class_list:
            assert savannah_cell.compute_relative_abundance(animal_class) == 0

def test_eat_herbivore_none_fodder():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal(
        [
            {"species": "Herbivore", "age": 5, "weight": 10},
        ])
    savannah_cell.eat_herbivore()
    assert savannah_cell.current_fodder == 0

def test_eat_herbivore():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 11
    savannah_cell.add_animal(
        [
            {"species": "Herbivore", "age": 5, "weight": 10},
        ])
    savannah_cell.eat_herbivore()
    assert savannah_cell.current_fodder == 1

def test_eat_herbivore_all():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 9
    savannah_cell.add_animal(
        [
            {"species": "Herbivore", "age": 5, "weight": 10},
        ])
    savannah_cell.eat_herbivore()
    assert savannah_cell.current_fodder == 0

def test_eat_carnivore():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 10},
            {"species": "Herbivore", "age": 5, "weight": 10}
        ])
    for animal in savannah_cell.animal_classes["Carnivore"]:
        animal.fitness = 30
        savannah_cell.eat_carnivore()
        assert animal.weight == 10