# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"
from .animals import Herbivore, Carnivore
from .cell import Ocean, Mountain, Desert, Savannah, Jungle
import numpy as np

class Map:
    dict_cells = {'O': Ocean, 'M': Mountain, 'D': Desert, 'S': Savannah, 'J': Jungle}

    def __init(self, map_string):

        self.map = np.array([self.map_factory(curr_list) for curr_list in map_string.split('\n')])

        # Legge til sjekk om at alle de første er Ocean

    @classmethod
    def map_factory(cls, list_to_alter):
        temp_list = []
        for letter in list_to_alter:
            if letter not in cls.dict_cells.values():
                raise ValueError(f'{letter} is not a cell type')
            temp_list.append(cls.dict_cells[letter])

        return temp_list

    def neighbour_cells(self, loc:
        pass

    def add_animals(self):
        pass

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
