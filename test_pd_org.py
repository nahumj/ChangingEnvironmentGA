"""
Tests for pd_org.py
"""

import unittest
import pd_org
from pd_org import MemoryPDGenotype as Geno
from pd_org import PDOrg

class TestMemoryPDGenotype(unittest.TestCase):

    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 5
        pd_org.MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = .33
        pd_org.MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = .33
        self.num_bits = 2
        self.decision_list = [True, False, False, True]
        self.initial_mem = [True, False]
        self.geno = Geno(self.num_bits, self.decision_list, self.initial_mem)
        
        
    def test_init(self):
        self.assertEqual(self.num_bits, self.geno.number_of_bits_of_memory)
        self.assertEqual(self.decision_list, self.geno.decision_list)
        self.assertEqual(self.initial_mem, self.geno.initial_memory)
        

    def test_init_bad(self):
        with self.assertRaises(AssertionError):
            Geno(2, [True]*4, [False])

        with self.assertRaises(AssertionError):
            Geno(2, [True]*3, [False]*2)
        
        with self.assertRaises(AssertionError):
            Geno(6, [True]*(2**6), [False]*6)
            
        with self.assertRaises(AssertionError):
            Geno(-1, [], [])

    def test_eq(self):
        geno2 = Geno(self.num_bits, self.decision_list, self.initial_mem)
        self.assertEqual(self.geno, geno2)
        
        geno3 =  Geno(1, [False, True], [False])
        self.assertNotEqual(self.geno, geno3)
        
        geno4 = Geno(self.num_bits, [True, True, False, True], self.initial_mem)
        self.assertNotEqual(self.geno, geno4)
        
        geno5 = Geno(self.num_bits, self.decision_list, [False, True])
        self.assertNotEqual(self.geno, geno5)
        
    def test_str(self):
        expected = "MemoryPDGenotype(2, [True, False, False, True], [True, False])"
        result = str(self.geno)
        self.assertEqual(expected, result)
        
        result_repr = repr(self.geno)
        self.assertEqual(expected, result_repr)
    
    def test_decision_list_mutant(self):
        mutant = self.geno._decision_list_mutant()
        self.assertNotEqual(mutant, self.geno)
        self.assertEqual(mutant.number_of_bits_of_memory,
            self.geno.number_of_bits_of_memory)
        self.assertNotEqual(mutant.decision_list, self.geno.decision_list)
        self.assertEqual(mutant.initial_memory, self.geno.initial_memory)
        
    def test_initial_memory_mutant(self):
        mutant = self.geno._initial_memory_mutant()
        self.assertNotEqual(mutant, self.geno)
        self.assertEqual(mutant.number_of_bits_of_memory,
            self.geno.number_of_bits_of_memory)
        self.assertEqual(mutant.decision_list, self.geno.decision_list)
        self.assertNotEqual(mutant.initial_memory, self.geno.initial_memory)
    
    def test_initial_memory_mutant_no_memory(self):
        no_memory = Geno(0, [True], [])
        mutant = no_memory._initial_memory_mutant()
        self.assertEqual(mutant, no_memory)
    
    def test_bits_of_memory_mutant(self):
        for _ in range(100):
            mutant = self.geno._get_bits_of_memory_mutant()
            if mutant.number_of_bits_of_memory == 1:
                self.assertEqual(mutant.decision_list, self.geno.decision_list[:2])
                self.assertEqual(mutant.initial_memory, self.geno.initial_memory[:1])
            elif mutant.number_of_bits_of_memory == 3:
                self.assertEqual(mutant.decision_list, self.geno.decision_list * 2)
                self.assertEqual(mutant.initial_memory[:-1], self.geno.initial_memory)
                self.assertIn(mutant.initial_memory[-1], [True, False])
            else:
                self.fail("number of bits MUST change")
    
    def test_get_mutant_of_self(self):
        for _ in range(100):
            mutant = self.geno.get_mutant_of_self()
            self.assertNotEqual(self.geno, mutant)
            
class TestCreateRandomGenotype(unittest.TestCase):
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 5
      
    def test_call(self):
        geno = pd_org._create_random_genotype()
        self.assertTrue(isinstance(geno, Geno))
    
            
class TestPDOrg(unittest.TestCase):
    
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 5
        pd_org.MUTATION_LIKELIHOOD_OF_BITS_OF_MEMORY = .33
        pd_org.MUTATION_LIKELIHOOD_OF_INITIAL_MEMORY_STATE = .33
        num_bits = 2
        decision_list = [True, False, False, True]
        initial_mem = [True, False]
        self.geno = Geno(num_bits, decision_list, initial_mem)
        self.org = PDOrg(self.geno)
        
    def test_init(self):
        """
        Tests if genotype given to PDOrg constructor
        """
        self.assertEqual(self.org.genotype, self.geno)
        self.assertSequenceEqual(self.org.memory, self.geno.initial_memory)
        
    def test_init_no_geno(self):
        """
        Test if no genotype is given to PDOrg constructor
        """
        random_org = PDOrg()
        self.assertIsInstance(random_org.genotype, Geno)
    
    def test_get_mutant(self):
        mutant_org = self.org.get_mutant()
        self.assertNotEqual(mutant_org.genotype, self.org.genotype)
        
    def test_eq(self):
        other_org = PDOrg(Geno(1, [False, True], [True]))
        same_org = PDOrg(self.geno)
        self.assertNotEqual(self.org, other_org)
        self.assertEqual(self.org, same_org)
        
    def test_str(self):
        expected = "PDOrg(MemoryPDGenotype(2, [True, False, False, True], [True, False]))"
        result = str(self.org)
        self.assertEqual(expected, result)
        repr_result = repr(self.org)
        self.assertEqual(expected, repr_result)
        
    def test_opponent_cooperated_last_round(self):
        self.org.opponent_cooperated_last_round(True)
        self.assertSequenceEqual([False, True], self.org.memory)
        
        self.org.opponent_cooperated_last_round(False)
        self.assertSequenceEqual([True, False], self.org.memory)
        
    def test_will_cooperate(self):
        did_cooperate = self.org.will_cooperate()
        self.assertEqual(False, did_cooperate)
        
        self.org.opponent_cooperated_last_round(True)
        did_cooperate = self.org.will_cooperate()
        self.assertEqual(False, did_cooperate)
        
        self.org.opponent_cooperated_last_round(True)
        did_cooperate = self.org.will_cooperate()
        self.assertEqual(True, did_cooperate)
    
if __name__ == "__main__":
    unittest.main()
