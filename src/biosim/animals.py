# -*- coding: utf-8 -*-

__author__ = 'Amir Arfan, Sebastian Becker'
__email__ = 'amar@nmbu.no, sebabeck@nmbu.no'

import math



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
    def _q_sigmoid(x, x_half, rate, signum):
        return 1 / (1+ math.exp(signum*rate*(x-x_half)))

    def update_weight(self, fodder):
        # Increase if eaten
        # Decrease each year
        pass

    def update_fitness(self, weight, age):
        # Denne bruker _q_sigmoid funksjonen
        pass



    class Herbivore(Animal):
        param ={"weight_birth":8.0,
                "sigma_birth":1.5,
                "beta":0.9,
                "eta":0.05,
                "a_half":40.0,
                "phi_age":0.2,
                "w_half":10.0,
                "phi_wheight":0.1,
                "mu":0.25,
                "lambda":1.0,
                "gamma":0.2,
                "zeta":3.5,
                "xi":1.2,
                "omega":0.4,
                "Fodder":10.0,
                "deltaPhimax":0}
        def __init__(self, weight=None, age=None):
            pass # Super location

    class Carnivore(Animal):
        param = {"weight_birth": 6.0,
                 "sigma_birth": 1.0,
                 "beta": 0.75,
                 "eta": 0.125,
                 "a_half": 60.0,
                 "phi_age": 0.4,
                 "w_half": 4.0,
                 "phi_wheight": 0.4,
                 "mu": 0.4,
                 "lambda": 1.0,
                 "gamma": 0.8,
                 "zeta": 3.5,
                 "xi": 1.1,
                 "omega": 0.9,
                 "Fodder": 50.0,
                 "deltaPhimax": 10.0}

        def __init__(self, weight=None, age=None):
            # IF none sett til standard verdi
            pass # Super

        @classmethod
        def compute_kill_prob(cls,min_fit_kill):
            #if
            pass

        def kill(self,min_fit_kill):
            pass
