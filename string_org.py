import random

TARGET_STRING = None
LETTERS = None

class StringOrg(object):
    """
    this is a class that represents organisms as a string
    fitness equals distance to the target string
    """

    should_maximize_fitness = True

    def __init__(self, genotype=None):
        if genotype is None:
            genotype = _create_random_genotype()
        assert len(genotype) == len(TARGET_STRING)
        self.genotype = genotype

    def fitness(self, environment):
        return environment(self.genotype)

    def get_mutant(self):
        return StringOrg(_get_mutated_genotype(self.genotype))

    def __eq__(self, other):
        return self.genotype == other.genotype

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "StringOrg(\"{}\")".format(self.genotype)

    def __repr__(self):
        return str(self)

    def get_clone(self):
        return StringOrg(self.genotype)

    def is_better_than(self, other, environment):
        return self.fitness(environment) > other.fitness(environment)

def _get_mutated_genotype(genotype):
    "Mutates one character in organism at random"
    mut_location = random.randrange(len(TARGET_STRING))
    while True:
        mut_letter = random.choice(LETTERS)
        if mut_letter != genotype[mut_location]:
            return genotype[:mut_location] + mut_letter + genotype[mut_location + 1:]

def default_environment(genotype):
    "Returns the number of matching letters between org and target"
    matches = 0
    for i in range(len(TARGET_STRING)):
        if TARGET_STRING[i] == genotype[i]:
            matches += 1
    return matches

def hash_environment(genotype):
    return hash(genotype)

def _create_random_genotype():
    genotype = []
    for _ in range(len(TARGET_STRING)):
        genotype.append(random.choice(LETTERS))
    return "".join(genotype)
