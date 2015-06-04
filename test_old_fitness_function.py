import unittest
import old_fitness_function as ff

class TestFitnessFunction(unittest.TestCase):
    
    def setUp(self):
        self.vals = [1.0, 2.0]
    
    def test_flat_function(self):
        self.assertEqual(ff.flat_function(self.vals), 0)

    def test_sphere_function(self):
        self.assertEqual(ff.sphere_function(self.vals), 5.0)

    def test_rosenbrock_function(self):
        self.assertEqual(ff.rosenbrock_function(self.vals), 100.0)

    def test_rana_function(self):
        self.assertEqual(ff.rana_function(self.vals), ff.rana_function(self.vals))
        self.assertEqual(len(ff.RANA_WEIGHTS), len(self.vals))

    def test_schafferF7(self):
        self.assertEqual(ff.schafferF7(self.vals), ff.schafferF7(self.vals))

    def test_deceptive(self):
        self.assertEqual(ff.deceptive(self.vals), ff.deceptive(self.vals))

class TestFitnessFunctionClass(unittest.TestCase):

    def setUp(self):
        self.ff_object = ff.Fitness_Function(ff.sphere_function, 2)
        self.vals = [1.0, 2.0]

    def test_fitness1_fitness(self):
        self.assertEqual(self.ff_object.fitness1_fitness(self.vals), ff.sphere_function(self.vals))

    
