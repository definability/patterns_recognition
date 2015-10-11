from unittest import TestCase, main

from classes.graph import Graph


class TestGraphBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_constructor(self):
        self.assertIsInstance(Graph(set(), set()), Graph)


if __name__ == '__main__':
    main()

