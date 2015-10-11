from unittest import TestCase, main

from classes.graph import Graph, Edge, Vertex


class TestGraphBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_constructor(self):
        self.assertIsInstance(Graph(set(), set()), Graph)


    def test_one_edge(self):
        v_zero = Vertex(0)
        v_one = Vertex(1)
        e = Edge(v_zero, v_one)
        self.assertIs(e.get_value(), None)
        self.assertIsInstance(Graph([v_zero, v_one], [e]), Graph)


    def test_incorrect_edge(self):
        v_zero = Vertex(0)
        v_one = Vertex(0)
        self.assertIsNot(v_zero, v_one)
        e = Edge(v_zero, v_one)
        with self.assertRaises(ValueError):
            Graph(v_zero, e)


if __name__ == '__main__':
    main()

