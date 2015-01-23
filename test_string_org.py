import unittest
import string_org as so    

class TestStringOrg(unittest.TestCase):
    """Testing real_value_vector_org.py"""
    
    def setUp(self):
        so.TARGET_STRING = "CC"
        so.LETTERS = "ABC"

    def test_init(self):
        org = so.StringOrg()
        self.assertEqual(len(so.TARGET_STRING), len(org.genotype))

    def test_random_range(self):
        org = so.StringOrg()
        for locus in org.genotype:
            self.assertIn(locus, so.LETTERS)
        
    def test_init_genotype(self):
        genotype = "AA"
        org = so.StringOrg(genotype)
        self.assertEqual(genotype, org.genotype)

    def test_fitness(self):
        org = so.StringOrg("AA")
        fitness = org.fitness(so.default_environment)
        self.assertEqual(fitness, 0)

    def test_eq_true(self):
        org1 = so.StringOrg("AA")
        org2 = so.StringOrg("AA")
        self.assertTrue(org1 == org2)

    def test_eq_false(self):
        org1 = so.StringOrg("AA")
        org2 = so.StringOrg("BB")
        self.assertFalse(org1 == org2)

    def test_get_clone(self):
        org1 = so.StringOrg("AA")
        org2 = org1.get_clone()
        self.assertEqual(org1, org2)

    def test_get_mutant(self):
        org1 = so.StringOrg("AA")
        org2 = org1.get_mutant()
        self.assertNotEqual(org1, org2)

    def test_str(self):
        org1 = so.StringOrg("CC")
        org2 = so.StringOrg("AA")
        self.assertIs(type(str(org1)), type("CC"))
        self.assertNotEqual(str(org1), str(org2))

    def test_repr(self):
        org1 = so.StringOrg("CC")
        org2 = so.StringOrg("AA")
        self.assertIs(type(repr(org1)), type("CC"))
        self.assertNotEqual(repr(org1), repr(org2))

    def test_is_better_than(self):
        org1 = so.StringOrg("CC")
        org2 = so.StringOrg("AA")
        self.assertTrue(org1.is_better_than(org2, so.default_environment))
        self.assertFalse(org2.is_better_than(org1, so.default_environment))

    def test_get_fitness_perfect(self):
        org = so.StringOrg(so.TARGET_STRING)
        fitness = org.fitness(so.default_environment)
        self.assertEqual(fitness, len(so.TARGET_STRING))

    def test_get_fitness_worst(self):
        terrible_org_genotype = "0" * len(so.TARGET_STRING)
        org = so.StringOrg(terrible_org_genotype)
        fitness = org.fitness(so.default_environment)
        self.assertEqual(fitness, 0)

    def test_get_fitness_one_off(self):
        one_off_genotype = so.TARGET_STRING[:-1] + "0"
        org = so.StringOrg(one_off_genotype)
        fitness = org.fitness(so.default_environment)
        self.assertEqual(fitness, len(so.TARGET_STRING) - 1)

    def test_get_mutated_organism(self):
        org = so.StringOrg()
        mutated_org = org.get_mutant()
        fit = org.fitness(so.default_environment)
        fit_mutated = mutated_org.fitness(so.default_environment)
        fit_difference = abs(fit - fit_mutated)
        self.assertLessEqual(fit_difference, 1)

class StringOrgFunctions(unittest.TestCase):
    """Testing the internal functions of the module."""

    def setUp(self):
        so.TARGET_STRING = "CC"
        so.LETTERS = "ABC"

    def test_get_mutant_genotype(self):
        genotype = "AA"
        mutated_genotype = so._get_mutated_genotype(genotype)
        self.assertNotEqual(genotype, mutated_genotype)

    def test_create_random_genotype(self):
        genotype = so._create_random_genotype()
        self.assertEqual(len(so.TARGET_STRING), len(genotype))

    def test_default_environment_worst(self):
        org = so.StringOrg("AA")
        self.assertEqual(so.default_environment(org.genotype), 0)

    def test_default_environment_okay(self):
        org = so.StringOrg("AC")
        self.assertEqual(so.default_environment(org.genotype), 1)

    def test_default_environment_best(self):
        org = so.StringOrg("CC")
        self.assertEqual(so.default_environment(org.genotype), len(so.TARGET_STRING))

    def test_hash_environment(self):
        org = so.StringOrg("AA")
        self.assertIs(type(so.hash_environment(org.genotype)), int)
