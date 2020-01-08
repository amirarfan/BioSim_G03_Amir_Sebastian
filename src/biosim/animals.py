# -*- coding: utf-8 -*-

__author__ = 'Amir Arfan, Sebastian Becker'
__email__ = 'amar@nmbu.no, sebabeck@nmbu.no'


class Animal:
    def __init__(self, age=None, location=None):
        self.location = location # IF TEST må legges til
        self.age = age # IF TEST må legges til
        pass

    # @classmethod
    # def eat(cls):
    # pass --  Flytte til Board/Map?

    # @classmethod
    # def update_age(cls):
    # pass --  Flytte til Board/Map?

    @classmethod
    def probability(cls, fitness):
        pass

    @classmethod
    def migration(cls, cell):
        # relative abundance of fodder(Ek) regnes ut i map
        # numpy random choice whit custom prpbability
        pass

    @staticmethod
    def compute_prob_death(fitness):
        pass

    @classmethod
    def death(cls, fitness):
        pass

    # @classmethod
    # def birth(cls, num_species, weight):
    # Update weight after birth
    #   pass --  Flytte til Board/Map?

    @classmethod
    def _normal_weight(cls, weight_birth, sigma_birth):
        # Bruker numpy.random.normal(w_birth, sigma_birth)

    @staticmethod
    def _q_sigmoid(x, x_half, rate):
        pass

    def update_weight(self, fodder):
        # Increase if eaten
        # Decrease each year
        pass

    def update_fitness(self, weight, age):
        # Denne bruker _q_sigmoid funksjonen
        pass



    class Herbivore(Animal):
        # Parameterene til Herbivore
        def __init__(self, weight=None, age=None):
            pass # Super

    class Carnivore(Animal):
        # Parameterne til Carnivore
        def __init__(self, weight=None, age=None):
            # IF none sett til standard verdi
            pass # Super

        def kill(self):
            pass
