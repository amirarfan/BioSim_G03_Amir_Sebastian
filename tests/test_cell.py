# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from biosim.cell import Mountain, Ocean, Savannah, Jungle, Desert
from biosim.animals import Herbivore, Carnivore
import pytest
import numpy
import os


@pytest.fixture(autouse=True)
def reset_parameters():
    standard_parameters_herb =  {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.2,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "lambda": 1.0,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
        "DeltaPhiMax": 0,
    }
    standard_parameters_carn = {
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 60.0,
        "phi_age": 0.4,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "lambda": 1.0,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.9,
        "F": 50.0,
        "DeltaPhiMax": 10.0,
    }

    Herbivore().update_parameters(standard_parameters_herb)
    Carnivore().update_parameters(standard_parameters_carn)


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
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    jun_cell.insert_animal(herbivores)
    jun_cell.insert_animal(carnivores)
    return jun_cell


@pytest.fixture
def populated_desert():
    desert_cell = Desert()
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    desert_cell.insert_animal(herbivores)
    desert_cell.insert_animal(carnivores)
    return desert_cell


@pytest.fixture
def populated_savannah():
    savannah_cell = Savannah()
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    savannah_cell.insert_animal(herbivores)
    savannah_cell.insert_animal(carnivores)
    return savannah_cell


def test_fodder_mountain(plain_mountain):
    assert plain_mountain.current_fodder == 0


def test_fodder_ocean(plain_ocean):
    assert plain_ocean.current_fodder == 0


def test_gen_fodder_savannah(populated_savannah):
    populated_savannah.eat_herbivore()
    prev_fodder = populated_savannah.current_fodder
    populated_savannah.gen_fodder_sav()
    new_fodder = populated_savannah.current_fodder
    assert new_fodder > prev_fodder


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
    sum_old_weights = sum(
        [
            animal.weight
            for class_type in populated_jungle.animal_classes.values()
            for animal in class_type
        ]
    )
    populated_jungle.annual_weight_loss()

    sum_new_weights = sum(
        [
            animal.weight
            for class_type in populated_jungle.animal_classes.values()
            for animal in class_type
        ]
    )

    assert sum_new_weights < sum_old_weights


def test_propensity_ocean_cell(plain_ocean):
    assert plain_ocean.propensity(specie=Herbivore()) == 0
    assert plain_ocean.propensity(specie=Carnivore()) == 0


def test_propensity(populated_savannah):
    populated_savannah.current_fodder = 0
    for animal_class in populated_savannah.animal_classes["Herbivore"]:
        assert populated_savannah.propensity(animal_class) == 1


def test_update_parameters(plain_savannah):
    plain_savannah.update_parameters({"f_max": 200, "alpha": 0.4})
    assert (
        plain_savannah.param["f_max"] == 200
        and plain_savannah.param["alpha"] == 0.4
    )


def test_update_parameters_non_existing_keys(plain_savannah):
    with pytest.raises(ValueError):
        plain_savannah.update_parameters({"max": 200, "lpha": 0.4})


def test_update_parameters_neg(plain_savannah):
    with pytest.raises(ValueError):
        plain_savannah.update_parameters({"f_max": -200, "alpha": -0.4})


def test_add_animal_non_existing_species(plain_savannah):
    with pytest.raises(ValueError):
        plain_savannah.add_animal(
            [{"species": "Amir", "age": 10, "weight": 20}]
        )


def test_add_animal_none_age_and_weight(plain_savannah):
    plain_savannah.add_animal([{"species": "Carnivore"}])
    assert len(plain_savannah.animal_classes["Carnivore"]) == 1


def test_num_animals_per_cell(plain_savannah):
    plain_savannah.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Herbivore", "age": 5, "weight": 20},
        ]
    )
    assert plain_savannah.num_animals_per_cell() == 3


def test_num_sepcies_per_cell(populated_savannah):
    assert populated_savannah.num_sepcies_per_cell() == (100, 100)


def test_compute_relative_abundance_herbivore_zero_fodder(plain_savannah):
    plain_savannah.current_fodder = 0
    plain_savannah.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 20}]
    )
    for class_list in plain_savannah.animal_classes.values():
        for animal_class in class_list:
            assert plain_savannah.compute_relative_abundance(animal_class) == 0


def test_compute_relative_abundance():
    cell_jungle = Jungle()
    cell_jungle.insert_animal([Herbivore(), Carnivore()])
    for class_list in cell_jungle.animal_classes.values():
        for animal_class in class_list:
            assert cell_jungle.compute_relative_abundance(animal_class) != 0


def test_compute_relative_abundance_carnivore(plain_savannah):
    plain_savannah.add_animal(
        [{"species": "Carnivore", "age": 5, "weight": 10}]
    )
    for class_list in plain_savannah.animal_classes.values():
        for animal_class in class_list:
            assert plain_savannah.compute_relative_abundance(animal_class) == 0


def test_eat_herbivore_none_fodder(plain_savannah):
    herbivores = [Herbivore() for _ in range(100)]
    plain_savannah.insert_animal(herbivores)
    plain_savannah.current_fodder = 0
    prev_weight_sum = sum(
        [herb.weight for herb in plain_savannah.animal_classes["Herbivore"]]
    )
    plain_savannah.eat_herbivore()
    new_weight_sum = sum(
        [herb.weight for herb in plain_savannah.animal_classes["Herbivore"]]
    )
    assert prev_weight_sum == new_weight_sum


def test_eat_herbivore(populated_savannah):
    prev_value = populated_savannah.current_fodder
    populated_savannah.eat_herbivore()
    assert populated_savannah.current_fodder < prev_value


def test_eat_herbivore_low_current_fodder(populated_savannah):
    populated_savannah.current_fodder = 5
    prev_weight_herbs = sum(
        [
            herb.weight
            for herb in populated_savannah.animal_classes["Herbivore"]
        ]
    )
    populated_savannah.eat_herbivore()
    new_weight_herbs = sum(
        [
            herb.weight
            for herb in populated_savannah.animal_classes["Herbivore"]
        ]
    )
    assert new_weight_herbs > prev_weight_herbs


def test_eat_carnivore(mocker):
    mocker.patch("numpy.random.choice", return_value=True)
    desert_cell = Desert()
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    desert_cell.insert_animal(herbivores)
    desert_cell.insert_animal(carnivores)

    prev_weight_carn = sum(
        [carn.weight for carn in desert_cell.animal_classes["Carnivore"]]
    )
    desert_cell.eat_carnivore()
    new_weight_carn = sum(
        [carn.weight for carn in desert_cell.animal_classes["Carnivore"]]
    )
    assert prev_weight_carn < new_weight_carn


def test_eat_carnivore_manipulated_fitness(populated_desert):
    herb_len_be = len(populated_desert.animal_classes["Herbivore"])
    for carn in populated_desert.animal_classes["Carnivore"]:
        carn.fitness = 30
    populated_desert.eat_carnivore()
    new_len = len(populated_desert.animal_classes["Herbivore"])
    assert herb_len_be > new_len


def test_eat_carnivore_none_appetite(populated_savannah):
    prev_weight_sum = sum(
        [
            carn.weight
            for carn in populated_savannah.animal_classes["Carnivore"]
        ]
    )
    for carn in populated_savannah.animal_classes["Carnivore"]:
        carn.fitness = 30
        carn.update_parameters({"F": 0})

    new_weight_sum = sum(
        [
            carn.weight
            for carn in populated_savannah.animal_classes["Carnivore"]
        ]
    )

    assert prev_weight_sum == new_weight_sum


def test_annual_death(populated_savannah, mocker):
    mocker.patch("numpy.random.choice", return_value=True)
    populated_savannah.annual_death()
    for animal_lists in populated_savannah.animal_classes.values():
        assert len(animal_lists) == 0


def test_insert_animal(plain_savannah):
    plain_savannah.insert_animal([Herbivore()])


def test_update_animal_parameters_in_cell(populated_savannah):
    populated_savannah.update_animal_parameters_in_cell("Carnivore", {"F": 0})
    for carn in populated_savannah.animal_classes["Carnivore"]:
        assert carn.param["F"] == 0


def test_desert(plain_desert):
    assert isinstance(plain_desert, Desert)


def test_delete_animal_not_in_cell(plain_savannah):
    plain_savannah.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 10},
            {"species": "Carnivore", "age": 5, "weight": 10},
        ]
    )
    animal = Herbivore()

    with pytest.raises(ValueError):
        plain_savannah.delete_single_animal(animal)


def test_delete_single_animal(populated_savannah, plain_savannah):
    """
    Testing delete_single animal that it only works for single instances.
    It will create a confused for loop if used within a for loop. Decided to
    keep this test for educational purposes.

    Parameters
    ----------
    populated_savannah: class instance
                        Class instance of cell type Savannah with an existing
                        population of carnivores and herbivores.
    plain_savannah: class instance
                    Class instance of cell type Savannah with non-existing
                    population.



    """
    for animal in populated_savannah.animal_classes["Carnivore"]:
        populated_savannah.delete_single_animal(animal)

    assert len(populated_savannah.animal_classes["Carnivore"]) != 0

    herb = Herbivore()
    plain_savannah.insert_animal([herb])
    prev_amount = len(plain_savannah.animal_classes["Herbivore"])
    plain_savannah.delete_single_animal(herb)
    assert len(plain_savannah.animal_classes["Herbivore"]) < prev_amount


def test_compute_move_prob(populated_savannah):
    for animal in populated_savannah.animal_classes["Carnivore"]:
        assert populated_savannah.compute_move_prob(
            animal, [Ocean(), Ocean(), Ocean(), Ocean()]
        ) == [0, 0, 0, 0]


def test_migration(plain_savannah):
    plain_savannah.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 70},
            {"species": "Carnivore", "age": 5, "weight": 70},
        ]
    )

    for animal in plain_savannah.animal_classes["Carnivore"]:
        animal.fitness = 1
        animal.update_parameters({"mu": 1})

    plain_savannah.migration([Savannah(), Savannah(), Savannah(), Jungle()])
    assert len(plain_savannah.animal_classes["Carnivore"]) == 0


def test_mating(plain_savannah):
    plain_savannah.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 70},
            {"species": "Carnivore", "age": 5, "weight": 70},
        ]
    )
    for animal in plain_savannah.animal_classes["Carnivore"]:
        animal.fitness = 1
        animal.update_parameters({"gamma": 1})
    plain_savannah.mating()
    assert (len(plain_savannah.animal_classes["Carnivore"])) > 2
