from unittest import TestCase, main

from classes.graph import Graph, Edge, Vertex
from classes.solver import DynamicProgramming
from classes.semiring import semirings#SemiringMinPlusElement, SemiringPlusMulElement


class TestGraphBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_constructor(self):
        v_zero = Vertex()
        v_one = Vertex()
        e = Edge(v_zero, v_one)
        g = DynamicProgramming([v_zero, v_one], [e])
        self.assertIsInstance(g, Graph)
        self.assertIsInstance(g, DynamicProgramming)


    def test_solve_incorrect_start(self):
        vertex = Vertex()
        g = DynamicProgramming([], [])
        with self.assertRaises(ValueError):
            g.set_start(vertex)


    def test_solve_incorrect_end(self):
        vertex = Vertex()
        g = DynamicProgramming([], [])
        with self.assertRaises(ValueError):
            g.set_end(vertex)
        

    def test_solve_simple(self):
        v_zero = Vertex()
        v_one = Vertex()
        for S in semirings:
            e = Edge(v_zero, v_one, S.unity())
            g = DynamicProgramming([v_zero, v_one], [e])
            g.set_start(v_zero)
            g.set_end(v_one)
            self.assertEqual(g.solve(S), S.zero())


    def test_solve_rhombus(self):

        start = Vertex()
        end = Vertex()
        a = Vertex()
        b = Vertex()

        for S in semirings:
            start_a = Edge(start, a, S.unity())
            start_b = Edge(start, b, S.unity())

            a_end = Edge(a, end, S.unity())
            b_end = Edge(b, end, S.unity())

            g = DynamicProgramming([start, a, b, end], [start_a, start_b, a_end, b_end])
            g.set_start(start)
            g.set_end(end)

            self.assertEqual(g.solve(S), S.zero())


if __name__ == '__main__':
    main()

