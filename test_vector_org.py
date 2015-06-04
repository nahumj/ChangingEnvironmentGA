import unittest
import real_value_vector_org as org
from numpy import sum

class TestVectorOrg(unittest.TestCase):
    """Testing real_value_vector_org.py"""

    def setUp(self):
        self.org = org.RealValueVectorOrg([0,1])
        self.env = sum

    def test_init(self):
        self.assertIsNone(self.org._fitness_cache)

    def test_get_fitness(self):
        fit_val = self.org.fitness(self.env)
        self.assertEqual(fit_val, self.org._fitness_cache)
        self.assertEqual(fit_val, 1)

    def test_reset_cache(self):
        self.org.fitness(self.env)
        self.org.reset_fitness_cache()
        self.assertIsNone(self.org._fitness_cache)
