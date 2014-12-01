import random
from fitness_function import Fitness_Function, sphere_function, MUTATION_EFFECT_SIZE
from functools import total_ordering

LENGTH = None
RANGE_MIN = None
RANGE_MAX = None

@total_ordering
class RealValueVectorOrg(object):
    """
    this is a class that represents organisms as a real value vector
    fitness is determined by calling the fitness fuction
    the length is determined at object creation
    """

    def __init__(self, genotype=None):
        if genotype is None:
            genotype = create_random_genotype()
        assert LENGTH == len(genotype)
        self.genotype = genotype
        self.environment = None

    def fitness(self, environment=None):
        if environment is None:
            if self.environment is None:
                raise AssertionError("Can't call fitness unless you set an environment")
            environment = self.environment
        return environment(self.genotype)

    def get_mutant(self):
        return RealValueVectorOrg(get_mutated_genotype(self.genotype))

    def get_clone(self):
        return RealValueVectorOrg(self.genotype)

    def __lt__(self, other):
        if self.fitness(self.environment) > other.fitness(self.environment):
            return True
        return self.genotype < other.genotype

    def __eq__(self, other):
        return self.genotype == other.genotype

    def __str__(self):
        return "RealValueVectorOrg({})".format(self.genotype)

    def __repr__(self):
        return str(self)

def get_mutated_genotype(genotype):
    "Mutates one locus in organism at random"
    mut_location = random.randrange(len(genotype))
    delta = random.normalvariate(0, MUTATION_EFFECT_SIZE)
    mutant_value = genotype[mut_location] + delta

    mutant = genotype[:]
    mutant[mut_location] = wrap_around(mutant_value)            
    return mutant

def wrap_around(value):
    width = RANGE_MAX - RANGE_MIN
    while value < RANGE_MIN or value > RANGE_MAX:
        if value < RANGE_MIN:
            value += width
        else:
            value -= width
    return value

def create_random_genotype():
    assert (LENGTH is not None and 
            RANGE_MIN is not None and 
            RANGE_MAX is not None), "Module variable must be initialized before use"
    genotype = []
    for _ in range(LENGTH):
        genotype.append(random.uniform(RANGE_MIN, RANGE_MAX))
    return genotype
