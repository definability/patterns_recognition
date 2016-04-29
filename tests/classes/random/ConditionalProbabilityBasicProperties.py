from unittest import TestCase, main

from classes.random import ConditionalProbability


class ConditionalProbabilityBasicProperties(TestCase):


    def setUp(self):
        def as_tuples(x):
            return [tuple(row) for row in x]
        self.processors = [
            lambda x: x,
            as_tuples,
            lambda x: set(as_tuples(x))
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


    def test_unknown_values(self):
        sample = [[0, 0], [0, 1]]
        for process in self.processors:
            p = ConditionalProbability()
            p.add_sample(process(sample))

            self.assertEqual(p.get_probabilities(0, [2]), {})
            self.assertEqual(p.get_probabilities(1, [1]), {})


if __name__ == '__main__':
    main()

