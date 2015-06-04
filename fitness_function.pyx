# distutils: language = c++

"""
Supposedly this can be used, have yet to get it to work
# distutils: sources = cpp_fitness_function.cpp
"""

# cython: profile=True
from libcpp.vector cimport vector
cdef extern from "cpp_fitness_function.cpp":
    double cpp_sphere_function(double* vals, long sz)
    double cpp_rosenbrock_function(double* vals, long sz)
    double cpp_rana_function(double* vals, long sz, double* weights)
    double cpp_schafferF7(double* vals, long sz)
    double cpp_deceptive(double* vals, long sz)
    double add_array(double* ary, int size)

from math import floor, sqrt, ceil, cos, sin, fabs
import numpy as np
cimport numpy as np
import scipy.interpolate
import scipy.stats as stats
import random, itertools
from copy import deepcopy
import cython

#from repoze.lru import LRUCache
#cache = LRUCache(128)
#from cpython cimport array as c_array
#from array import array

"""
Example usage:
solution = [2,2]
f = Fitness_Function(sphere_function, 0, 2)
fitness = f.evaluate(solution)
"""
MUTATION_EFFECT_SIZE = 50#None
MOD_SAMPLES = 32 #How sparse should the set of refernce points be
CHANGE_MODIFIER = 50.0 #cludgey multiplier to get environment 2 to be in 
                       #the right ball-park of similarity to environment 1
RANA_WEIGHTS = None #somehow we need to give a constant set of weights to 
                    #the Rana function


#Example of how to get numpy arrays to work
@cython.boundscheck(False)
@cython.wraparound(False)
def array_testing():
    cdef np.ndarray[np.float64_t, mode="c"] a = np.array([1.0,2.0,3.0], ndmin=1)
    cdef int s
    s = a.shape[0]
    return add_array(&a[0], s)


def flat_function(vals):
    """Takes in vals so as not to break when called."""
    return 0.0

def old_sphere_function(vals):
    """
    A very easy test function
    Parameters:
           vals - a list specifying the point in N-dimensionsla space to be
                  evaluated
    OLD, NOT USED
    """
    return sum(val**2 for val in vals)

def sphere_function(np.ndarray[np.float64_t] vals):
    """Very simple function. Sums the squares of each value."""
    cdef long sz = vals.shape[0]
    return cpp_sphere_function(&vals[0], sz)

#Does not work very well; is slower
#def cached_sphere_function(object vals):
#    key_vals = tuple(vals)
#    if(cache.get(key_vals)):
#        return cache.get(key_vals)
#    cdef vector[float] vec = vals
#    cdef float result = cpp_sphere_function(vec)
#    cache.put(key_vals, result)
#    return result

def old_rosenbrock_function(vals):
    """OLD, NOT USED"""
    return sum(100*(vals[i+1] - vals[i]**2)**2 + (vals[i]-1)**2 
               for i in range(len(vals)-1))

def rosenbrock_function(np.ndarray[np.float64_t] vals):
    cdef long sz = vals.shape[0]
    return cpp_rosenbrock_function(&vals[0], sz)

def initialize_rana_weights(length):
    #Initialize temp_weights the same as the old rana weights
    temp_weights = [random.random() for i in range(length)]
    total = sum(temp_weights)
    temp_weights = [i/total for i in temp_weights]
    #Then copy each index over to the array
    global RANA_WEIGHTS
    RANA_WEIGHTS = np.array([], dtype=np.float64)
    for i in range(length):
        RANA_WEIGHTS = np.append(RANA_WEIGHTS, temp_weights[i])

def old_rana_function(vals):
    """OLD, NOT USED"""
    total = 0.0
    for i in range(len(vals)):
        x = vals[i]
        if i == len(vals) - 1:
            y = vals[0]
        else:
            y = vals[i+1]
        #Equation from 
        #http://www.cs.unm.edu/~neal.holts/dga/benchmarkFunction/rana.html
        global RANA_WEIGHTS
        if RANA_WEIGHTS is None:
            initialize_rana_weights(len(vals))

        total += RANA_WEIGHTS[i]*x*sin(sqrt(fabs(y+1-x)))* \
                 cos(sqrt(fabs(x+y+1))) + (y+1)*cos(sqrt(fabs(y+1-x)))* \
                 sin(sqrt(fabs(x+y+1)))
    return total

def rana_function(np.ndarray[np.float64_t] vals):
    cdef long sz = vals.shape[0]
    global RANA_WEIGHTS
    if RANA_WEIGHTS is None:
        initialize_rana_weights(sz)
    #Not ideal, but cannot find a way to have a typed global
    cdef np.ndarray[np.float64_t] weights = RANA_WEIGHTS
    return cpp_rana_function(&vals[0], sz, &weights[0])

def old_schafferF7(vals):
    """OLD, NOT USED"""
    #Equation from 
    #http://www.cs.unm.edu/~neal.holts/dga/benchmarkFunction/schafferf7.html
    total = 0.0
    normalizer = 1.0/float(len(vals))
    for i in range(len(vals)-1):
        si = sqrt(vals[i]**2 + vals[i+1]**2)
        total += (normalizer * sqrt(si) * (sin(50*si**0.20) + 1))**2
    return total

def schafferF7(np.ndarray[np.float64_t] vals):
    cdef long sz = vals.shape[0]
    return cpp_schafferF7(&vals[0], sz)

def old_deceptive(vals):
    """OLD, NOT USED"""
    #Adapted from: http://www.cs.unm.edu/~neal.holts/dga/
    #benchmarkFunction/deceptive.html
    deceptiveness = 0.20 #This is actually more like the 
                    #inverse of deceptiveness since smaller = more deceptive.
    best_fitness = 1.0
    deceptive_best = 0.7
    total = 0.0
    dimensions = len(vals)
    for i in range(dimensions):
        if vals[i] < deceptiveness:
            #Then fitness value is on a negative slope with a y
            #intercept at 1
            total += vals[i]*(-1.0/deceptiveness) \
			+ best_fitness
        else:
            #Otherwise, the fitness value is on a positive slope
            #with an x intercept at deceptiveness
            total += (vals[i]-deceptiveness)* \
                       (deceptive_best/(1.0-deceptiveness))
    return total/float(dimensions)

def deceptive(np.ndarray[np.float64_t] vals):
    cdef long sz = vals.shape[0]
    return cpp_deceptive(&vals[0], sz)

cdef class Fitness_Function:
    """
    Class to store information about the fitness landscape the real value vector orgs
    will be evaluated over.
    """
    cdef object fitness1, fitness2, range_, mods
    cdef int optimal, arglen
    cdef bint flipped
    cdef double corr

    def __init__(self, func, arglen):
        """
        func = fitness function type
        arglen = length of real value vector org
        """
        self.fitness1 = func
        self.fitness2 = None
        self.optimal = 0
        self.arglen = arglen
        self.range_ = (-512, 512)
        self.flipped = False

    #Old version
    #def _python_apply_modgen_to_vals(self, vals, modgen):
    #    """
    #    Apply modgen to each val in vals.
    #    """
    #    def python_put_in_range(val):
    #        if val < self.range_[0]:
    #            return self.range_[0]
    #        if val > self.range_[1]:
    #            return self.range_[1]
    #        return val
    #    return [put_in_range(vals[i] + modgen(vals[i])) for i in range(len(vals))]

    #Cython version
    cdef _apply_modgen_to_vals(self, np.ndarray[np.float64_t] vals, object modgen):
        """
        Apply modgen to each val in vals.
        """
        cdef np.ndarray[np.float64_t] new_vals = np.zeros(vals.shape[0], np.float64)
        cdef double val, mod, val_and_mod
        for i in range(vals.shape[0]):
            val = vals[i]
            mod = modgen(vals[i])
            val_and_mod = val + mod
            if val_and_mod < self.range_[0]:
                new_vals[i] = self.range_[0]
            elif val_and_mod > self.range_[1]:
                new_vals[i] = self.range_[1]
            else:
                new_vals[i] = val_and_mod
        return new_vals
    
    def fitness1_fitness(self, vals):
        return self.fitness1(vals)

    def fitness2_fitness(self, vals):
        if self.fitness2 is None:
            raise AssertionError("Need to initialize fitness2 first")
        return self.fitness2(vals)

    def correlation(self, samples=5000):
        """
        Evaluates a random data set on both fitness functions # of samples times,
        saves the values in two lists, then gets the correlation of the lists
        """
        vals1 = []
        vals2 = []
        #Samples number of times...
        for i in range(samples):
            random_genotype = np.zeros(self.arglen, np.float64)
            #Make a random data set
            for j in range(self.arglen):
                random_genotype[j] = random.randrange(*self.range_)
            #Evaluate it on both fitness functions and save the results
            vals1.append(self.fitness1(random_genotype))
            vals2.append(self.fitness2(random_genotype))
        #Compare all the results against each other and get the r value
        slope, intercept, r_value, p_value, std_err = stats.linregress(vals1, vals2)
        return r_value

    #IS THIS EVER EVEN USED???
    def sd(self, samples=100):
        vals = []
        for i in range(samples):
            solution = []
            for j in range(self.arglen):
                solution.append(random.randrange(*self.range_))
            vals.append(self.fitness1(solution))
        return stats.tstd(vals)

    def create_mods(self):
        """
        Initializes the self.mods dictionary with the pertubations that will be applied to each value.
        """
        #THIS IS THE ONLY PLACE THESE TWO GLOBALS ARE USED, EQUAL TO 50*50.0=250.0
        sd = MUTATION_EFFECT_SIZE  * CHANGE_MODIFIER * (1 - abs(self.corr))
        return [random.normalvariate(0, sd) for _ in range(MOD_SAMPLES + 1)]

    #Old version
    #def python_random_mod(self, val):
    #    """
    #    random_mod is supposed to skew each value
    #    global variable MOD_SAMPLES is the granularity by which the values are skewed
    #    interval is the size of the range divided by the granularity
    #    shifted_val is the val's position in the granularity
    #    """
    #    interval = float(self.range_[1] - self.range_[0])/MOD_SAMPLES
    #    shifted_val = ((self.range_[0]*-1) + val) / interval
    #
    #    ceil_val = int(ceil(shifted_val))
    #    floor_val = int(floor(shifted_val))
    #
    #    sd = MUTATION_EFFECT_SIZE  * CHANGE_MODIFIER * (1 - abs(self.corr))
    #
    #    upper = self.mods[ceil_val]
    #    lower = self.mods[floor_val]
    #    if upper == lower:
    #        return upper
    #    slope = (upper-lower)/float(ceil_val - floor_val)
    #    result = slope*(shifted_val - floor_val) + lower
    #    return result

    #Cython version
    cpdef double random_mod(self, double val):
        """
        random_mod is supposed to skew each value
        global variable MOD_SAMPLES is the granularity by which the values are skewed
        interval is the size of the range divided by the granularity
        shifted_val is the val's position in the granularity
        """
        #Make an interval equal to the range size divided by the number of samples
        cdef double interval = float(self.range_[1] - self.range_[0])/MOD_SAMPLES
        #Shift the val up by half the range (ensuring it is positive), then divide by the interval
        cdef double shifted_val = ((self.range_[0]*-1) + val) / interval
	#Get the ceiling and floor of the shifted val
        cdef int ceil_val = int(ceil(shifted_val))
        cdef int floor_val = int(floor(shifted_val))
	#Make a standard deviation (not ever used???)
        cdef double sd = MUTATION_EFFECT_SIZE  * CHANGE_MODIFIER * (1 - abs(self.corr))
	#Get the upper and lower bounds on the shifted val's location in the mods dict
        cdef double upper = self.mods[ceil_val]
        cdef double lower = self.mods[floor_val]
        #If they're the same, return upper
        if upper == lower:
            return upper
        #Otherwise, get the slope between the bounds
        cdef double slope = (upper-lower)/float(ceil_val - floor_val)
        #Then multiply the slope by the distance shifted val is from floor val, then add lower to it
        cdef double result = slope*(shifted_val - floor_val) + lower
        return result

    def create_fitness2(self, corr):
        def fitness2(vals):
            new_vals = self._apply_modgen_to_vals(vals, self.random_mod)
            return self.fitness1(new_vals)

        self.corr = corr
        self.mods = self.create_mods()
        if corr < 0:
            fitness2 = self.invert(fitness2)
        self.fitness2 = fitness2

    def invert(self, function):
        def inverted(vals):
            return function(vals) * -1
        return inverted

    def get_fitness1(self):
        return self.fitness1

    def get_fitness2(self):
        return self.fitness2
