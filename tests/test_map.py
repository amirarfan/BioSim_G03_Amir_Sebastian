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
        {"pop": [
            {"species": "Herbivore", "age": 10, "weight": 20}
            for _ in range(10)
        ],
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
