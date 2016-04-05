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
            self.assertTrue(perceptron.setup(process(left), process(right)))


    def test_setup_plane(self):
        left = [[-1, 1], [-2, 1]]
        right = [[1, 1], [2, 1]]

        for process in self.processors:
            perceptron = Perceptron(2)
            self.assertTrue(perceptron.setup(process(left), process(right)))


    def test_classify_line_zero(self):
        left = [[-1]]
        right = [[1]]

        left_test = [[-5], [-10]]
        right_test = [[5], [10]]
        for process in self.processors:
            perceptron = Perceptron(1)
            self.assertTrue(perceptron.setup(process(left), process(right)))
            for l in process(left_test):
                self.assertEqual(perceptron.classify_vertex(l), -1)
            for r in process(right_test):
                self.assertEqual(perceptron.classify_vertex(r), 1)


    def test_classify_line_offset(self):
        left = [[-3, 1], [-2, 1]]
        right = [[-1, 1], [10, 1]]

        left_test = [[-3, 1], [-20, 1]]
        right_test = [[-1, 1], [0, 1]]
        for process in self.processors:
            perceptron = Perceptron(2)
            self.assertTrue(perceptron.setup(process(left), process(right)))
            for l in process(left + left_test):
                self.assertEqual(perceptron.classify_vertex(l), -1)
            for r in process(right + right_test):
                self.assertEqual(perceptron.classify_vertex(r), 1)


if __name__ == '__main__':
    main()

