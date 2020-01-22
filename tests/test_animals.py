# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from biosim.animals import Herbivore, Carnivore
import pytest
from scipy.stats import normaltest
from scipy.stats import shapiro


@pytest.fixture
def plain_herbivore():
    """

    Pytest fixture which returns a standard Herbivore class

    """
    return Herbivore()


def test_new_herbivore_age():
    """

    Tests that when you initalize a new Herbivore class, the age is equal to 0

    """
    herb = Herbivore()
    assert herb.age == 0


def test_herbivore_custom_neg_age():
    """

    Tests that setting negative age when initialising a new Herbivore instance
    ValueError is raised.


    """
    # Try - Except could also be used here
    with pytest.raises(ValueError):
        Herbivore(age=-1)


def test_herbivore_custom_pos_age():
    """

    Tests that initialising a new Herbivore class instance with a specific
    age works.

    """
    herb = Herbivore(age=2)
    assert herb.age == 2


def test_herbivore_setter_method_age(plain_herbivore):
    """

    Tests setting Herbivore age works

    Parameters
    ----------
    plain_herbivore: class instance
                    Herbivore class instance from fixture


    """
    plain_herbivore.age = 2
    assert plain_herbivore.age == 2


def test_herbivore_setter_method_neg_age(plain_herbivore):
    """

    Checks if 'ValueError' is raised when assigning a negative age to an
    already existing instance of Herbivore.

    Parameters
    ----------
    plain_herbivore: class instance
                    Herbivore class instance from fixture


    """
    try:
        plain_herbivore.age = -1
    except ValueError as ve:
        print(ve)


def test_herbivore_non_int_setter_age(plain_herbivore):
    """

    Tests that non-int value of age raises 'ValueError'

    Parameters
    ----------
    plain_herbivore: class instance
                    Herbivore class instance from fixture

    """
    with pytest.raises(ValueError):
        plain_herbivore.age = 2.1


def test_herbivore_actually_ages(plain_herbivore):
    """

    Tests the add age function from Animal class from 'animals.py'.

    Parameters
    ----------
    plain_herbivore: class instance
                    Herbivore class instance from fixture


    """
    first_age = plain_herbivore.age
    plain_herbivore.add_age()
    second_age = plain_herbivore.age
    assert first_age < second_age


def test_herbivore_continual_aging():
    """
    Tests that add_age function from Animal class from 'animals.py' works
    when called several times.

    """
    herb = Herbivore()
    for i in range(10):
        herb.add_age()
        assert i + 1 == herb.age


def test_herbivore_weight(plain_herbivore):
    assert plain_herbivore.weight is not None
    assert plain_herbivore.weight != 0


def test_herbivore_change_weight(plain_herbivore):
    plain_herbivore.weight = 2
    assert plain_herbivore.weight == 2


def test_herbivore_neg_weight():
    # One could also use try except here
    with pytest.raises(ValueError) as ve:
        Herbivore(-1)


def test_herbivore_custom_pos_weight():
    herb = Herbivore(weight=20)
    assert herb.weight == 20


def test_herbivore_custom_weight_setter(plain_herbivore):
    with pytest.raises(ValueError):
        plain_herbivore.weight = -20


def test_herbivore_fitness_changes_with_weight(plain_herbivore):
    before_fitness = plain_herbivore.fitness
    plain_herbivore.weight = 30
    after_fitness = plain_herbivore.fitness
    assert before_fitness != after_fitness


def test_herbivore_fitness_not_zero():
    herb = Herbivore()
    assert herb._fitness != 0


def test_fitness_setter_negval(plain_herbivore):
    with pytest.raises(ValueError) as ve:
        plain_herbivore.fitness = -1


def test_non_existing_parameter_herbivore(plain_herbivore):
    with pytest.raises(ValueError):
        plain_herbivore.update_parameters({"non_exist": 20})


def test_negative_parameter_herbivore(plain_herbivore):
    with pytest.raises(ValueError):
        plain_herbivore.update_parameters({"sigma_birth": -20})


def test_eta_greater_than_one_herbivore(plain_herbivore):
    with pytest.raises(ValueError):
        plain_herbivore.update_parameters({"eta": 2})


def test_deltaphimax_negative(plain_carnivore):
    with pytest.raises(ValueError):
        plain_carnivore.update_parameters({"DeltaPhiMax": -1})


def test_parameters_actually_update(plain_herbivore):
    prev_param = plain_herbivore.param.copy()
    plain_herbivore.update_parameters({"DeltaPhiMax": 5})
    assert prev_param != plain_herbivore.param


def test_determine_death_zero_fitness():
    herb = Herbivore()
    herb.fitness = 0
    assert herb.determine_death() is True


def test_determine_death_is_bool():
    herb = Herbivore()
    assert type(herb.determine_death()) == bool


def test_determine_death_mocker(mocker):
    mocker.patch("random.uniform", return_value=0)
    herb = Herbivore()
    assert herb.determine_death()


def test_determine_birth_no_animals():
    herb = Herbivore()
    assert herb.determine_birth(0) is False


def test_determine_birth_is_bool():
    herb = Herbivore()
    herb.weight = 100
    assert type(herb.determine_birth(100)) == bool


def test_move_probability_herb():
    herb = Herbivore()
    bool_val = herb.determine_to_move()
    assert type(bool_val) == bool


def test_move_prob_herb_true(mocker):
    mocker.patch("random.uniform", return_value=0)
    herb = Herbivore()
    assert herb.determine_to_move()


@pytest.fixture
def plain_carnivore():
    return Carnivore()


def test_new_carnivore_age():
    carn = Carnivore()
    assert carn.age == 0


def test_carnivore_fitness_change_when_eat(plain_carnivore):
    prev_fitness = plain_carnivore.fitness
    plain_carnivore.increase_eat_weight(20)
    assert plain_carnivore.fitness != prev_fitness


def test_carnivore_weight_change_when_eat(plain_carnivore):
    prev_weight = plain_carnivore.weight
    plain_carnivore.increase_eat_weight(10)
    assert prev_weight < plain_carnivore.weight


def test_carnivore_actually_ages(plain_carnivore):
    prev_age = plain_carnivore.age
    plain_carnivore.add_age()
    assert plain_carnivore.age > prev_age


def test_carnivore_birth_decrease_weight(plain_carnivore):
    prev_weight = plain_carnivore.weight
    plain_carnivore.decrease_birth_weight(20)
    assert plain_carnivore.weight < prev_weight


def test_decrease_annual_weight(plain_carnivore, plain_herbivore):
    prev_weight_carn, prev_weight_herb = (
        plain_carnivore.weight,
        plain_herbivore.weight,
    )
    plain_carnivore.decrease_annual_weight()
    plain_herbivore.decrease_annual_weight()
    assert plain_carnivore.weight < prev_weight_carn
    assert plain_herbivore.weight < prev_weight_herb


def test_kill_probability_gf_herb():
    # Herbivore has greater fitness
    carn = Carnivore()
    prob = carn._compute_kill_prob(0.4, 0.9, 10)
    assert prob == 0


def test_kill_probability_gf_carn():
    # Carnivore has greater fitness
    carn = Carnivore()
    prob = carn._compute_kill_prob(10, 0.1, 5)
    assert prob == 1


def test_bool_carnivore_det_kill(plain_carnivore):
    kill_prob = plain_carnivore.determine_kill(0.20)
    assert type(kill_prob) is bool


def test_det_kill_false(plain_carnivore, mocker):
    mocker.patch("random.uniform", return_value=1)
    assert not plain_carnivore.determine_kill(0.01)


def test_fitness_weight_zero():
    """
    Test that fitness is zero if weight is zero

    """
    herb = Herbivore()
    assert herb._calculate_fitness(0, 1) == 0


def test_gauss_distribution_pearson():
    """
    Tests the gauss distribution used for starting weights for animal classes

    Uses Scipys normal test to test for normal distribution.

    Alpha value is set to 0.05 to test for significance levels.

    The test out puts the statistics and the probability, if the probability
    is lower than the alpha value, one can say that the null hypothesis is
    confirmed and the normal distribution holds.

    """
    herbivores = [Herbivore() for _ in range(5000)]
    carnivores = [Carnivore() for _ in range(5000)]
    herb_weights = [herb.weight for herb in herbivores]
    carn_weights = [carn.weight for carn in carnivores]
    alpha = 0.05
    herb_stat, herb_p = normaltest(herb_weights)
    carn_stat, carn_p = normaltest(carn_weights)

    assert herb_p > alpha

    assert carn_p > alpha


def test_gauss_distribution_shapiro():
    """
    Tests the gauss distribution  used for starting weights for animal classes

    Uses the Shapiro Wilk tests to test the normal distribution

    The Shapiro Wilk outputs the statistic and the probability (p-value)
     of obtaining the observed results of a test. The lower the probability
     the more the null hypothesis seems significant. Null hypothesis being in
     this test that the test data is normally distributed.

     We define a significance level (alpha) which can be seen as threshold.
     If the p-value is lower than alpha, one can say that the null hypothesis
     is more insignificant.

    """
    herbivores = [Herbivore() for _ in range(5000)]
    carnivores = [Carnivore() for _ in range(5000)]
    herb_weights = [herb.weight for herb in herbivores]
    carn_weights = [carn.weight for carn in carnivores]
    alpha = 0.05  # Sets the probability of rejecting the null hypothesis

    herb_stat, herb_p = shapiro(herb_weights)
    carn_stat, carn_p = shapiro(carn_weights)

    assert herb_p > alpha

    assert carn_p > alpha


def test_sick_herbivores_eat(mocker):
    """
    Simple test to check if a sick animal loses more weight than a healthy
    animal.

    """
    healthy_herb = Herbivore(weight=10)
    sick_herb = Herbivore(weight=10)
    healthy_herb.increase_eat_weight(10)
    sick_herb.update_parameters({"p_sick": 1})

    mocker.patch("random.uniform", return_value=0)
    sick_herb.increase_eat_weight(10)

    assert healthy_herb.weight > sick_herb.weight
