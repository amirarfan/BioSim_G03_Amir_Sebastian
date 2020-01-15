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

    allowed_cells = ["Jungle", "Savannah", "Desert"]

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

    def get_neighbour(self, loc):
        x, y = loc
        neighbour_cords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [self.map[cell] for cell in neighbour_cords]

    def add_animals(self, ini_list):
        for dictionary in ini_list:
            try:
                loc = dictionary["loc"]
            except IndexError:
                print(f'{dictionary["loc"]} is not a location on map')
                break
            pop = dictionary["pop"]
            cell_type = self.map[loc]

            if type(cell_type).__name__ not in self.allowed_cells:
                raise ValueError(f"This location is inhabitable")

            cell_type.add_animal(pop)

    def move_all_animals(self):
        for y, list_loc in enumerate(self.map):
            for x, cell in enumerate(self.map):
                cell.migration(self.get_neighbour((x, y)))

    def all_animals_eat(self):
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.eat_herbivore()
                    cell.eat_carnivore()

    def mate_all_animals(self):
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.mating()

    def age_all_animals(self):
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.aging()

    def annual_weightloss_all_animals(self):
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.annual_weight_loss()

    def annual_death_all_animals(self):
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.annual_death()
