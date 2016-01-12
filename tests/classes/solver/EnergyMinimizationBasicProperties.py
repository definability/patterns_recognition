from unittest import TestCase, main

from classes.graph import Graph, Edge, Vertex
from classes.solver import EnergyMinimization
from classes.semiring import SemiringMaxPlusElement


class TestEnergyMinimizationBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_constructor(self):
        v_zero = Vertex()
        v_one = Vertex()
        e = Edge(v_zero, v_one)
        g = EnergyMinimization([v_zero, v_one], [e])
        self.assertIsInstance(g, Graph)
        self.assertIsInstance(g, EnergyMinimization)


    def test_solve_trivial(self):
        """Solve simple problem

        1 - 1 - 1
        2 - 2 - 2
        3 - 3 - 3

        Right answer is {3, 3, 3}
        """
        v_one_a = Vertex(value=1, domain='a')
        v_one_b = Vertex(value=1, domain='b')
        v_one_c = Vertex(value=1, domain='c')
        e_one = [Edge(v_one_a, v_one_b, 0),
                 Edge(v_one_b, v_one_c, 0)]

        v_two_a = Vertex(value=2, domain='a')
        v_two_b = Vertex(value=2, domain='b')
        v_two_c = Vertex(value=2, domain='c')
        e_two = [Edge(v_two_a, v_two_b, 0),
                 Edge(v_two_b, v_two_c, 0)]

        v_three_a = Vertex(value=3, domain='a')
        v_three_b = Vertex(value=3, domain='b')
        v_three_c = Vertex(value=3, domain='c')
        e_three = [Edge(v_three_a, v_three_b, 0),
                 Edge(v_three_b, v_three_c, 0)]

        g = EnergyMinimization([
            v_one_a, v_one_b, v_one_c,
            v_two_a, v_two_b, v_two_c,
            v_three_a, v_three_b, v_three_c],
            e_one + e_two + e_three)
        self.assertItemsEqual(g.solve(), [v_three_a, v_three_b, v_three_c])


#    def test_solve_trivial_advanced(self):
#        """Solve advanced trivial problem
#
#        1 - 1 - 1
#          \   \
#        2 - 2 - 2
#          /   /
#        3 - 3 - 3
#
#        Right answer is {3, 3, 3}
#        """
#        v_one_a = Vertex(value=1, domain='a')
#        v_one_b = Vertex(value=1, domain='b')
#        v_one_c = Vertex(value=1, domain='c')
#        e_one = [Edge(v_one_a, v_one_b, 0),
#                 Edge(v_one_b, v_one_c, 0)]
#
#        v_two_a = Vertex(value=2, domain='a')
#        v_two_b = Vertex(value=2, domain='b')
#        v_two_c = Vertex(value=2, domain='c')
#        e_two = [Edge(v_two_a, v_two_b, 0),
#                 Edge(v_two_b, v_two_c, 0)]
#
#        v_three_a = Vertex(value=3, domain='a')
#        v_three_b = Vertex(value=3, domain='b')
#        v_three_c = Vertex(value=3, domain='c')
#        e_three = [Edge(v_three_a, v_three_b, 0),
#                   Edge(v_three_b, v_three_c, 0)]
#
#        g = EnergyMinimization([
#            v_one_a, v_one_b, v_one_c,
#            v_two_a, v_two_b, v_two_c,
#            v_three_a, v_three_b, v_three_c],
#            e_one + e_two + e_three + [
#                Edge(v_one_a, v_two_b, 0), Edge(v_three_a, v_two_b, 0),
#                Edge(v_one_b, v_two_c, 0), Edge(v_three_b, v_two_c, 0)
#        ])
#        self.assertItemsEqual(g.solve(), [v_three_a, v_three_b, v_three_c])


#    def test_solve_simple(self):
#        """Solve simple problem
#
#        1   1 - 1
#          X     
#        3   2 - 3
#
#        Right answer is {1, 2, 3}
#        """
#        v_one_a = Vertex(value=1, domain='a')
#        v_one_b = Vertex(value=1, domain='b')
#        v_one_c = Vertex(value=1, domain='c')
#
#        v_three_a = Vertex(value=3, domain='a')
#        v_two_b = Vertex(value=2, domain='b')
#        v_three_c = Vertex(value=3, domain='c')
#
#        g = EnergyMinimization([
#            v_one_a, v_one_b, v_one_c,
#            v_three_a, v_two_b, v_three_c], [
#            Edge(v_one_a, v_two_b, 0), Edge(v_three_a, v_one_b, 0),
#            Edge(v_one_b, v_one_c, 0), Edge(v_two_b, v_three_c, 0)])
#        self.assertItemsEqual(g.solve(), [v_one_a, v_two_b, v_three_c])


