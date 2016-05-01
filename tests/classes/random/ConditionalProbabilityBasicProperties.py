from unittest import TestCase, main

from classes.random import ConditionalProbability


class ConditionalProbabilityBasicProperties(TestCase):


    def setUp(self):
        def as_tuples(x):
            return [tuple(row) for row in x]
        self.processors = [
            lambda x: x,
            as_tuples,
        ]


    def tearDown(self):
        pass


    def test_constructor(self):
        p = ConditionalProbability()
        self.assertIsInstance(p, ConditionalProbability)


    def test_add_sample(self):
        sample = [[0, 1], [1, 0]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))


    def test_add_samples(self):
        sampleA = [[0, 1], [1, 0]]
        sampleB = [[2, 3], [3, 2]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sampleA))
            p.add_sample(process(sampleB))


    def test_get_probabilities(self):
        sample = [[0, 0], [0, 1]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))

            self.assertAlmostEqual(p.get_probabilities(0, [0])[0], 1.)
            self.assertAlmostEqual(p.get_probabilities(0, [1])[0], 1.)

            self.assertAlmostEqual(p.get_probabilities(1, [0])[0], .5)
            self.assertAlmostEqual(p.get_probabilities(1, [0])[1], .5)


    def test_get_probabilities_one_dimensional(self):
        sample = [[0], [1], [1], [1]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))
            self.assertAlmostEqual(p.get_probabilities(0)[0], .25)
            self.assertAlmostEqual(p.get_probabilities(0)[1], .75)


    def test_get_probabilities_excluding(self):
        sample = [[0, 0], [0, 1]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))

            self.assertAlmostEqual(p.get_probabilities(0, exclude=[1])[0], 1.)

            self.assertAlmostEqual(p.get_probabilities(1, exclude=[1])[0], .5)
            self.assertAlmostEqual(p.get_probabilities(1, exclude=[1])[1], .5)


    def test_get_probabilities_middle(self):
        sample = [[0, 0, 0], [1, 0, 1], [1, 1, 1], [1, 0, 1]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))

            self.assertAlmostEqual(p.get_probabilities(1, [0, 0])[0], 1.)

            self.assertAlmostEqual(p.get_probabilities(1, [1, 1])[0], 2./3)
            self.assertAlmostEqual(p.get_probabilities(1, [1, 1])[1], 1./3)


    def test_unknown_values(self):
        sample = [[0, 0], [0, 1]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))

            self.assertEqual(p.get_probabilities(0, [2]), {})
            self.assertEqual(p.get_probabilities(1, [1]), {})


    def test_get_mode(self):
        sample = [[0, 0], [0, 1]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))

            self.assertEqual(p.get_mode(0), 0)
            self.assertIn(p.get_mode(1), [0, 1])


if __name__ == '__main__':
    main()

