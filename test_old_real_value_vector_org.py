import unittest
import old_real_value_vector_org as rvvo

class TestRealValueVectorOrg(unittest.TestCase):
    """Testing real_value_vector_org.py"""
    
    def setUp(self):
        rvvo.LENGTH = 2
        rvvo.RANGE_MIN = -2
        rvvo.RANGE_MAX = 2
        rvvo.MUTATION_EFFECT_SIZE = 10

    def test_init(self):
        org = rvvo.RealValueVectorOrg()
        self.assertEqual(rvvo.LENGTH, len(org.genotype))

    def test_random_range(self):
        org = rvvo.RealValueVectorOrg()
        for locus in org.genotype:
            self.assertLessEqual(locus, rvvo.RANGE_MAX)
            self.assertGreaterEqual(locus, rvvo.RANGE_MIN)
        
    def test_init_genotype(self):
        genotype = [0,0]
        org = rvvo.RealValueVectorOrg(genotype)
        self.assertEqual(genotype, org.genotype)

    def test_fitness(self):
        org = rvvo.RealValueVectorOrg([0,0])
        fitness = org.fitness(sum)
        self.assertEqual(fitness, 0)

    def test_eq_true(self):
        org1 = rvvo.RealValueVectorOrg([0,0])
        org2 = rvvo.RealValueVectorOrg([0,0])
        self.assertEqual(org1, org2)

    def test_eq_false(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertNotEqual(org1, org2)

    def test_str(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertIs(type(str(org1)), str)
        self.assertNotEqual(str(org1), str(org2))

    def test_repr(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertIs(type(repr(org1)), str)
        self.assertNotEqual(repr(org1), repr(org2))


    def test_get_clone(self):
        org1 = rvvo.RealValueVectorOrg([0,0])
        org2 = org1.get_clone()
        self.assertEqual(org1, org2)

    def test_get_mutant(self):
        org1 = rvvo.RealValueVectorOrg([0,0])
        org2 = org1.get_mutant()
        self.assertNotEqual(org1, org2)

    def test_is_better_than(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertTrue(org1.is_better_than(org2, sum))
        self.assertFalse(org2.is_better_than(org1, sum))

class TestRealValueVectorOrgFunctions(unittest.TestCase):
    """Testing the internal functions of the module."""

    def test_wrap_around(self):
        min_ = -10
        max_ = 10
        qa_dict = {-11:9, 5:5, 11:-9, -31:9, 31:-9}
        for question, answer in qa_dict.items():
            result = rvvo._wrap_around(question, min_, max_)
            self.assertEqual(result, answer)
        
    def test_get_mutant_genotype(self):
        genotype = [0,0]
        mutated_genotype = rvvo._get_mutated_genotype(genotype, 10)
        self.assertNotEqual(genotype, mutated_genotype)

    def test_create_random_genotype(self):
        genotype = rvvo._create_random_genotype()
        self.assertEqual(rvvo.LENGTH, len(genotype))
