# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from numba import jit
from .weighted_prob import weighted_prob
from .animals import Animal, Herbivore, Carnivore
import math
import random
import itertools
import numpy as np


class Cell:
    """
    Cell base class, which refers to a area or a square in a map. From this
    base class all cell types will be based upon, they will in other words
    be subclasses of Cell.
    """

    param = {}

    def __init__(self):
        """
        Initialises the cell class
        """
        self.animal_classes = {"Herbivore": [], "Carnivore": []}
        self.allowed_species = {"Herbivore": Herbivore, "Carnivore": Carnivore}
        self.current_fodder = 0

    @classmethod
    def update_parameters(cls, new_par_dict):
        """
        Uses the new dictionary to update the current parameters set.

        Parameters
        ----------
        new_par_dict: dict
                    Dictionary containing new parameter values.

        """
        for par in new_par_dict.keys():
            if par not in cls.param:
                raise ValueError(
                    f"Invalid input: {par} is not a key in "
                    f"class parameters"
                )

            if new_par_dict[par] < 0:
                raise ValueError(
                    f"Invalid input: {par} is of non-positive value"
                )
        cls.param.update(new_par_dict)

    def mating(self):
        """

        Mating function which makes all the animals in current cell have
        intercourse if 'determine_birth' is True and there are more than one
        animal of the same specie in the cell. Adds a new animal class to cell
        if the current animal is to give birth, and also updates the weight
        of the birth-giving animal.



        """
        for animal_list in self.animal_classes.values():
            children_born = [
                child
                for child in (
                    creature.determine_birth(len(animal_list))
                    for creature in animal_list
                )
                if child is not None
            ]
            animal_list.extend(children_born)

    def annual_weight_loss(self):
        """
        Makes all animals in the current cell lose their annual weight.

        """
        for animal_classes in itertools.chain.from_iterable(
            self.animal_classes.values()
        ):
            animal_classes.decrease_annual_weight()

    def eat_herbivore(self):
        r"""

        Makes all herbivores in the current cell eat and updates their weight
        by doing so.

        The eating method is determined by this:

        :math:`F` is the animals appetite, and :math:`f_{ij}` is the current
        fodder in the cell.

        if :math:`F\le f_{ij}`
            There is enough fodder in the cell, because F is the apetite, and
            the herbivore eats till it's full.
        if :math:`0 < f_{ij} < F`
            the animal eats is what is left of fodder, remaining fodder in the
            cell will be then set to 0.
        if :math:`f_{ij} = 0`
            the animal receives no food at all, because the current fodder
            in the cell is equal to 0.

        """

        # The fittest herbivore is to eat first
        sorted_herbivores = sorted(
            self.animal_classes["Herbivore"],
            key=lambda animal: animal.fitness,
            reverse=True,
        )

        for animals in sorted_herbivores:
            fodder_eat = animals.param["F"]

            if self.current_fodder == 0:
                break

            if fodder_eat <= self.current_fodder:
                animals.increase_eat_weight(fodder_eat)
                self.current_fodder -= fodder_eat
            elif 0 < self.current_fodder < fodder_eat:
                animals.increase_eat_weight(self.current_fodder)
                self.current_fodder -= self.current_fodder

    def eat_carnivore(self):
        r"""

        Feeds the carnivores in the current cell and updates their weight by
        doing so. The prey which is eaten by the predator (carnivore) is
        deleted from the cell.

        The carnivore eats till it has eaten an amnount :math:`F`, which means
        that it has eaten himself full of herbivores, i.e.
        :math:`\sum w_{herb-eaten} \geq F`



        """
        if len(self.animal_classes["Herbivore"]) > 0:
            self.animal_classes["Carnivore"].sort(
                key=lambda animal: animal.fitness, reverse=True
            )
            self.animal_classes["Herbivore"].sort(
                key=lambda animal: animal.fitness
            )
            for car in self.animal_classes["Carnivore"]:
                remove_herb = set()
                food_des = car.param["F"]
                current_food = 0
                for index, herb in enumerate(self.animal_classes["Herbivore"]):
                    if food_des <= current_food:
                        break
                    if car.determine_kill(herb.fitness):
                        current_food += herb.weight
                        car.increase_eat_weight(herb.weight)
                        remove_herb.add(index)
                self.remove_multiple_animals("Herbivore", remove_herb)

    def remove_multiple_animals(self, specie, animals_to_remove):
        """

        Deletes multiple animals from the cell instance, given the specie
        and the indexes of the animals to remove.

        Parameters
        ----------
        specie: string
            The specie type which is to be deleted from a cell instance
        animals_to_remove: list
        The list of indexes of the animals which are to be deleted from
        the cell list containing the animals.

        """
        self.animal_classes[specie] = [
            animal
            for index, animal in enumerate(self.animal_classes[specie])
            if index not in animals_to_remove
        ]

    def migration(self, neighbour_cells):
        """
        Moves animals from one cell to another cell, whether the animal is to
        move is determined by the animal instance with the function
        'determine_to_move'. Which cell it will move to is determined
        by computing the move probability for each cell, and is chosen by using
        random choice method with fixed probabilities.

        Parameters
        ----------
        neighbour_cells: list
                        List of class instances containing neighbouring cells

        """
        for type_of_animal, animal_list in self.animal_classes.items():
            remove_list = set()
            for index, animal in enumerate(animal_list):
                if animal.determine_to_move() and not animal.has_migrated:
                    move_prob = animal.compute_move_prob(neighbour_cells)
                    if sum(move_prob) == 0:
                        break
                    else:
                        idx = weighted_prob(move_prob)
                        chosen_cell = neighbour_cells[idx]
                        chosen_cell.insert_animal([animal])
                        animal.has_migrated = True
                        remove_list.add(index)
            self.remove_multiple_animals(type_of_animal, remove_list)

    # @staticmethod
    # @jit
    # def _weighted_probability(weights):
    #     cum_sum = cumsum(weights)
    #     idx = sum(cum_sum < rand())
    #     return idx

    def annual_death(self):
        """

        Loops through all animals in a cell and checks whether the animal is
        to die by using the animal instance function 'determine_death'.
        Proceeds to delete the animals which are to die, using the
        'remove_multiple_animals' function.

        """
        for type_of_animal, animal_list in self.animal_classes.items():
            remove_list = set()
            for index, animal in enumerate(animal_list):
                animal.has_migrated = False  # Prepares for the next cycle
                if animal.determine_death():
                    remove_list.add(index)
            self.remove_multiple_animals(type_of_animal, remove_list)

    # @staticmethod
    # def compute_move_prob(animal_type, neighbour_cells):
    #     """
    #
    #     Computes the probability to move to each neighbouring cell
    #
    #     Parameters
    #     ----------
    #     animal_type: class instance
    #                  Takes in a specific class instance
    #     neighbour_cells:
    #                 Takes in the neighbouring cells of the cell the animal
    #                 class instance is located at
    #
    #     Returns
    #     -------
    #
    #     list
    #         List containing probability to move to each cell
    #
    #
    #     """
    #     cell_propensity = []
    #     for cell in neighbour_cells:
    #         propensity_cell = cell.propensity(animal_type)
    #         cell_propensity.append(propensity_cell)
    #
    #     total_propensity = sum(cell_propensity)
    #
    #     computed_propensities = []
    #     for cell_prop in cell_propensity:
    #         try:
    #             prob = cell_prop / total_propensity
    #         except ZeroDivisionError:
    #             prob = 0
    #         computed_propensities.append(prob)
    #     return computed_propensities

    # def compute_relative_abundance(self, animal_class):
    #     r"""
    #
    #     Computes the relative abundance for either herbivore or carnivore,
    #     depending on the specie type.
    #
    #     The relative abundance is computed through this formula:
    #
    #     .. math::
    #         \epsilon_{k} = \frac{f_{k}}{(n_{k}+1)F^{\text{'}}}
    #
    #     Where :math:`\epsilon_{k}` is the relative abundance. :math:`f_{k}` is
    #     the current fodder for cell k, which is different for carnivores
    #     and herbivores. :math:`n_{k}` is the amount of same species in cell
    #     k, and :math:`F^{\text{'}}` is how much food the animal wants to eat.
    #
    #     Parameters
    #     ----------
    #     animal_class: class instance
    #                 The class instance one needs to calculate relative
    #                 abundance for
    #
    #     Returns
    #     -------
    #     float
    #         The relative abundance of the current cell
    #
    #             """
    #
    #     animal_name = type(animal_class).__name__
    #     amount_same_spec = len(self.animal_classes[animal_name])
    #     food_wanting = animal_class.param["F"]
    #     curr_fod = 0
    #     if animal_name == "Herbivore":
    #         curr_fod = self.current_fodder
    #     elif animal_name == "Carnivore":
    #         herb_weight_list = [
    #             herbivore.weight
    #             for herbivore in self.animal_classes["Herbivore"]
    #         ]
    #         curr_fod = sum(herb_weight_list)
    #
    #     if curr_fod == 0:
    #         return 0
    #     else:
    #         return curr_fod / ((amount_same_spec + 1) * food_wanting)

    # def propensity(self, specie):
    #     r"""
    #
    #     Computes and returns the propensity to move, the relative abundance is
    #     calculated through the 'compute_relative_abundance' function.
    #     The formula for propensity is given by:
    #
    #     .. math::
    #         \pi_{i\rightarrow j} =
    #         \begin{cases}
    #         0 & \text{if } j \text{is Mountain or Ocean}\\
    #         e^{\lambda \epsilon_{j}} & \text{otherwise}
    #         \end{cases}
    #
    #
    #     Parameters
    #     ----------
    #     specie: class instance
    #         The class instance of animal to be used in the function
    #
    #     Returns
    #     -------
    #     float
    #         The propensity to move
    #
    #     """
    #     name = type(specie).__name__
    #     cell_name = type(self).__name__
    #     if (name == "Herbivore" or name == "Carnivore") and (
    #         cell_name == "Ocean" or cell_name == "Mountain"
    #     ):
    #         return 0
    #
    #     relative_abundance = self.compute_relative_abundance(specie)
    #     lambda_specie = specie.param["lambda"]
    #
    #     return math.exp(lambda_specie * relative_abundance)

    def aging(self):
        """

        Loops through all animals in the cell and uses add age function from
        'animals.py' to add one age.

        """
        for animal_classes in itertools.chain.from_iterable(
            self.animal_classes.values()
        ):
            animal_classes.add_age()

    def delete_single_animal(self, animal):
        """

        Deletes single class instance from cell. Not to be used in a for loop
        because it would become a confused for loop. This method should only
        be used to delete a single instance of animal.

        Parameters
        ----------
        animal: class instance


        """
        name_animal = type(animal).__name__
        animal_classes_list = self.animal_classes[name_animal]
        if animal not in animal_classes_list:
            raise ValueError(f"Class {name_animal} is not in this cell")

        animal_classes_list.remove(animal)

    def insert_animal(self, animal_list):
        """

        Inserts animal class instance to a cell

        Parameters
        ----------
        animal_list: list
                List of animal classes to append to a cell


        """
        for animal_class in animal_list:
            if type(self).__name__ not in Animal.allowed_landscape:
                raise TypeError(f"This cell is inhabitable.")
            self.animal_classes[type(animal_class).__name__].append(
                animal_class
            )

    def add_animal(self, list_animal_dicts):
        """

        Adds a new animal from a dictionary into a cell

        Parameters
        ----------
        list_animal_dicts: list
                        List of dictionary containing animal specifications

        """
        cell_name = type(self).__name__
        for dicts in list_animal_dicts:
            animal_name = dicts["species"]

            age = dicts.get("age", None)
            weight = dicts.get("weight", None)

            if animal_name not in self.allowed_species.keys():
                raise ValueError(f"The animal type is not allowed")

            if cell_name not in Animal.allowed_landscape:
                raise ValueError(
                    f"This cell is inhabitable for specie: {animal_name}"
                )

            current_class = self.allowed_species[animal_name](weight, age)
            self.animal_classes[animal_name].append(current_class)

    def num_animals_per_cell(self):
        """

        Calculates the amount of animals per cell and returns that value

        Returns
        -------

        int
            The total number of animals per cell

        """
        return sum(len(lst) for lst in self.animal_classes.values())

    def num_species_per_cell(self):
        """

        Checks how many of each specie there is in the cell and returns that
        value.

        Returns
        -------
        int
            The amount of herbivores in cell
        int
            The amount of carnivores in cell


        """
        tot_herbivores = len(self.animal_classes["Herbivore"])
        tot_carnivores = len(self.animal_classes["Carnivore"])
        return tot_herbivores, tot_carnivores

    def gen_fodder(self):
        """

        Regenerates fodder for the cell classes

        """
        pass

    @staticmethod
    def update_animal_parameters_in_cell(species, param_dict):
        """

        Updates the parameters for all instances of specified specie

        Parameters
        ----------
        species: str
                Name of the specie which need sto be updated.
        param_dict:
                New parameter dictionary

        Returns
        -------

        """
        eval(species).update_parameters(param_dict)


class Ocean(Cell):
    """
    Ocean subclass, which inherits from the Cell superclass
    """

    def __init__(self):
        """
        Initialises the Ocean cell instance.
        """
        super().__init__()


class Mountain(Cell):
    """
    Mountain subclass, which inherits from the Cell superclass
    """

    def __init__(self):
        """
        Initialises the Mountain cell instance.
        """
        super().__init__()


class Desert(Cell):
    """
    Desert subclass which inherits from the Cell superclass
    """

    def __init__(self):
        """
        Initialises the Desert cell instance.
        """
        super().__init__()


class Savannah(Cell):
    """
    Savannah subclass, which inherits from the Cell superclass
    """

    param = {"f_max": 300, "alpha": 0.3}

    def __init__(self):
        """
        Initialises the Savannah cell instance, and current fodder is set
        to f_max from parameters.
        """
        super().__init__()
        self.current_fodder = self.param["f_max"]

    def gen_fodder(self):
        r"""

        Updates current fodder by this equation:

        .. math::
            f_{ij} \leftarrow f_{ij} + \alpha \times (f_{\text{Sav-max}} -
            f_{ij})

        Where :math:`f_{ij}` is the current amount of fodder in the cell,
        :math:`\alpha` is the growth parameter for Savannah subclass, and
        :math:`\f_{\text{Sav-max}}` is the maximum amount of fodder for
        the Savannah cell.


        """
        self.current_fodder = self.current_fodder + self.param["alpha"] * (
            self.param["f_max"] - self.current_fodder
        )


class Jungle(Cell):
    """
    Jungle subclass, which inherits from the Cell superclass
    """

    param = {"f_max": 800, "alpha": 0}

    def __init__(self):
        """
        Initialises the Jungle class instance and sets current fodder to the
        maximum value obtained from the parameters.

        """
        super().__init__()
        self.current_fodder = self.param["f_max"]

    def gen_fodder(self):
        """

        Updates current fodder to be the maximum amount of fodder.


        """
        self.current_fodder = self.param["f_max"]
