from unittest import TestCase, main

from classes.solver import Perceptron


class TestPerceptronBasicProperties(TestCase):


    def setUp(self):
        def as_tuples(x):
            return [tuple(row) for row in x]
        self.processors = [
            lambda x: x,
            as_tuples,
            lambda x: set(as_tuples(x))
        ]
        pass


    def tearDown(self):
        pass


    def test_constructor(self):
        perceptron = Perceptron(1)
        self.assertIsInstance(perceptron, Perceptron)


    def test_setup_line(self):
        left = [[-1]]
        right = [[1]]
        for process in self.processors:
            perceptron = Perceptron(1)
            perceptron.setup(process(left), process(right))


    def test_setup_plane(self):
        left = [[-1, 1], [-2, 1]]
        right = [[1, 1], [2, 1]]

        for process in self.processors:
            perceptron = Perceptron(2)
            perceptron.setup(process(left), process(right))


if __name__ == '__main__':
    main()

