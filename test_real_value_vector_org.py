import unittest
import real_value_vector_org as rvvo
from rvvo import *

class TestRealValueVectorOrg(unittest.TestCase):

    def setup(self):
        rvvo.LENGTH = 2
        rvvo.RANGE_MIN = -2
        rvvo.RANGE_MAX = 2
        def env(genotype):
            return sum(genotype)
        self.env = env
    

if __name__ == "__main__":
    unittest.main()
