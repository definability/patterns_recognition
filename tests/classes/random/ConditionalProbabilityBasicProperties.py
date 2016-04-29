from unittest import TestCase, main

from classes.random import ConditionalProbability


class ConditionalProbabilityBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_constructor(self):
        p = ConditionalProbability()
        self.assertIsInstance(p, ConditionalProbability)


if __name__ == '__main__':
    main()

