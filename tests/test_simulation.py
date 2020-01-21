# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

import pytest
from biosim.simulation import BioSim
import textwrap
import os


@pytest.fixture
def standard_sim():
    geogr = """\
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
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]
    stan_sim = BioSim(geogr, ini_herbs, seed=123)
    stan_sim.add_population(ini_carns)
    return stan_sim


@pytest.fixture
def desert_sim():
    geogr = """\
                      OOOOOOOOOOOOOOOOOOOOO
                      OOOOOOOODDDDDDDDDDDDO
                      ODDDDDDDDDDDDDDDDDDOO
                      ODDDDDDDDDDDDDDDDDOOO
                      ODDDDDDDDDDDDDDDDDOOO
                      OODDDDDDDDDDDDDDDDOOO
                      OODDDDDDDDDDDDDDDDOOO
                      OODDDDDDDDDDDDDDDDOOO
                      ODDDDDDDDDDDDDDDDDDOO
                      OOOODDDDDDDDDDDDDDDOO
                      ODDDDDDDDDDDDDDDDDDOO
                      ODDDDDDDDDDDDDDDDDDOO
                      OOOOOOOOOOOOOOOOOOOOO"""

    geogr = textwrap.dedent(geogr)

    des_sim = BioSim(geogr, ini_pop=[], seed=123)
    return des_sim


def test_standard_biosim(standard_sim):
    """
    Simple test to check that simulation works properly with visualization.

    """
    standard_sim.simulate(50)


def test_herbs_des_sim(desert_sim):
    """
    Test to see if Herbivores die out on Desert

    """
    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    desert_sim.add_population(ini_herbs)
    desert_sim.simulate(50)


def test_herbs_and_carns_des_sim(desert_sim):
    """
    Test to see that Carnivores will outlive the Herbivores in the desert

    """
    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(500)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(200)
            ],
        }
    ]
    desert_sim.add_population(ini_herbs)
    desert_sim.add_population(ini_carns)
    desert_sim.simulate(100)
