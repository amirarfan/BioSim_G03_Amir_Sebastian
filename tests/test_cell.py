# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from biosim.cell import Mountain, Ocean, Savannah, Jungle, Desert
from biosim.animals import Herbivore, Carnivore
import pytest


@pytest.fixture
def plain_mountain():
    return Mountain()


@pytest.fixture
def plain_ocean():
    return Ocean()


@pytest.fixture
def plain_savannah():
    return Savannah()


@pytest.fixture
def plain_jungle():
    return Jungle()


@pytest.fixture
def plain_desert():
    return Desert()


@pytest.fixture
def populated_jungle():
    jun_cell = Jungle()
    jun_cell.add_animal(
        [
            {"species": "Carnivore", "age": 10, "weight": 20},
            {"species": "Carnivore", "age": 10, "weight": 20},
            {"species": "Herbivore", "age": 10, "weight": 20},
        ]
    )
    return jun_cell


@pytest.fixture
def populated_ocean():
    ocean_cell = Ocean()
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    ocean_cell.insert_animal(herbivores)
    ocean_cell.insert_animal(carnivores)
    return ocean_cell

@pytest.fixture
def populated_


def test_fodder_mountain(plain_mountain):
    assert plain_mountain.current_fodder == 0


def test_fodder_ocean(plain_ocean):
    assert plain_ocean.current_fodder == 0


def test_fodder_savannah(plain_savannah):
    assert plain_savannah.current_fodder == 300


def test_gen_fodder_update_par_savannah(plain_savannah):
    plain_savannah.update_parameters({"f_max": 300, "alpha": 0})
    plain_savannah.gen_fodder_sav()
    assert plain_savannah.current_fodder == 300


def test_gen_fodder_jung(plain_jungle):
    plain_jungle.current_fodder = 700
    plain_jungle.gen_fodder_jung()
    assert plain_jungle.current_fodder == plain_jungle.param["f_max"]


def test_aging_cell(populated_jungle):
    prev_ages = [
        animal.age
        for class_type in populated_jungle.animal_classes.values()
        for animal in class_type
    ]
    populated_jungle.aging()

    new_ages = [
        animal.age
        for class_type in populated_jungle.animal_classes.values()
        for animal in class_type
    ]

    for old_age in prev_ages:
        for new_age in new_ages:
            assert new_age > old_age


def test_annual_weightloss(populated_jungle):
    old_weights = [
        animal.weight
        for class_type in populated_jungle.animal_classes.values()
        for animal in class_type
    ]
    populated_jungle.annual_weight_loss()

    new_weights = [
        animal.weight
        for class_type in populated_jungle.animal_classes.values()
        for animal in class_type
    ]

    for old_weight in old_weights:
        for new_weight in new_weights:
            assert new_weight < old_weight


def test_propensity_ocean_cell(populated_ocean):
    for class_list in populated_ocean.animal_classes.values():
        for animal in class_list:
            assert populated_ocean.propensity(specie=animal) == 0


def test_propensity():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 20}]
    )
    for class_list in savannah_cell.animal_classes.values():
        for animal_class in class_list:
            savannah_cell.compute_relative_abundance(animal_class)
            assert savannah_cell.propensity(animal_class) == 1


def test_update_parameters():
    savannah_cell = cell.Savannah()
    savannah_cell.update_parameters({"f_max": 200, "alpha": 0.4})
    assert (
            savannah_cell.param["f_max"] == 200
            and savannah_cell.param["alpha"] == 0.4
    )


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
        savannah_cell.add_animal(
            [{"species": "Amir", "age": 10, "weight": 20}]
        )
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
    assert savannah_cell.num_sepcies_per_cell() == (1, 2)


def test_compute_relative_abundance_Herbivore():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 20}]
    )
    for class_list in savannah_cell.animal_classes.values():
        for animal_class in class_list:
            assert savannah_cell.compute_relative_abundance(animal_class) == 0


def test_compute_relative_abundance_Carnivore():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal(
        [{"species": "Carnivore", "age": 5, "weight": 10}]
    )
    for class_list in savannah_cell.animal_classes.values():
        for animal_class in class_list:
            assert savannah_cell.compute_relative_abundance(animal_class) == 0


def test_eat_herbivore_none_fodder():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 0
    savannah_cell.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 10}]
    )
    savannah_cell.eat_herbivore()
    assert savannah_cell.current_fodder == 0


def test_eat_herbivore():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 11
    savannah_cell.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 10}]
    )
    savannah_cell.eat_herbivore()
    assert savannah_cell.current_fodder == 1


def test_eat_herbivore_all():
    savannah_cell = cell.Savannah()
    savannah_cell.current_fodder = 9
    savannah_cell.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 10}]
    )
    savannah_cell.eat_herbivore()
    assert savannah_cell.current_fodder == 0


def test_eat_carnivore():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 10},
            {"species": "Herbivore", "age": 5, "weight": 10},
        ]
    )
    for animal in savannah_cell.animal_classes["Carnivore"]:
        animal.fitness = 30
        savannah_cell.eat_carnivore()
        assert animal.weight > 10


def test_eat_carnivore_none_fodder():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 10},
            {"species": "Herbivore", "age": 5, "weight": 10},
        ]
    )
    for animal in savannah_cell.animal_classes["Carnivore"]:
        animal.fitness = 30
        prev_weight = animal.weight
        animal.update_parameters({"F": 0})
        savannah_cell.eat_carnivore()
        assert prev_weight == animal.weight


def test_annual_death():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [{"species": "Carnivore", "age": 5, "weight": 10}]
    )
    for animal in savannah_cell.animal_classes["Carnivore"]:
        animal.fitness = 0
        savannah_cell.annual_death()
        assert len(savannah_cell.animal_classes["Carnivore"]) == 0


def test_insert_animal():
    savannah_cell = cell.Savannah()
    animal = savannah_cell.allowed_species["Carnivore"]
    savannah_cell.insert_animal(animal())


def test_update_animal_parameters_in_cell():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 10},
            {"species": "Herbivore", "age": 5, "weight": 10},
        ]
    )
    savannah_cell.update_animal_parameters_in_cell("Carnivore", {"F": 0})
    assert savannah_cell.allowed_species["Carnivore"].param["F"] == 0


def test_desert():
    desert = cell.Desert()
    assert isinstance(desert, cell.Desert)


def test_delete_animal_not_in_list():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 10},
            {"species": "Carnivore", "age": 5, "weight": 10},
        ]
    )
    animal = savannah_cell.allowed_species["Herbivore"]
    try:
        savannah_cell.delete_animal(animal())
    except ValueError as ve:
        print(ve)


def test_delete_animal():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [{"species": "Carnivore", "age": 5, "weight": 10}]
    )
    for animal in savannah_cell.animal_classes["Carnivore"]:
        savannah_cell.delete_animal(animal)
    assert len(savannah_cell.animal_classes["Carnivore"]) == 0


def test_compute_move_prob():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [{"species": "Carnivore", "age": 5, "weight": 10}]
    )
    for animal in savannah_cell.animal_classes["Carnivore"]:
        assert savannah_cell.compute_move_prob(
            animal, [cell.Ocean(), cell.Ocean(), cell.Ocean(), cell.Ocean()]
        ) == [0, 0, 0, 0]


def test_migration():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [{"species": "Carnivore", "age": 5, "weight": 10}]
    )
    for animal in savannah_cell.animal_classes["Carnivore"]:
        animal.fitness = 1
        animal.update_parameters({"mu": 1})
    savannah_cell.migration(
        [cell.Savannah(), cell.Savannah(), cell.Savannah(), cell.Savannah()]
    )
    assert len(savannah_cell.animal_classes["Carnivore"]) == 0


def test_mating():
    savannah_cell = cell.Savannah()
    savannah_cell.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 70},
            {"species": "Carnivore", "age": 5, "weight": 70},
        ]
    )
    for animal in savannah_cell.animal_classes["Carnivore"]:
        animal.fitness = 1
        animal.update_parameters({"gamma": 1})
    savannah_cell.mating()
    assert (len(savannah_cell.animal_classes["Carnivore"])) > 2
