# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

# You may have to run 'python setup.py build_ext --inplace' to make this code
# run. Be sure to have Cython installed, and a C++ compiler.
# Mac uses xCode, on Windows you can download Visual Studio Build tool
# Then add ..\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build
# To system path. Contact me at amar@nmbu.no, if you have trouble
# running the cython code on Mac or Windows.
import math

from numba import jit
import numpy as np
import random
from .compute_fit import calculate_fitness
from .det_kill import det_kill


class Animal:
    """
    Animal class used as a base for Herbivore and Carnivore sub-classes
    """

    param = {}
    allowed_landscape = ["Jungle", "Desert", "Savannah"]

    @classmethod
    def update_parameters(cls, new_par_dict):
        """
        Updates the current parameters and also checks that no parameters are
        negative.

        Parameters
        ----------
        new_par_dict: Dictionary
                    New dictionary containing the new parameters which need to
                    be updated.

        """
        for par in new_par_dict.keys():
            if par not in cls.param:
                raise ValueError(
                    f"Invalid input: {par} is not a key in "
                    f"class parameters"
                )
            if (
                new_par_dict[par] <= 0
                and par == "DeltaPhiMax"
                and cls.__name__ == "Carnivore"
            ):
                raise ValueError(f"{par} must be strictly positive")
            elif new_par_dict[par] < 0 and par != "DeltaPhiMax":
                raise ValueError(f"{par} must be positive")
            elif new_par_dict[par] > 1 and (par == "eta" or par == "p_sick"):
                raise ValueError(f"{par} must be less or equal to 1")

        cls.param.update(new_par_dict)

    def __init__(self, weight=None, age=None):
        """

        Initializes the Animal class instance.

        Parameters
        ----------
        age: int [default=none]
            The age of the animal to be initialised
        weight: float or int [default=none]
            The weight of the animal to be initialised
        """

        if age is not None and ((age < 0) or (type(age) != int)):
            raise ValueError("Age cannot be lower than 0")

        if age is not None:
            self._age = age
        else:
            self._age = 0

        if weight is not None and weight < 0:
            raise ValueError("Weight cannot be lower than 0")
        elif weight is not None and weight > 0:
            self._weight = weight
        else:
            self._weight = self._normal_weight()

        self.has_migrated = False

        self._should_update_fitness = False
        self._fitness = None

        self.is_sick = False

    @property
    def age(self):
        """
        Property method for age

        Returns
        -------
        _age: int
            The current age of the animal instance

        """
        return self._age

    @age.setter
    def age(self, val):
        """

        Setter method for age property. Updates self._age, and updates the
        fitness of the animal as well

        Parameters
        ----------
        val: int
            The new age the animal is supposed to be

        """
        if val < 0:
            raise ValueError("Age must be higher than 0")

        if type(val) != int:
            raise ValueError("Age must be a positive integer")

        self._age = val
        self.update_fitness()

    @property
    def weight(self):
        """
        Property function for the Animal's weight

        Returns
        -------
        _weight: int or float
            Returns the current weight of the animal instance

        """
        return self._weight

    @weight.setter
    def weight(self, val):
        """
        Setter method for the weight property. Updates the weight value and
        also updates the fitness

        Parameters
        ----------
        val: int or float
            New weight value to be assigned

        """
        if val < 0:
            raise ValueError("Weight must be higher than 0")
        self._weight = val
        self._should_update_fitness = True

    @property
    def fitness(self):
        """

        Property method for the fitness

        Returns
        -------
        _fitness = float
            The current fitness value of the animal instance

        """
        if self._should_update_fitness or self._fitness is None:
            self.update_fitness()
            self._should_update_fitness = False
        return self._fitness

    @classmethod
    def _calculate_fitness(cls, weight, age):
        r"""

        Calculates the fitness by using the 'calculate_fitness'
        function which uses the parameters from the class. 'calculate_fitness'
        is a cythonized function.

        .. math::
            \Phi =
            \begin{cases}
            0 & \text{for }w\le0\\
            q^{+}(a, a_{\frac{1}{2}},\phi_{age}) \times
            q^{-}(w, w_{\frac{1}{2}},\phi_{weight}) & \text{else}
            \end{cases}

        Parameters
        ----------
        weight: int or float
            Weight of the animal class instance
        age: int
            Age of the animal class instance

        Returns
        -------
        float
            The new value of fitness using the _q_sigmoid function with
            different sign values :math:`+`, and  :math:`-`

        """
        a_half = cls.param["a_half"]
        phi_age = cls.param["phi_age"]
        w_half = cls.param["w_half"]
        phi_weight = cls.param["phi_weight"]
        if weight == 0:
            return 0
        else:
            return calculate_fitness(
                age, a_half, phi_age, weight, w_half, phi_weight
            )

    def update_fitness(self):
        """
        Updates the 'self._fitness' variable using '_calculate_fitness'
        method
        """
        self._fitness = self._calculate_fitness(self._weight, self._age)

    def add_age(self):
        """
        Updates the '_age' variable in the class instance by one, also updates
        the fitness when age is updated.

        """
        self._age += 1
        self._should_update_fitness = True

    def determine_to_move(self):
        """

        Calculates the probability to move, and then returns a bool value
        deciding whether animal is to move.

        Returns
        -------
        bool
            Returns True if Animal is to move, or false if it is not to move

        """
        probability_move = self.fitness * self.param["mu"]
        return np.random.random() < probability_move

    def compute_move_prob(self, neighbour_cells):
        """

        Computes the probability to move to each neighbouring cell

        Parameters
        ----------
        animal_type: class instance
                     Takes in a specific class instance
        neighbour_cells:
                    Takes in the neighbouring cells of the cell the animal
                    class instance is located at

        Returns
        -------

        list
            List containing probability to move to each cell


        """
        cell_propensity = []
        for cell in neighbour_cells:
            propensity_cell = self.propensity(cell)
            cell_propensity.append(propensity_cell)

        total_propensity = sum(cell_propensity)

        computed_propensities = []
        for cell_prop in cell_propensity:
            try:
                prob = cell_prop / total_propensity
            except ZeroDivisionError:
                prob = 0
            computed_propensities.append(prob)
        return computed_propensities

    def propensity(self, cell):
        r"""

        Computes and returns the propensity to move, the relative abundance is
        calculated through the 'compute_relative_abundance' function.
        The formula for propensity is given by:

        .. math::
            \pi_{i\rightarrow j} =
            \begin{cases}
            0 & \text{if } j \text{is Mountain or Ocean}\\
            e^{\lambda \epsilon_{j}} & \text{otherwise}
            \end{cases}


        Parameters
        ----------
        cell: cell instance
            The cell instance of neighbouring cells.

        Returns
        -------
        float
            The propensity to move

        """
        cell_name = type(cell).__name__
        if cell_name not in self.allowed_landscape:
            return 0

        relative_abundance = self.compute_relative_abundance(cell)
        lambda_specie = self.param["lambda"]

        return math.exp(lambda_specie * relative_abundance)

    @classmethod
    def compute_relative_abundance(cls, cell):
        r"""

        Computes the relative abundance for either herbivore or carnivore,
        depending on the specie type.

        The relative abundance is computed through this formula:

        .. math::
            \epsilon_{k} = \frac{f_{k}}{(n_{k}+1)F^{\text{'}}}

        Where :math:`\epsilon_{k}` is the relative abundance. :math:`f_{k}` is
        the current fodder for cell k, which is different for carnivores
        and herbivores. :math:`n_{k}` is the amount of same species in cell
        k, and :math:`F^{\text{'}}` is how much food the animal wants to eat.

        Parameters
        ----------
        cell: Cell instance
            The cell instance one needs to calculate the relative abundance
            for.

        Returns
        -------
        float
            The relative abundance of the current cell

                """

        pass

    def determine_death(self):
        """

        Calculates the probability of death for the animal instance, uses that
        probability and random.uniform function to return a bool value.

        Returns
        -------
        bool
            Returns True if Animal instance is to die, and False if it is not
            to die

        """
        death_prob = 0
        if self.fitness == 0:
            return True
        elif self.fitness > 0.01:
            death_prob = self.param["omega"] * (1 - self.fitness)

        return np.random.random() < death_prob

    def determine_birth(self, nearby_animals):
        r"""
        Determines whether the animal is to give birth or not using
        the 'compute_prob_birth' function to gain a value. The function then
        uses random.uniform to choose between True or False with fixed
        probabilities.

          Computes the probability of birth for the animal, using the equation

        .. math::
            \text{min}(1, \gamma \times \Phi \times (N-1))

        Parameters
        ----------
        nearby_animals: int
                       The amount of animals nearby in the same area (cell)

        Returns
        -------
        bool
            True if the animal is to give birth, False if the animal is not
            to give birth.

        """
        gamma = self.param["gamma"]
        zeta = self.param["zeta"]
        w_birth = self.param["w_birth"]
        sigma_birth = self.param["sigma_birth"]
        xi = self.param["xi"]

        if nearby_animals < 2 or self._weight < zeta * (w_birth + sigma_birth):
            return None
        prob_birth = min(1, gamma * self.fitness * (nearby_animals - 1))
        if np.random.random() < prob_birth:
            child_weight = self._normal_weight()
            if xi * child_weight > self.weight:
                return None
            self.decrease_birth_weight(child_weight)
            return type(self)(weight=child_weight)
        else:
            return None

    @classmethod
    def _normal_weight(cls):
        r"""
        Class method which returns the birth weight using a Gaussian
        distribution, where it gets the mean and standard deviation from the
        class parameters.

        .. math::
            \text{w} \sim \cal{N}(\text{w}_{\text{birth}},\sigma_{
            \text{birth}})

        Where :math:`w_{birth}` is the mean, and :math:`sigma_{birth}` is
        the standard deviation.

        Returns
        -------
        start_weight = int or float
            The birth weight value gotten from the normal distribution.


        """
        start_weight = np.random.normal(
            cls.param["w_birth"], cls.param["sigma_birth"]
        )
        return start_weight

    def decrease_birth_weight(self, child_weight):
        r"""
        Updates '_weight' each time an animal class instance gives birth,
        by reducing the animal class instance's birth by :math:`\zeta` times
        the birth-giving animal's weight.

        It also updates the fitness after the weight has been altered.

        Parameters
        ----------
        child_weight: int or float
            The weight of the new-born child.

        """
        xi = self.param["xi"]
        self._weight -= xi * child_weight
        self._should_update_fitness = True

    @classmethod
    def _determine_sick(cls):
        """

        Determines if the animal is to become sick, using the 'p_sick'
        parameter and random.uniform method.

        Returns
        -------
        bool
            True or False

        """
        p_sick = cls.param["p_sick"]
        return np.random.random() < p_sick

    def increase_eat_weight(self, fodder):
        """
        Increases the animal class instance's weight by :math:`\beta` times
        the current weight of the instance. The function also updates
        the fitness of the animal class instance using 'update_fitness'.

        Parameters
        ----------
        fodder: int or float
            Amount of food the animal instance is to eat.

        """

        self.is_sick = self._determine_sick()
        beta = self.param["beta"]
        loss_rate = self.param["loss_rate"]

        if self.is_sick:
            self._weight += beta * fodder * loss_rate
        else:
            self._weight += beta * fodder
        self._should_update_fitness = True

    def decrease_annual_weight(self):
        r"""
        Decreases weight by :math:`\eta times the current weight. The function
        also updates the fitness of the animal instance by using the
        'update_fitness' method.

        """
        eta = self.param["eta"]
        self._weight -= eta * self._weight
        self._should_update_fitness = True


class Herbivore(Animal):
    """
    Herbivore is a subclass of Animal class. Uses super method to inherit
    the attributes and methods from animal class.
    """

    param = {
        "w_birth": 8.0,
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
        "DeltaPhiMax": 0,
        "p_sick": 0,
        "loss_rate": 0.8,
    }

    def __init__(self, weight=None, age=None):
        """

         Initialises the Herbivore class

        Parameters
        ----------
        weight: int or float
            Weight of the Herbivore to be initialised
        age
            Age of the Herbivore to be initalised
        """
        super().__init__(weight, age)

    @classmethod
    def compute_relative_abundance(cls, cell):
        animal_name = cls.__name__
        amount_same_spec = len(cell.animal_classes[animal_name])
        food_wanting = cls.param["F"]
        curr_fod = cell.current_fodder
        if curr_fod == 0:
            return 0
        else:
            return curr_fod / ((amount_same_spec + 1) * food_wanting)


class Carnivore(Animal):
    """
    Carnivore is a subclass of Animal. Uses super method to inherit methods
    and specified attributes from Animal class.
    """

    param = {
        "w_birth": 6.0,
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
        "DeltaPhiMax": 10.0,
        "p_sick": 0,
        "loss_rate": 0.8,
    }

    def __init__(self, weight=None, age=None):
        """
        Initialises the Carnivore class.

        Parameters
        ----------
        weight: int or float
            Weight of the Herbivore to be initialised
        age: int
            Age of the Herbivore to be initialised
        """
        super().__init__(weight, age)

    # @staticmethod
    # @jit(nopython=True, fastmath=True)
    # def _compute_kill_prob(fit_carn, fit_herb, delta_phi_max):
    #     r"""
    #     Computes probability of a Carnivore killing Herbivore which is
    #     determined through:
    #
    #     .. math::
    #         p =
    #         \begin{cases}
    #         0 & \text{if }\Phi_{carn}\le \Phi_{herb}\\
    #         \frac{\Phi_{carn} - \Phi_{herb}}{\Delta\Phi_{max}} &
    #         \text{if } 0 \le \Phi_{carn} - \Phi_{herb} \le \Delta\Phi_{max}\\
    #         1 & \text{otherwise}
    #         \end{cases}
    #
    #
    #
    #     Parameters
    #     ----------
    #     fit_carn: int or float
    #         Fitness of the Carnivore which is the predator
    #     fit_herb: int or float
    #         Fitness of the Herbivore which is the prey
    #     delta_phi_max: int or float
    #         Parameter for Carnivore
    #
    #
    #     Returns
    #     -------
    #     float or int
    #         The probability of the carnivore killing the herbivore
    #
    #     """
    #     if fit_carn <= fit_herb:
    #         return 0
    #     elif 0 < fit_carn - fit_herb < delta_phi_max:
    #         return (fit_carn - fit_herb) / delta_phi_max
    #     else:
    #         return 1

    def determine_kill(self, min_fit_herb):
        """

        Determine kill function which uses '_compute_kill_prob' to
        calculate the probability and then uses random choice with
        fixed probability to determine if the carnivore is to kill
        the chosen herbivore.

        Parameters
        ----------
        min_fit_herb: int or float
                    Fitness of the herbivore which is to be preyed upon
                    by the carnivore.

        Returns
        -------
        bool
            Returns true or false determining whether the carnivore is to kill
            the herbivore or not

        """

        delta_phi_max = self.param["DeltaPhiMax"]
        return det_kill(self.fitness, min_fit_herb, delta_phi_max)

    @classmethod
    def compute_relative_abundance(cls, cell):
        animal_name = cls.__name__
        amount_same_spec = len(cell.animal_classes[animal_name])
        food_wanting = cls.param["F"]
        curr_food = sum(
            herbivore.weight for herbivore in cell.animal_classes["Herbivore"]
        )
        if curr_food == 0:
            return 0
        else:
            return curr_food / ((amount_same_spec + 1) * food_wanting)
