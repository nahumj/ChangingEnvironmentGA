import unittest
import main
import string_org as so
import real_value_vector_org as rvvo

class TestMain(unittest.TestCase):
    """Testing main.py"""

    def setUp(self):
        #main.FITNESS_FUNCTION_TYPE = 
        main.NUMBER_OF_ORGANISMS = 10
        main.MUTATION_RATE = .1
        main.NUMBER_OF_GENERATIONS = 10
        #main.OUTPUT_FILE = test_folder
        main.ORG_TYPE = "string"
        main.TOURNAMENT_SIZE = 2
        main.VERBOSE = False
        main.ALTERNATE_ENVIRONMENT_CORR = 0.5
        #main.START_TIME = 
        so.TARGET_STRING = "CC"
        so.LETTERS = "ABC"

    def test_create_initial_population(self):
        pop = main.create_initial_population()
        self.assertEqual(len(pop), int(main.NUMBER_OF_ORGANISMS))

    def test_get_mutated_population_max_mutation(self):
        pop = main.create_initial_population()
        main.MUTATION_RATE = 1
        new_pop = main.get_mutated_population(pop)
        self.assertNotEqual(pop, new_pop)
        self.assertEqual(len(pop), len(new_pop))

    def test_get_mutated_population_no_mutation(self):
        pop = main.create_initial_population()
        main.MUTATION_RATE = 0
        new_pop = main.get_mutated_population(pop)
        self.assertEqual(pop, new_pop)
        self.assertEqual(len(pop), len(new_pop))

    def test_get_selected_population(self):
        environment = so.default_environment
        pop = main.create_initial_population()
        new_pop = main.get_selected_population(pop, environment)
        for org in new_pop:
            self.assertIn(org, pop)
        self.assertEqual(len(pop), len(new_pop))

    def test_get_best_organism(self):
        environment = so.default_environment
        pop = main.create_initial_population()
        best_org = main.get_best_organism(pop, environment)
        self.assertIs(type(best_org), so.StringOrg)
        for org in pop:
            self.assertFalse(org.is_better_than(best_org, environment))

    def test_get_next_generation_max_mutation(self):
        environment = so.default_environment
        pop = main.create_initial_population()
        main.MUTATION_RATE = 1
        new_pop = main.get_next_generation(pop, environment)
        self.assertNotEqual(pop, new_pop)
        self.assertEqual(len(pop), len(new_pop))

    def test_get_next_generation_no_mutation(self):
        environment = so.default_environment
        pop = main.create_initial_population()
        main.MUTATION_RATE = 0
        new_pop = main.get_next_generation(pop, environment)
        for org in new_pop:
            self.assertIn(org, pop)
        self.assertEqual(len(pop), len(new_pop))
