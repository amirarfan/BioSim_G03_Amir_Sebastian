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
    standard_map

    Returns
    -------

    """
    test_map = Map(standard_map)
    assert isinstance(test_map, Map)


def test_uneven_map():
    test_map = "OOO\nODSDO\nOOO"
    with pytest.raises(ValueError):
        Map(test_map)

def test_non_allowed_cell_type():
    test_map = "OOO\nOKO\nOOO"
    with pytes.raises(ValueError)
