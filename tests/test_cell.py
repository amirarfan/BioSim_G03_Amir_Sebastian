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


def test_eat_carnivore_none_apetite(populated_savannah):
    prev_weight_sum = sum([carn.weight for carn in
                           populated_savannah.animal_classes["Carnivore"]])
    for animal in populated_savannah.animal_classes["Carnivore"]:
        animal.fitness = 30
        animal.update_parameters({"F": 0})

    new_weight_sum = sum([carn.weight for carn in
                          populated_savannah.animal_classes["Carnivore"]])

    assert prev_weight_sum == new_weight_sum


def test_annual_death(populated_savannah, mocker):
    mocker.patch('numpy.random.choice', return_value=True)
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
        plain_savannah.delete_animal(animal)


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


def test_compute_move_prob():
    savannah_cell = Savannah()
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
