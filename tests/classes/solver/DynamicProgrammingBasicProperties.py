from unittest import TestCase, main

from classes.graph import Graph, Edge, Vertex
from classes.solver import DynamicProgramming


class TestGraphBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_constructor(self):
        v_zero = Vertex(0)
        v_one = Vertex(1)
        e = Edge(v_zero, v_one)
        self.assertIs(e.get_value(), None)
        g = DynamicProgramming([v_zero, v_one], [e])
        self.assertIsInstance(g, Graph)
        self.assertIsInstance(g, DynamicProgramming)


if __name__ == '__main__':
    main()

