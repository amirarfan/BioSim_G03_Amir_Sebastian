# -*- coding: utf-8 -*-

__author__ = 'Amir Arfan, Sebastian Becker'
__email__ = 'amar@nmbu.no, sebabeck@nmbu.no'

import math
import numpy as np


class Animal:
    param = {}

    def __init__(self, age=None, weight=None):

        if age is not None and age < 0:
            raise ValueError('Age cannot be lower than 0')

        if age is not None:
            self._age = age
        else:
            self._age = 0

        if weight is not None and weight < 0:
            raise ValueError('Weight cannot be lower than 0')

        if weight is not None:
            self._weight = weight
        else:
            self._weight = self._normal_weight()

        self.fitness = None

        if self.fitness is not None:
            pass
        else:
            self.update_fitness()

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, val):
        if val < 0:
            raise ValueError('Age must be higher than 0')
        self._age = val
        self.update_fitness()

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, val):
        if val < 0:
            raise ValueError('Weight must be higher than 0')
        self._weight = val
        self.update_fitness()


    # def eat(cls):
    # pass --  Flytte til Board/Map?

    # @classmethod
    # def update_age(cls):
    # pass --  Flytte til Board/Map?

    @classmethod
    def update_parameters(cls, new_par_dict):
        for par in new_par_dict.keys():
            if par in cls.param:
                pass
            else:
                raise ValueError(f'Invalid input: {par} is not a key in '
                                 f'class parameters')

        cls.param.update(new_par_dict)

    def add_age(self):
        self._age += 1
        self.update_fitness()

    def determine_to_move(self):
        probability_move = self.fitness * self.param["mu"]
        return np.random.choice([True, False], p=[probability_move,
                                                  1 - probability_move])

    def determine_death(self):
        death_prob = 0
        if self.fitness == 0:
            return True
        elif self.fitness > 0:
            death_prob = self.param['omega'] * (1 - self.fitness)

        return np.random.choice([True, False], p=[death_prob,
                                                  1 - death_prob])  # Chooses randomly with given probabilities

    @staticmethod
    def compute_prob_birth(gamma, fitness, nearby_animals):
        return min(1, gamma * fitness * (nearby_animals - 1))

    def determine_birth(self, nearby_animals):
        gamma = self.param['gamma']
        zeta = self.param['zeta']
        w_birth = self.param['w_birth']
        sigma_birth = self.param['sigma_birth']
        prob_birth = self.compute_prob_birth(gamma, self.fitness, nearby_animals)

        if self._weight < zeta * (w_birth + sigma_birth):
            return False
        np.random.choice([True, False], p=[prob_birth, 1 - prob_birth])

    @classmethod
    def _normal_weight(cls):
        start_weight = np.random.normal(cls.param['w_birth'],
                                        cls.param['sigma_birth'])
        return start_weight

    def decrease_birth_weight(self, child_weight):
        xi = self.param['xi']
        self._weight -= xi * child_weight
        self.update_fitness()

    def increase_eat_weight(self, fodder):
        beta = self.param['beta']
        self._weight += beta * fodder
        self.update_fitness()

    def decrease_annual_weight(self):
        eta = self.param['eta']
        self._weight -= eta * self._weight
        self.update_fitness()

    @staticmethod
    def _q_sigmoid(x, x_half, rate, signum):
        return 1 / (1 + math.exp(signum * rate * (x - x_half)))

    @classmethod
    def _calculate_fitness(cls, weight, age):
        a_half = cls.param['a_half']
        phi_age = cls.param['phi_age']
        w_half = cls.param['w_half']
        phi_weight = cls.param['phi_weight']
        if weight == 0:
            return 0
        else:
            return cls._q_sigmoid(age, a_half, phi_age, +1) * cls._q_sigmoid(weight, w_half, phi_weight, -1)

    def update_fitness(self):
        self.fitness = self._calculate_fitness(self._weight, self._age)


class Herbivore(Animal):
    param = {"w_birth": 8.0,
             "sigma_birth": 1.5,
             "beta": 0.9,
             "eta": 0.05,
             "a_half": 40.0,
             "phi_age": 0.2,
             "w_half": 10.0,
             "phi_weight": 0.1,
             "mu": 0.25,
             "lambda": 1.0,
             "gamma": 0.2,
             "zeta": 3.5,
             "xi": 1.2,
             "omega": 0.4,
             "F": 10.0,
             "DeltaPhiMax": 0}

    def __init__(self, weight=None, age=None):
        super().__init__(weight, age)
        pass  # Super location


class Carnivore(Animal):
    param = {"w_birth": 6.0,
             "sigma_birth": 1.0,
             "beta": 0.75,
             "eta": 0.125,
             "a_half": 60.0,
             "phi_age": 0.4,
             "w_half": 4.0,
             "phi_weight": 0.4,
             "mu": 0.4,
             "lambda": 1.0,
             "gamma": 0.8,
             "zeta": 3.5,
             "xi": 1.1,
             "omega": 0.9,
             "F": 50.0,
             "DeltaPhiMax": 10.0}

    def __init__(self, weight=None, age=None):
        # IF none sett til standard verdi
        pass  # Super

    @classmethod
    def compute_kill_prob(cls, min_fit_kill):
        # if
        pass

    def kill(self, min_fit_kill):
        pass
