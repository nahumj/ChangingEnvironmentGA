import unittest
import old_fitness_function as ff
import fitness_function as cy
import numpy as np

class TestFitnessFunction(unittest.TestCase):
    
    def setUp(self):
        self.vals = [1.0, 2.0]
        self.ary = np.asarray(self.vals, dtype=np.float64)
    
    def test_flat_function(self):
        self.assertEqual(ff.flat_function(self.vals), cy.flat_function(self.ary))

    def test_sphere_function(self):
        self.assertEqual(ff.sphere_function(self.vals), cy.sphere_function(self.ary))

    def test_rosenbrock_function(self):
        self.assertEqual(ff.rosenbrock_function(self.vals), cy.rosenbrock_function(self.ary))

    def test_rana_function(self):
        ff.rana_function(self.vals)
        self.assertIsNotNone(ff.RANA_WEIGHTS)
        cy.rana_function(self.ary)
        self.assertIsNotNone(cy.RANA_WEIGHTS)
        self.assertEqual(len(ff.RANA_WEIGHTS), cy.RANA_WEIGHTS.shape[0])
        cy.RANA_WEIGHTS = np.asarray(ff.RANA_WEIGHTS, dtype=np.float64)
        self.assertAlmostEqual(ff.rana_function(self.vals), cy.rana_function(self.ary), places=5)

    def test_schafferF7(self):
        self.assertAlmostEqual(ff.schafferF7(self.vals), cy.schafferF7(self.ary), places=5)

    def test_deceptive(self):
        self.assertAlmostEqual(ff.deceptive(self.vals), cy.deceptive(self.ary), places=5)

class TestFitnessFunctionClass(unittest.TestCase):

    def setUp(self):
        self.ff_object = ff.Fitness_Function(ff.sphere_function, 2)
        self.cy_object = cy.Fitness_Function(cy.sphere_function, 2)
        self.vals = [1.0, 2.0]
        self.ary = np.asarray(self.vals, dtype=np.float64)

    def test_fitness1_fitness(self):
        self.assertEqual(self.ff_object.fitness1_fitness(self.vals), ff.sphere_function(self.vals))
        self.assertEqual(self.cy_object.fitness1_fitness(self.ary), cy.sphere_function(self.ary))
        self.assertEqual(self.ff_object.fitness1_fitness(self.vals), self.cy_object.fitness1_fitness(self.ary))
