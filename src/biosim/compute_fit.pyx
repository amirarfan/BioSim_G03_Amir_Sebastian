from libc.math cimport exp

cpdef sigmoidal(double x, double x_half, double rate, int signum):
    r"""
    This is the standard sigmoid function besides that the sign can be
        specified.

        It is given by:

        .. math::
                q^{\pm}(x, x_{\frac{1}{2}},\phi) =
                \frac{1}{1 + e^{\pm \phi (x - x_{\frac{1}{2})}}}



        Parameters
        ----------
        x: int or float
        x_half: int or float
        rate: int or float
        signum: +- 1

        Returns
        -------
        float
            Sigmoid value given the inputs

    """
    return 1 / (1 + exp(signum * rate * (x - x_half)))

cpdef calculate_fitness(int age, double a_half, double phi_age, double weight,
                         double w_half,
                         double phi_weight):
    """
    
    Calculates the fitness using sigmoidal function.
    
    """
    return sigmoidal(age, a_half, phi_age, +1) * sigmoidal(
                weight, w_half, phi_weight, -1  )
