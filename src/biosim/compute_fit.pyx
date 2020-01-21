from libc.math cimport exp

cpdef sigmoidal(double x, double x_half, double rate, int signum):
    return 1 / (1 + exp(signum * rate * (x - x_half)))

cpdef calculate_fitness(int age, double a_half, double phi_age, double weight, double w_half, double phi_weight):
    return sigmoidal(age, a_half, phi_age, +1) * sigmoidal(
                weight, w_half, phi_weight, -1  )
