# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from biosim.cell import Mountain, Ocean, Savannah, Jungle, Desert
from biosim.animals import Herbivore, Carnivore
import pytest


@pytest.fixture(autouse=True)
def reset_parameters():
    """

    Resets class parameters after each test.
    Used because of the update parameters test, and Pytest only import modules
    once at the beginning, so parameters are not reset by standard.

    """
    standard_parameters_herb = {
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
    """
    Pytest fixture for the Mountain subclass

    Returns
    -------
    cls
        Mountain class instance

    """
    return Mountain()


@pytest.fixture
def plain_ocean():
    """
    Pytest fixture for the Ocean subclass

    Returns
    -------
    cls
        Ocean class instance
    """
    return Ocean()


@pytest.fixture
def plain_savannah():
    """

    Pytest fixture for the Savannah subclass

    Returns
    -------
    cls
        Savannah class instance

    """
    return Savannah()


@pytest.fixture
def plain_jungle():
    """
    Pytest fixture for the Jungle subclass

    Returns
    -------
    cls
        Jungle class instance

    """
    return Jungle()


@pytest.fixture
def plain_desert():
    """

    Pytest fixture for the Desert subclass

    Returns
    -------
    cls
        Desert class instance

    """
    return Desert()


@pytest.fixture
def populated_jungle():
    """

    Pytest fixture for jungle subclass with a population of herbivores and
    carnivores.

    Returns
    -------
    jun_cell: cls
            class instance with already inserted population

    """
    jun_cell = Jungle()
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    jun_cell.insert_animal(herbivores)
    jun_cell.insert_animal(carnivores)
    return jun_cell


@pytest.fixture
def populated_desert():
    """

    Pytest fixture for desert subclass with a population of herbivores and
    carnivores

    Returns
    -------
    desert_cell: cls
                Class instance of desert cell with already inserted population

    """
    desert_cell = Desert()
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    desert_cell.insert_animal(herbivores)
    desert_cell.insert_animal(carnivores)
    return desert_cell


@pytest.fixture
def populated_savannah():
    """

    Pytest fixture for Savannah subclass with already inserted population

    Returns
    -------
    savannah_cell: cls
                    Class instance of Savannah subclass with already inserted
                    population
    """
    savannah_cell = Savannah()
    herbivores = [Herbivore() for _ in range(100)]
    carnivores = [Carnivore() for _ in range(100)]
    savannah_cell.insert_animal(herbivores)
    savannah_cell.insert_animal(carnivores)
    return savannah_cell


def test_fodder_mountain(plain_mountain):
    """
    Tests that there is no available fodder in the 'Mountain' cell type.

    Parameters
    ----------
    plain_mountain: cls
                    Class instance from pytest.fixture


    """
    assert plain_mountain.current_fodder == 0


def test_fodder_ocean(plain_ocean):
    """
    Tests that there is no available fodder in the 'Ocean' cell type.
    Parameters
    ----------
    plain_ocean: cls
                Class instance from pytest.fixture


    """
    assert plain_ocean.current_fodder == 0


def test_gen_fodder_savannah(populated_savannah):
    """
    Tests the generate fodder function for 'Savannah' cell type.

    Parameters
    ----------
    populated_savannah: cls
                        Class instance from pytest fixture



    """
    populated_savannah.eat_herbivore()
    prev_fodder = populated_savannah.current_fodder
    populated_savannah.gen_fodder()
    new_fodder = populated_savannah.current_fodder
    assert new_fodder > prev_fodder


def test_gen_fodder_jung(plain_jungle):
    """

    Tests the generate fodder function for 'Jungle' cell type.

    Parameters
    ----------
    plain_jungle: cls
                Plain jungle class from fixture


    """
    plain_jungle.current_fodder = 200
    plain_jungle.gen_fodder()
    assert plain_jungle.current_fodder == plain_jungle.param["f_max"]


def test_aging_cell(populated_jungle):
    """
    Tests that the aging function works for all animals in a cell.

    Parameters
    ----------
    populated_jungle: cls
                    Populated jungle class from fixture


    """
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


def test_annual_weight_loss(populated_jungle):
    """

    Tests the annual weight loss function. Checks if all animals actually lose
    weigh.

    Parameters
    ----------
    populated_jungle: cls
                    Populated jungle class from fixture

    Returns
    -------

    """
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
    """
    Checks that the propensity to move to an ocean cell for
    Herbivore and Carnivore is 0.

    Parameters
    ----------
    plain_ocean: cls
                Ocean class instance from fixture


    """
    assert plain_ocean.propensity(specie=Herbivore()) == 0
    assert plain_ocean.propensity(specie=Carnivore()) == 0


def test_propensity(populated_savannah):
    """
    Checks if current fodder is equal to 0, the propensity to move returned
    is 1.

    Parameters
    ----------
    populated_savannah: cls
                        Savannah class with population from fixture

    """
    populated_savannah.current_fodder = 0
    for animal_class in populated_savannah.animal_classes["Herbivore"]:
        assert populated_savannah.propensity(animal_class) == 1


def test_update_parameters(plain_savannah):
    """

    Tests the update parameters function in a cell

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class from fixture


    """
    plain_savannah.update_parameters({"f_max": 200, "alpha": 0.4})
    assert (
        plain_savannah.param["f_max"] == 200
        and plain_savannah.param["alpha"] == 0.4
    )


def test_update_parameters_non_existing_keys(plain_savannah):
    """
    Tests that ValueError is raised when entering non existing keys for
    update parameters

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture

    """
    with pytest.raises(ValueError):
        plain_savannah.update_parameters({"max": 200, "lpha": 0.4})


def test_update_parameters_neg(plain_savannah):
    """
    Checks that when negative parameters are inserted into update parameters
    ValueError is raised.

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
    with pytest.raises(ValueError):
        plain_savannah.update_parameters({"f_max": -200, "alpha": -0.4})


def test_add_animal_non_existing_species(plain_savannah):
    """
    Checks that ValueError is raised when trying to add non existing species.

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture

    """
    with pytest.raises(ValueError):
        plain_savannah.add_animal(
            [{"species": "Amir", "age": 10, "weight": 20}]
        )


def test_add_animal_ocean(plain_ocean):
    with pytest.raises(ValueError):
        plain_ocean.add_animal([{"species": "Herbivore"}])

    with pytest.raises(ValueError):
        plain_ocean.add_animal([{"species": "Carnivore"}])


def test_add_animal_none_age_and_weight(plain_savannah):
    """

    Tests that adding animal with no age or weight input works

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture

    """
    plain_savannah.add_animal([{"species": "Carnivore"}])
    assert len(plain_savannah.animal_classes["Carnivore"]) == 1


def test_num_animals_per_cell(plain_savannah):
    """
    Tests that num_animals_per_cell function returns the correct value
    of animals.

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
    plain_savannah.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Carnivore", "age": 5, "weight": 20},
            {"species": "Herbivore", "age": 5, "weight": 20},
        ]
    )
    assert plain_savannah.num_animals_per_cell() == 3


def test_num_species_per_cell(populated_savannah):
    """
    Tests the num_species_per_cell function to output correct value.

    Parameters
    ----------
    populated_savannah: cls
                        Savannah class instance from fixture with population

    """
    assert populated_savannah.num_species_per_cell() == (100, 100)


def test_compute_relative_abundance_herbivore_zero_fodder(plain_savannah):
    """
    Check that with zero fodder, the relative abundance is also equal to 0

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
    plain_savannah.current_fodder = 0
    plain_savannah.add_animal(
        [{"species": "Herbivore", "age": 5, "weight": 20}]
    )
    for class_list in plain_savannah.animal_classes.values():
        for animal_class in class_list:
            assert plain_savannah.compute_relative_abundance(animal_class) == 0


def test_compute_relative_abundance():
    """

    Tests that relative abundance is not zero when fodder is available for
    both species.

    """
    cell_jungle = Jungle()
    cell_jungle.insert_animal([Herbivore(), Carnivore()])
    for class_list in cell_jungle.animal_classes.values():
        for animal_class in class_list:
            assert cell_jungle.compute_relative_abundance(animal_class) != 0


def test_compute_relative_abundance_carnivore(plain_savannah):
    """
    Tests that relative abundance for the carnivore is equal to 0, when
    no Herbivores are in the cell.

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture

    Returns
    -------

    """
    plain_savannah.add_animal(
        [{"species": "Carnivore", "age": 5, "weight": 10}]
    )
    for class_list in plain_savannah.animal_classes.values():
        for animal_class in class_list:
            assert plain_savannah.compute_relative_abundance(animal_class) == 0


def test_eat_herbivore_none_fodder(plain_savannah):
    """
    Tests that herbivores gain no weight when no fodder is available, and
    that eat function can be called properly even though no fodder is available

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
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
    """

    Parameters
    ----------
    populated_savannah

    Returns
    -------

    """
    prev_value = populated_savannah.current_fodder
    populated_savannah.eat_herbivore()
    assert populated_savannah.current_fodder < prev_value


def test_eat_herbivore_low_current_fodder(populated_savannah):
    """
    Tests that some herbivores can eat even though the current fodder is of low
    amount.

    Parameters
    ----------
    populated_savannah: cls
                        Savannah class instance with population from fixture

    Returns
    -------

    """
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
    """
    Tests the eat carnivore function using mocker.patch to make it always eat

    """
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
    """
    Manipulating the fitness so that there is a certain probability
    for the carnivore to eat, tests that Carnivores eat with manipulated
    fitness.

    Parameters
    ----------
    populated_desert: cls
                    Desert class instance with population from fixture


    """
    herb_len_be = len(populated_desert.animal_classes["Herbivore"])
    for carn in populated_desert.animal_classes["Carnivore"]:
        carn.fitness = 30
    populated_desert.eat_carnivore()
    new_len = len(populated_desert.animal_classes["Herbivore"])
    assert herb_len_be > new_len


def test_eat_carnivore_none_appetite(populated_savannah):
    """

    Tests that with no apetite, the Carnivores will consume no food

    Parameters
    ----------
    populated_savannah: cls
                        Savannah class instance with population from fixture.


    """
    prev_weight_sum = sum(
        [
            carn.weight
            for carn in populated_savannah.animal_classes["Carnivore"]
        ]
    )
    populated_savannah.update_animal_parameters_in_cell("Carnivore", {"F": 0})

    new_weight_sum = sum(
        [
            carn.weight
            for carn in populated_savannah.animal_classes["Carnivore"]
        ]
    )

    assert prev_weight_sum == new_weight_sum


def test_annual_death(populated_savannah, mocker):
    """

    Testing that annual death works by using mocker to give certain death to
    animals.

    Parameters
    ----------
    populated_savannah: cls
                        Savannah class instance from fixture.


    """
    mocker.patch("numpy.random.choice", return_value=True)
    populated_savannah.annual_death()
    for animal_lists in populated_savannah.animal_classes.values():
        assert len(animal_lists) == 0


def test_insert_animal(plain_savannah):
    """
    Testing the insert animal function

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
    plain_savannah.insert_animal([Herbivore()])


def test_update_animal_parameters_in_cell(populated_savannah):
    """

    Tests update parameters for several animals in cell

    Parameters
    ----------
    populated_savannah: cls
                        Savannah class instance with population from fixture

    Returns
    -------

    """
    populated_savannah.update_animal_parameters_in_cell("Carnivore", {"F": 0})
    for carn in populated_savannah.animal_classes["Carnivore"]:
        assert carn.param["F"] == 0


def test_desert(plain_desert):
    """
    Checks if a desert instance of Desert class.

    Parameters
    ----------
    plain_desert: cls
                Desert class instance from fixture.


    """
    assert isinstance(plain_desert, Desert)


def test_delete_animal_not_in_cell(plain_savannah):
    """
    Checks that ValueError is raised when attempting to delete an animal
    which is not in the cell.


    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
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
    populated_savannah: cls
                        Class instance of cell type Savannah with an existing
                        population of carnivores and herbivores.
    plain_savannah: cls
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
    """
    Tests that the move probability to move to only ocean cells is 0.

    Parameters
    ----------
    populated_savannah: cls
                        Savannah class instance from fixture with population.


    """
    for animal in populated_savannah.animal_classes["Carnivore"]:
        assert populated_savannah.compute_move_prob(
            animal, [Ocean(), Ocean(), Ocean(), Ocean()]
        ) == [0, 0, 0, 0]


def test_migration(plain_savannah):
    """

    Tests migration by manipulation mu and fitness so that all animals are
    certain to move.

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
    plain_savannah.add_animal(
        [
            {"species": "Carnivore", "age": 5, "weight": 70},
            {"species": "Carnivore", "age": 5, "weight": 70},
        ]
    )
    plain_savannah.update_animal_parameters_in_cell("Carnivore", {"mu": 1})
    for animal in plain_savannah.animal_classes["Carnivore"]:
        animal.fitness = 1

    plain_savannah.migration([Savannah(), Savannah(), Savannah(), Jungle()])
    assert len(plain_savannah.animal_classes["Carnivore"]) == 0


def test_mating(plain_savannah):
    """
    Tests mating by manipulating fitness and gamma parameter.

    Parameters
    ----------
    plain_savannah: cls
                    Savannah class instance from fixture


    """
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
