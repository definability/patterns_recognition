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

