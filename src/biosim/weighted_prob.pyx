from numpy.random import rand

cpdef weighted_prob(list weights):
    cdef double cs
    cdef double random
    cpdef int length
    length = len(weights)
    random = rand()
    cs = 0.0
    i = 0
    while cs < random and i < length:
        cs += weights[i]
        i += 1
    return i-1