# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no"

from biosim.map import Map
from biosim.cell import Mountain, Ocean, Savannah, Jungle, Desert
from biosim.animals import Herbivore, Carnivore
import pytest
import textwrap


@pytest.fixture
def standard_map():
    """
    Creates a standard map  fixture which can be used for tests

    Returns
    -------
    sgegor = str
            Standard map taken from 'check_sim.py'

    """
    sgeogr = """\
               OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""

    sgeogr = textwrap.dedent(sgeogr)

    return sgeogr


@pytest.fixture
def populated_island(standard_map):
    ini_herbs = [
        {
            "loc": (5, 5),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (5, 5),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    island_map = Map(standard_map)
    island_map.add_animals(ini_herbs)
    island_map.add_animals(ini_carns)

    return island_map


def test_constructor_map(standard_map):
    """
    Tests the constructor in Map

    Parameters
    ----------
    standard_map: str
                String based map from fixture

    """
    test_map = Map(standard_map)
    assert isinstance(test_map, Map)


def test_uneven_map():
    test_map = "OOO\nODSDO\nOOO"
    with pytest.raises(ValueError):
        Map(test_map)


def test_non_allowed_cell_type():
    test_map = "OOO\nOKO\nOOO"
    with pytest.raises(ValueError):
        Map(test_map)


def test_non_island_map():
    test_map = "DDD\nOOO\nDDD"
    with pytest.raises(ValueError):
        Map(test_map)


def test_get_neighbours(standard_map):
    island = Map(standard_map)
    neighbours = island.get_neighbour((2, 2))
    assert len(list(neighbours)) == 4

    # Should only get two values at the edge
    neighbours_edge = island.get_neighbour((0, 0))
    assert len(list(neighbours_edge)) == 2

    # Testing non existing indexes
    non_exist_neighbours = island.get_neighbour((30, 30))
    assert len(list(non_exist_neighbours)) == 0

    # Testing negative indexes
    negative_neighbours = island.get_neighbour((2, -10))
    assert len(list(negative_neighbours)) == 0


def test_add_animals_map(standard_map):
    ini_herbs = [
        {
            "loc": (5, 5),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (5, 5),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]

    island = Map(standard_map)

    island.add_animals(ini_carns)
    assert island.num_animals_on_map() == 150

    island.add_animals(ini_herbs)
    assert island.num_animals_on_map() == 300


def test_add_animals_on_ocean_loc(standard_map):
    ini_herbs = [
        {
            "loc": (0, 0),
            "pop": [
                {"species": "Herbivore", "age": 10, "weight": 20}
                for _ in range(10)
            ],
        }
    ]

    island = Map(standard_map)
    with pytest.raises(ValueError):
        island.add_animals(ini_herbs)


def test_add_animals_on_no_loc(standard_map):
    ini_herbs = [
        {
            "pop": [
                {"species": "Herbivore", "age": 10, "weight": 20}
                for _ in range(10)
            ]
        }
    ]

    ini_carns = [
        {
            "loc": None,
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]

    island = Map(standard_map)
    island.add_animals(ini_herbs)
    assert island.num_animals_on_map() == 0

    with pytest.raises(ValueError):
        island.add_animals(ini_carns)


def test_move_all_animals(populated_island):
    island = populated_island
    curr_cell = island.map[(5, 5)]
    prev_val = curr_cell.num_animals_per_cell()
    island.move_all_animals()
    new_val = curr_cell.num_animals_per_cell()
    assert prev_val > new_val


def test_all_animals_eat(populated_island):
    island = populated_island
    curr_cell = island.map[(5, 5)]
    prev_amount_herbs, prev_amount_carns = curr_cell.num_species_per_cell()
    island.all_animals_eat()
    # If the carnivores eat, there should be a reduction in herbivore pop.
    new_amount_herbs, new_amount_carns = curr_cell.num_species_per_cell()
    assert new_amount_herbs < prev_amount_herbs


def test_mate_all_animals(standard_map, mocker):
    mocker.patch("numpy.random.choice", return_value=True)
    ini_carns = [
        {
            "loc": (5, 5),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 50}
                for _ in range(150)
            ],
        }
    ]

    island = Map(standard_map)
    island.add_animals(ini_carns)
    prev_val = island.num_animals_on_map()
    island.mate_all_animals()
    new_val = island.num_animals_on_map()
    assert prev_val < new_val


def test_age_all_animal(populated_island):
    island = populated_island
    curr_cell = island.map[(5, 5)]
    prev_age_sum = sum(
        [
            anim.age
            for anim_list in curr_cell.animal_classes.values()
            for anim in anim_list
        ]
    )
    island.age_all_animals()
    new_age_sum = sum(
        [
            anim.age
            for anim_list in curr_cell.animal_classes.values()
            for anim in anim_list
        ]
    )
    assert prev_age_sum < new_age_sum


def test_annual_weight_loss(populated_island):
    island = populated_island
    curr_cell = island.map[(5, 5)]
    prev_weight_sum = sum(
        [
            anim.weight
            for anim_list in curr_cell.animal_classes.values()
            for anim in anim_list
        ]
    )
    island.annual_weight_loss_all_animals()
    new_weight_sum = sum(
        [
            anim.weight
            for anim_list in curr_cell.animal_classes.values()
            for anim in anim_list
        ]
    )

    assert new_weight_sum < prev_weight_sum


def test_annual_weight(populated_island, mocker):
    mocker.patch("numpy.random.choice", return_value=True)
    island = populated_island
    prev_val = island.num_animals_on_map()
    island.annual_death_all_animals()
    new_val = island.num_animals_on_map()

    assert prev_val > new_val


def test_num_animals_per_species(populated_island):
    island = populated_island
    tot_herbs, tot_carns = island.num_species_on_map()
    assert tot_herbs == 150
    assert tot_carns == 150


def test_update_params_animals(populated_island):
    island = populated_island
    island.update_animal_params_all_cells("Herbivore", {"F": 15})
    assert Herbivore.param["F"] == 15

    island.update_animal_params_all_cells("Carnivore", {"DeltaPhiMax": 5})
    assert Carnivore.param["DeltaPhiMax"] == 5


def test_update_params_cell(populated_island):
    island = populated_island
    island.update_param_all_cells("J", {"f_max": 500})
    assert Jungle.param["f_max"] == 500


def test_cycle_runs(populated_island):
    island = populated_island
    island.cycle()
