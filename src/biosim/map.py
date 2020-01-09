# -*- coding: utf-8 -*-

__author__ = 'Amir Arfan, Sebastian Becker'
__email__ = 'amar@nmbu.no, sebabeck@nmbu.no'

import animals


class Cell:
    param = {}

    def __init__(self):
        self.cell_pop = {'Herbivore': 0, 'Carnivore': 0}
        self.animal_classes = []
        self.allowed_species = ['Herbivore', 'Carnivore']

    @classmethod
    def propensity(cls):
        pass

    def intercourse(self):
        pass


    def aging(self):
        for animal in self.animal_classes:
            animal.add_age()

    def delete_animal(self):
        pass

    def add_animal(self, list_animal):
        for dicts in list_animal:
            if dicts['species'] in self.allowed_species:
                self.animal_classes.append(animals.dicts['species'](dicts['age'], dicts['weight']))
            else:
                raise ValueError(f'The animal type is not allowed')





class Ocean(Cell):
    def __init__(self):
        self.relevant_fodder = None
        pass


class Mountain(Cell):
    def __init__(self):
        self.relevant_fodder = None
        pass


class Desert(Cell):
    # Herbivores kan ikke spise her, dvs at hvis de spiser er det feil
    def __init__(self):
        pass


class Savannah(Cell):
    param = {'f_max': 300, 'alpha': 0.3}

    def __init__(self):
        self.current_fodder = self.param['f_max']
        pass

    def gen_fodder_sav(self):
        self.current_fodder = self.current_fodder + self.param['alpha'] * (
                    self.param['f_max'] - self.current_fodder)


class Jungle(Cell):
    param = {'f_max': 800, 'alpha': 0}

    def __init__(self):
        self.current_fodder = self.param["f_max"]

    def gen_fodder_jung(self):
        self.current_fodder = self.param['f_max']
