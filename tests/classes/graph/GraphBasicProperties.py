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


    def test_get_domains(self):
        v_aA = Vertex('A', None, 'a')
        v_aB = Vertex('B', None, 'a')
        v_bA = Vertex('A', None, 'b')
        v_bB = Vertex('B', None, 'b')
        v_bC = Vertex('C', None, 'b')
        g = Graph([v_aA, v_aB, v_bA, v_bB, v_bC], Edge(v_aA, v_bB))
        self.assertEqual(g.get_domains(), ['a', 'b'])


    def test_get_domain(self):
        v_aA = Vertex('A', None, 'a')
        v_aB = Vertex('B', None, 'a')
        v_bA = Vertex('A', None, 'b')
        v_bB = Vertex('B', None, 'b')
        v_bC = Vertex('C', None, 'b')
        g = Graph([v_aA, v_aB, v_bA, v_bB, v_bC], Edge(v_aA, v_bB))
        self.assertItemsEqual(g.get_domain('a'), set([v_aA, v_aB]))
        self.assertItemsEqual(g.get_domain('b'), set([v_bA, v_bB, v_bC]))


    def test_get_domain_tuple(self):
        v_aA = Vertex('A', None, (0,1))
        v_aB = Vertex('B', None, (0,1))
        v_bA = Vertex('A', None, (0,2))
        v_cA = Vertex('A', None, (1,1))
        v_cB = Vertex('B', None, (1,1))
        g = Graph([v_aA, v_aB, v_bA, v_cA, v_cB], Edge(v_aA, v_bA))
        self.assertItemsEqual(g.get_domain((0,1)), set([v_aA, v_aB]))
        self.assertItemsEqual(g.get_domain((0,2)), set([v_bA]))
        self.assertItemsEqual(g.get_domain((1,1)), set([v_cA, v_cB]))


if __name__ == '__main__':
    main()

