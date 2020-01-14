# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"
from .animals import Herbivore, Carnivore
from .cell import Ocean, Mountain, Desert, Savannah, Jungle
import numpy as np


class Map:
    dict_cells = {
        "O": Ocean,
        "M": Mountain,
        "D": Desert,
        "S": Savannah,
        "J": Jungle,
    }

    def __init__(self, map_string):

        self.map = np.array(
            [
                self.map_factory(curr_list)
                for curr_list in map_string.split("\n")
            ]
        )

        self.outer_limits = np.concatenate(
            self.map[0], self.map[:, 0], self.map[:, -1], self.map[-1]
        )

        for cell in self.outer_limits:
            if type(cell).__name__ != "Ocean":
                raise ValueError(f"Outer Cell is not {Ocean}")

    @classmethod
    def map_factory(cls, list_to_alter):
        temp_list = []
        for letter in list_to_alter:
            if letter not in cls.dict_cells.values():
                raise ValueError(f"{letter} is not a cell type")
            temp_list.append(cls.dict_cells[letter])

        return temp_list

    def r(self, loc):
        x, y = loc
        neighbour_cords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [self.map[cell] for cell in neighbour_cords]

<<<<<<< Updated upstream
    def add_animals(self):
        pass
=======

    def add_animals(self, ini_list):
        loc = ini_list["loc"]
        if loc in self.map:


>>>>>>> Stashed changes

    def move_all_animals(self):
        pass

    def eat_all_animals(self):
        pass

    def mate_all_animals(self):
        pass

    def age_all_animals(self):
        pass

    def annual_weightloss_all_animals(self):
        pass
