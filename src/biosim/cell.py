# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from .animals import Herbivore, Carnivore
import numpy as np


class Cell:
    param = {}

    def __init__(self):
        # self.cell_pop = {'Herbivore': 0, 'Carnivore': 0} Ubrukelig ?? kaan
        # telle fra animal_classes!
        self.animal_classes = {"Herbivore": [], "Carnivore": []}
        self.allowed_species = {"Herbivore": Herbivore, "Carnivore": Carnivore}
        self.current_fodder = self.param["f_max"]

    @classmethod
    def update_parameters(cls, new_par_dict):
        for par in new_par_dict.keys():
            if par not in cls.param:
                raise ValueError(
                    f"Invalid input: {par} is not a key in "
                    f"class parameters"
                )

            if new_par_dict["par"] < 0:
                raise ValueError(
                    f"Invalid input: {par} is of non-positive value"
                )
        cls.param.update(new_par_dict)

    def mating(self):
        for (
            animal_list
        ) in (
            self.animal_classes.values()
        ): 
            for animal_class in animal_list:
                if animal_class.determine_birth(len(animal_list)):
                    new_child = animal_class.__class__()
                    new_child_specie = type(new_child).__name__
                    self.animal_classes[new_child_specie].append(new_child)
                    animal_class.decrease_birth_weight(new_child.weight)

    def compute_relative_abundance(self, animal_class):
        animal_name = type(animal_class).__name__
        amount_same_spec = len(self.animal_classes[animal_name])
        food_wanting = self.animal_class.param["F"]
        return self.current_fodder / ((amount_same_spec + 1) * food_wanting)

    def propensity(self, specie):
        name = type(specie).__name__
        cell_name = type(self).__name__
        if (name == "Herbivore" or name == "Carnivore") and (
            cell_name == "Ocean" or cell_name == "Mountain"
        ):
            return 0

        relative_abundance = self.compute_relative_abundance(specie)
        lambda_specie = specie.param['lambda']

        return np.exp(lambda_specie*relative_abundance)

    def aging(self):
        """

        Loops through all animals in the cell and uses add age function from
        'animals.py' to add one age.

        """
        for all_animals in self.animal_classes.values():
            for animal in all_animals:
                animal.add_age()

    def delete_animal(self, animal):
        name_animal = type(animal).__name__
        animal_classes_list = self.animal_classes[name_animal]
        if animal not in animal_classes_list:
            raise ValueError(f"Class {name_animal} is not in this cell")

        animal_classes_list.remove(
            animal
        )  # Tenkte at siden remove tar den første LIKE INSTANCEN,
        # er det mer brukbart å bruke remove.

    def add_animal(self, list_animal):
        for dicts in list_animal:
            animal_name = dicts["species"]
            age = dicts["age"]
            weight = dicts["weight"]
            if animal_name in self.allowed_species.keys():
                current_class = self.allowed_species["animal_name"](
                    age, weight
                )
                self.animal_classes[animal_name].append(current_class)
            else:
                raise ValueError(f"The animal type is not allowed")


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
    param = {"f_max": 300, "alpha": 0.3}

    def __init__(self):
        super().__init__()

    def gen_fodder_sav(self):
        self.current_fodder = self.current_fodder + self.param["alpha"] * (
            self.param["f_max"] - self.current_fodder
        )


class Jungle(Cell):
    param = {"f_max": 800, "alpha": 0}

    def __init__(self):
        self.current_fodder = self.param["f_max"]

    def gen_fodder_jung(self):
        self.current_fodder = self.param["f_max"]
