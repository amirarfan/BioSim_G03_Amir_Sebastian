# -*- coding: utf-8 -*-

__author__ = 'Amir Arfan, Sebastian Becker'
__email__ = 'amar@nmbu.no, sebabeck@nmbu.no'


class Animal:
    def __init__(self):
        self.weight = weight
        pass

    #@classmethod
    #def birth(cls, num_species, weight):
     # Update weight after birth
     #   pass --  Flytte til Board/Map?

    @staticmethod
    def _q_sigmoid(x, x_half, rate):
        pass

    @classmethod
    def fitness(cls, weight, age):
        # Denne bruker _q_sigmoid funksjonen
        pass

    @classmethod
    def update_weight(cls, fodder):
        # Increase if eaten
        # Decrease each year
        pass

    @classmethod
    def eat(cls):
        pass

    @classmethod
    def age(cls):
        pass

    @classmethod
    def migration(cls):
        pass
    
    @classmethod
    def death(cls):
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
