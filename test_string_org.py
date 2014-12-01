import unittest
from string_org import *

class TestStringOrgModule(unittest.TestCase):
    
    def test_get_fitness_perfect(self):
        org = StringOrg(TARGET_STRING)
        fitness = org.get_fitness()
        self.assertEqual(fitness, len(TARGET_STRING))

    def test_get_fitness_worst(self):
        terrible_org_genotype = "0" * len(TARGET_STRING)
        org = StringOrg(terrible_org_genotype)
        fitness = org.get_fitness()
        self.assertEqual(fitness, 0)

    def test_get_fitness_one_off(self):
        one_off_genotype = TARGET_STRING[:-1] + "0"
        org = StringOrg(one_off_genotype)
        fitness = org.get_fitness()
        self.assertEqual(fitness, len(TARGET_STRING) - 1)

    def test_get_mutated_organism(self):
        org = StringOrg()
        mutated_org = org.get_mutant()
        fit = org.get_fitness()
        fit_mutated = mutated_org.get_fitness()
        fit_difference = abs(fit - fit_mutated)
        self.assertLessEqual(fit_difference, 1)

    def test_create_random_organism(self):
        StringOrg()

if __name__ == "__main__":
    unittest.main()
