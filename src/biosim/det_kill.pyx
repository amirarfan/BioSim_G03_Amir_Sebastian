import random

cpdef det_kill(double fit_carn,  double fit_herb, double delta_phi_max):
    r"""
    Computes probability of a Carnivore killing Herbivore which is
    determined through:

    .. math::
        p =
        \begin{cases}
        0 & \text{if }\Phi_{carn}\le \Phi_{herb}\\
        \frac{\Phi_{carn} - \Phi_{herb}}{\Delta\Phi_{max}} &
        \text{if } 0 \le \Phi_{carn} - \Phi_{herb} \le \Delta\Phi_{max}\\
        1 & \text{otherwise}
        \end{cases}



    Parameters
    ----------
    fit_carn: int or float
        Fitness of the Carnivore which is the predator
    fit_herb: int or float
        Fitness of the Herbivore which is the prey
    delta_phi_max: int or float
        Parameter for Carnivore


    Returns
    -------
    float or int
        The probability of the carnivore killing the herbivore

    """
    if fit_carn <= fit_herb:
       kill_prob =  0
    elif 0 < fit_carn - fit_herb < delta_phi_max:
       kill_prob =  (fit_carn - fit_herb) / delta_phi_max
    else:
        kill_prob = 1

    return random.uniform(0,1)<kill_prob

