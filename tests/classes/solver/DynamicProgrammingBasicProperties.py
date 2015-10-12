from unittest import TestCase, main

from classes.graph import Graph, Edge, Vertex
from classes.solver import DynamicProgramming
from classes.semiring import semirings#SemiringMinPlusElement, SemiringPlusMulElement
from classes.semiring import SemiringMinPlusElement, SemiringPlusMulElement


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


    def test_solve_incorrect_finish(self):
        vertex = Vertex()
        g = DynamicProgramming([], [])
        with self.assertRaises(ValueError):
            g.set_finish(vertex)

        
    def test_solve_simple(self):
        """Solve simple problem

        start --1--> finish

        Right answer is 1
        """
        start = Vertex('start')
        finish = Vertex('finish')
        for S in semirings:
            e = Edge(start, finish, S.unity())
            g = DynamicProgramming([start, finish], [e])
            g.set_start(start)
            g.set_finish(finish)
            self.assertEqual(g.solve(S), S.unity())


    def test_solve_square(self):
        """Solve problem with rhombus

        start ---1--> A
          |           |
          1           1
          |           |
          V           V
          B ---1--> finish

        Right answer is (1*1 + 1*1)
        """

        start = Vertex('start')
        finish = Vertex('finish')
        a = Vertex('a')
        b = Vertex('b')

        for S in semirings:
            start_a = Edge(start, a, S.unity())
            start_b = Edge(start, b, S.unity())

            a_finish = Edge(a, finish, S.unity())
            b_finish = Edge(b, finish, S.unity())

            g = DynamicProgramming([start, a, b, finish], [start_a, start_b,
                                                        a_finish, b_finish])
            g.set_start(start)
            g.set_finish(finish)

            self.assertEqual(g.solve(S), S.unity()+S.unity())


if __name__ == '__main__':
    main()

