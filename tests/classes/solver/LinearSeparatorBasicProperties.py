from unittest import TestCase, main

from classes.solver import LinearSeparator


class TestLinearSeparatorBasicProperties(TestCase):


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
        separator = LinearSeparator(1, ['left', 'right'])
        self.assertIsInstance(separator, LinearSeparator)


    def test_setup_line(self):
        left = [[-1]]
        right = [[1]]
        for process in self.processors:
            separator = LinearSeparator(1, ['left', 'right'])
            self.assertTrue(separator.setup({'left': process(left), 'right': process(right)}))


    def test_setup_one_by_one(self):
        left = [[-1]]
        right = [[1]]
        for process in self.processors:
            separator = LinearSeparator(1, ['left', 'right'])
            self.assertIsNone(separator.setup())
            self.assertTrue(separator.setup({'left': process(left)}))
            self.assertTrue(separator.setup({'right': process(right)}))


    def test_setup_plane(self):
        left = [[-1, 1], [-2, 1]]
        right = [[1, 1], [2, 1]]

        for process in self.processors:
            separator = LinearSeparator(2, ['left', 'right'])
            self.assertTrue(separator.setup({'left': process(left), 'right': process(right)}))


    def test_classify_line_zero(self):
        left = [[-1]]
        right = [[1]]

        left_test = [[-5], [-10]]
        right_test = [[5], [10]]
        for process in self.processors:
            separator = LinearSeparator(1, ['left', 'right'])
            self.assertTrue(separator.setup({'left': process(left), 'right': process(right)}))
            for l in process(left_test):
                self.assertEqual(separator.classify_vertex(l), 'left')
            for r in process(right_test):
                self.assertEqual(separator.classify_vertex(r), 'right')


    def test_classify_line_offset(self):
        left = [[-3, 1], [-2, 1]]
        right = [[-1, 1], [10, 1]]

        left_test = [[-3, 1], [-20, 1]]
        right_test = [[-1, 1], [0, 1]]
        for process in self.processors:
            separator = LinearSeparator(2, ['left', 'right'])
            self.assertTrue(separator.setup({'left': process(left), 'right': process(right)}))
            for l in process(left + left_test):
                self.assertEqual(separator.classify_vertex(l), 'left')
            for r in process(right + right_test):
                self.assertEqual(separator.classify_vertex(r), 'right')


    def test_classify_line_zero_one_by_one(self):
        left = [[-1]]
        right = [[1]]

        left_test = [[-5], [-10]]
        right_test = [[5], [10]]
        for process in self.processors:
            separator = LinearSeparator(1, ['left', 'right'])
            self.assertIsNone(separator.setup())
            self.assertTrue(separator.setup({'left': process(left)}))
            self.assertTrue(separator.setup({'right': process(right)}))
            for l in process(left_test):
                self.assertEqual(separator.classify_vertex(l), 'left')
            for r in process(right_test):
                self.assertEqual(separator.classify_vertex(r), 'right')


    def test_wrong_setup_without_offset(self):
        left = [[-2]]
        right = [[-1]]

        for process in self.processors:
            separator = LinearSeparator(1, ['left', 'right'], 10)
            self.assertFalse(separator.setup({'left': process(left), 'right': process(right)}))


    def test_unclassifiable_setup(self):
        left = [[-1], [1]]
        right = [[0]]

        for process in self.processors:
            separator = LinearSeparator(1, ['left', 'right'], 10)
            self.assertFalse(separator.setup({'left': process(left), 'right': process(right)}))


if __name__ == '__main__':
    main()

