# -*- coding: utf-8 -*-

__author__ = 'Amir Arfan, Sebastian Becker'
__email__ = 'amar@nmbu.no, sebabeck@nmbu.no'

from .animals import Herbivore, Carnivore, Animal
import numpy as np


class Cell:
    param = {}

    def __init__(self):
        self.cell_pop = {'Herbivore': 0, 'Carnivore': 0}
        self.animal_classes = {'Herbivore': [], 'Carnivore': []}
        self.allowed_species = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        self.current_fodder = self.param['f_max']

    def propensity(self):
        pass

    def intercourse(self):
        pass

    def compute_relative_abundance(self):
        pass

    def aging(self):
        for animal in self.animal_classes.values():
            animal.add_age()

    def delete_animal(self, animal):
        name_animal = type(animal).__name__
        animal_classes_list = self.animal_classes[name_animal]
        if animal not in animal_classes_list:
            raise ValueError(f'Class {name_animal} is not in this cell')
        else:
            for element in animal_classes_list:
                if element == animal:
                    return animal_classes_list.pop(
                        animal_classes_list.pop(element))

    def add_animal(self, list_animal):
        for dicts in list_animal:
            animal_name = dicts['species']
            age = dicts['age']
            weight = dicts['weight']
            if animal_name in self.allowed_species.keys():
                current_class = self.allowed_species['animal_name'](age,
                                                                    weight)
                self.animal_classes[animal_name].append(current_class)
            else:
                raise ValueError(f'The animal type is not allowed')


class Ocean(Cell):
    def __init__(self):
        self.relevant_fodder = None


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
        super().__init__()

    def gen_fodder_sav(self):
        self.current_fodder = self.current_fodder + self.param['alpha'] * (
                self.param['f_max'] - self.current_fodder)


class Jungle(Cell):
    param = {'f_max': 800, 'alpha': 0}

    def __init__(self):
        self.current_fodder = self.param["f_max"]

    def gen_fodder_jung(self):
        self.current_fodder = self.param['f_max']
