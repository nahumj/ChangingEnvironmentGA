import unittest
import pd_org
import pd_tournament
from pd_tournament import pd_payout

class TestPDPayout(unittest.TestCase):
    def test_pd_payout(self):
        def alt_pd_payout(self_is_cooperator, other_is_cooperator):
            if self_is_cooperator:
                if other_is_cooperator:
                    return pd_tournament.REWARD
                return pd_tournament.SUCKER
            if other_is_cooperator:
                return pd_tournament.TEMPTATION
            return pd_tournament.PUNISHMENT
        
        for a_cooperates in [True, False]:
            for b_cooperates in [True, False]:
                payout_a, payout_b = pd_payout(a_cooperates, b_cooperates)
                expected_payout_a = alt_pd_payout(a_cooperates, b_cooperates)
                expected_payout_b = alt_pd_payout(b_cooperates, a_cooperates)
                
                self.assertEqual(expected_payout_a, payout_a)
                self.assertEqual(expected_payout_b, payout_b)
                
                
class TestRunGame(unittest.TestCase):
    def setUp(self):
        pd_org.MAX_BITS_OF_MEMORY = 4

        pd_tournament.NUMBER_OF_ROUNDS = 2
        self.organism_a = pd_org.PDOrg(pd_org.MemoryPDGenotype(1,[True, False], [False]))
        self.organism_b = pd_org.PDOrg(pd_org.MemoryPDGenotype(2,[True, False, False, True], [False, True]))
        
    
    def test_run_game(self):
        total_payout_a, total_payout_b = pd_tournament.run_game(self.organism_a, self.organism_b)
        expected_total_payout_a = 3
        expected_total_payout_b = 8
        self.assertEqual(expected_total_payout_a, total_payout_a)
        self.assertEqual(expected_total_payout_b, total_payout_b)
                

if __name__ == "__main__":
    unittest.main()