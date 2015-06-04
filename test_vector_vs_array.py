import unittest
import old_real_value_vector_org as rvvo #Original vectors
import real_value_vector_org as arr #New arrays

class TestVectorOrgVsArrayOrg(unittest.TestCase):
    """Testing old_real_value_vector_org.py against real_value_vector_org.py"""
    
    def setUp(self):
        rvvo.LENGTH = arr.LENGTH = 2
        rvvo.RANGE_MIN = arr.RANGE_MIN = -2
        rvvo.RANGE_MAX = arr.RANGE_MAX = 2
        rvvo.MUTATION_EFFECT_SIZE = arr.MUTATION_EFFECT_SIZE = 10

    def test_init(self):
        vector_org = rvvo.RealValueVectorOrg()
        array_org = arr.RealValueVectorOrg()
        self.assertEqual(rvvo.LENGTH, len(vector_org.genotype))
        self.assertEqual(arr.LENGTH, array_org.genotype.shape[0])

    def test_random_range(self):
        vector_org = rvvo.RealValueVectorOrg()
        array_org = arr.RealValueVectorOrg()
        for locus in vector_org.genotype:
            self.assertLessEqual(locus, rvvo.RANGE_MAX)
            self.assertGreaterEqual(locus, rvvo.RANGE_MIN)
        for locus in array_org.genotype:
            self.assertLessEqual(locus, arr.RANGE_MAX)
            self.assertGreaterEqual(locus, arr.RANGE_MIN)

    def test_init_genotype(self):
        genotype = [0,0]
        vector_org = rvvo.RealValueVectorOrg(genotype)
        array_org = arr.RealValueVectorOrg(genotype)
        self.assertEqual(genotype, vector_org.genotype)
        self.assertEqual((arr.RealValueVectorOrg(vector_org.genotype)==array_org).all(), True)

    def test_fitness(self):
        vector_org = rvvo.RealValueVectorOrg([0,0])
        vector_fitness = vector_org.fitness(sum)
        array_org = arr.RealValueVectorOrg([0,0])
        array_fitness = array_org.fitness(sum)
        self.assertEqual(vector_fitness, 0)
        self.assertEqual(array_fitness, 0)

    def test_eq_true(self):
        org1 = rvvo.RealValueVectorOrg([0,0])
        org2 = rvvo.RealValueVectorOrg([0,0])
        self.assertEqual(org1, org2)
        org3 = arr.RealValueVectorOrg([0,0])
        org4 = arr.RealValueVectorOrg([0,0])
        self.assertEqual((org3==org4).all(), True)

    def test_eq_false(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertNotEqual(org1, org2)
        org3 = arr.RealValueVectorOrg([0,0])
        org4 = arr.RealValueVectorOrg([0,1])
        self.assertNotEqual((org3==org4).all(), True)

    def test_str(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertIs(type(str(org1)), str)
        self.assertNotEqual(str(org1), str(org2))
        org3 = arr.RealValueVectorOrg([0,0])        
        org4 = arr.RealValueVectorOrg([0,1])
        self.assertIs(type(str(org3)), str)
        self.assertNotEqual(str(org3), str(org4))

    def test_repr(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertIs(type(repr(org1)), str)
        self.assertNotEqual(repr(org1), repr(org2))
        org3 = arr.RealValueVectorOrg([0,0])        
        org4 = arr.RealValueVectorOrg([0,1])
        self.assertIs(type(repr(org3)), str)
        self.assertNotEqual(repr(org3), repr(org4))

    def test_get_mutant(self):
        org1 = rvvo.RealValueVectorOrg([0,0])
        org2 = org1.get_mutant()
        self.assertNotEqual(org1, org2)
        org3 = arr.RealValueVectorOrg([0,0])
        org4 = org3.get_mutant()
        self.assertNotEqual((org3==org4).all(), True)

    def test_is_better_than(self):
        org1 = rvvo.RealValueVectorOrg([0,0])        
        org2 = rvvo.RealValueVectorOrg([0,1])
        self.assertTrue(org1.is_better_than(org2, sum))
        self.assertFalse(org2.is_better_than(org1, sum))
        org3 = arr.RealValueVectorOrg([0,0])        
        org4 = arr.RealValueVectorOrg([0,1])
        self.assertTrue(org3.is_better_than(org4, sum))
        self.assertFalse(org4.is_better_than(org3, sum))

class TestVectorOrgFunctionsVsArrayOrgFunctions(unittest.TestCase):
    """Testing the internal functions of the modules."""

    def setUp(self):
        rvvo.LENGTH = arr.LENGTH = 2
        rvvo.RANGE_MIN = arr.RANGE_MIN = -2
        rvvo.RANGE_MAX = arr.RANGE_MAX = 2
        rvvo.MUTATION_EFFECT_SIZE = arr.MUTATION_EFFECT_SIZE = 10

    def test_wrap_around(self):
        min_ = -10
        max_ = 10
        qa_dict = {-11:9, 5:5, 11:-9, -31:9, 31:-9}
        for question, answer in qa_dict.items():
            result = rvvo._wrap_around(question, min_, max_)
            self.assertEqual(result, answer)
        for question, answer in qa_dict.items():
            result = arr._wrap_around(question, min_, max_)
            self.assertEqual(result, answer)
        
    def test_get_mutant_genotype(self):
        genotype = [0,0]
        vector_mutated_genotype = rvvo._get_mutated_genotype(genotype, 10)
        self.assertNotEqual(genotype, vector_mutated_genotype)
        array_mutated_genotype = arr._get_mutated_genotype(arr.RealValueVectorOrg(genotype).genotype, 10)
        self.assertNotEqual((arr.RealValueVectorOrg(genotype).genotype==array_mutated_genotype).all(), True)

    def test_create_random_genotype(self):
        vector_genotype = rvvo._create_random_genotype()
        self.assertEqual(rvvo.LENGTH, len(vector_genotype))
        array_genotype = arr._create_random_genotype()
        self.assertEqual(arr.LENGTH, array_genotype.shape[0])
