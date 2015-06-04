from math import floor, sqrt, ceil, cos, sin, fabs
import numpy as np
import scipy.interpolate
import scipy.stats as stats
import random, itertools
from copy import deepcopy

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


def flat_function(vals):
    """Takes in vals so as not to break when called."""
    return 0

def sphere_function(vals):
    """
    A very easy test function
    Parameters:
           vals - a list specifying the point in N-dimensionsla space to be
                  evaluated
    """
    return sum(val**2 for val in vals)

def rosenbrock_function(vals):
    return sum(100*(vals[i+1] - vals[i]**2)**2 + (vals[i]-1)**2 
               for i in range(len(vals)-1))

def initialize_rana_weights(vals):
    global RANA_WEIGHTS
    RANA_WEIGHTS = [random.random() for i in range(len(vals))]
    total = sum(RANA_WEIGHTS)
    RANA_WEIGHTS = [i/total for i in RANA_WEIGHTS]


def rana_function(vals):
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
            initialize_rana_weights(vals)

        total += RANA_WEIGHTS[i]*x*sin(sqrt(fabs(y+1-x)))* \
                 cos(sqrt(fabs(x+y+1))) + (y+1)*cos(sqrt(fabs(y+1-x)))* \
                 sin(sqrt(fabs(x+y+1)))
    return total

def schafferF7(vals):
    #Equation from 
    #http://www.cs.unm.edu/~neal.holts/dga/benchmarkFunction/schafferf7.html
    total = 0.0
    normalizer = 1.0/float(len(vals))
    for i in range(len(vals)-1):
        si = sqrt(vals[i]**2 + vals[i+1]**2)
        total += (normalizer * sqrt(si) * (sin(50*si**0.20) + 1))**2
    return total

def deceptive(vals):
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

class Fitness_Function:

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

    def _apply_modgen_to_vals(self, vals, modgen):
        """
        Apply modgen to each val in vals.
        """
        def put_in_range(val):
            if val < self.range_[0]:
                return self.range_[0]
            if val > self.range_[1]:
                return self.range_[1]
            return val
        return [put_in_range(vals[i] + modgen(vals[i])) for i in range(len(vals))]

    def fitness1_fitness(self, vals):
        return self.fitness1(vals)

    def fitness2_fitness(self, vals):
        if self.fitness2 is None:
            raise AssertionError("Need to initialize fitness2 first")
        return self.fitness2(vals)

    def correlation(self, samples=5000):
        vals1 = []
        vals2 = []
        for i in range(samples):
            solution = []
            for j in range(self.arglen):
                solution.append(random.randrange(*self.range_))
            vals1.append(self.fitness1(solution))
            vals2.append(self.fitness2(solution))
        slope, intercept, r_value, p_value, std_err = stats.linregress(vals1, vals2)

        return r_value

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
        sd = MUTATION_EFFECT_SIZE  * CHANGE_MODIFIER * (1 - abs(self.corr))
        return [random.normalvariate(0, sd) for _ in range(MOD_SAMPLES + 1)]

    def random_mod(self, val):
        """
        random_mod is supposed to skew each value
        global variable MOD_SAMPLES is the granularity by which the values are skewed
        interval is the size of the range divided by the granularity
        shifted_val is the val's position in the granularity
        """
        interval = float(self.range_[1] - self.range_[0])/MOD_SAMPLES
        shifted_val = ((self.range_[0]*-1) + val) / interval

        ceil_val = int(ceil(shifted_val))
        floor_val = int(floor(shifted_val))

        sd = MUTATION_EFFECT_SIZE  * CHANGE_MODIFIER * (1 - abs(self.corr))

        upper = self.mods[ceil_val]
        lower = self.mods[floor_val]
        if upper == lower:
            return upper
        slope = (upper-lower)/float(ceil_val - floor_val)
        result = slope*(shifted_val - floor_val) + lower
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
