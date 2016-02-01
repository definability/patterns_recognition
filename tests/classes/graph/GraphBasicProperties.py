from unittest import TestCase, main
from copy import deepcopy
from random import randint

from classes.graph import Graph, Edge, Vertex
from classes.semiring import SemiringMinPlusElement


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


    def test_calculated_neighborhood(self):
        v_a = Vertex(domain='a')
        v_b = Vertex(domain='b')
        v_c = Vertex(domain='c')
        e = Edge(v_a, v_b)
        g = Graph([v_a, v_b, v_c], e)
        self.assertItemsEqual(g.get_neighboring_domains(), [('a', 'b')])


    def test_preset_neighborhood(self):
        v_a = Vertex(domain='a')
        v_b = Vertex(domain='b')
        v_c = Vertex(domain='c')
        e = Edge(v_a, v_b)
        g = Graph([v_a, v_b, v_c], e, [('a', 'b')])
        self.assertItemsEqual(g.get_neighboring_domains(), [('a', 'b')])


    def test_neighborhood_corrupted(self):
        v_a = Vertex(domain='a')
        v_b = Vertex(domain='b')
        v_c = Vertex(domain='c')
        e = Edge(v_a, v_b)
        with self.assertRaises(ValueError):
            Graph([v_a, v_b, v_c], e, [('a', 'b'), ('a', 'c')])


    def test_get_links(self):
        """
        a - b - c
        -----
        A - A - A
              /
        B - B
          \
            C
        """
        v_aA = Vertex(domain='a')
        v_aB = Vertex(domain='a')
        v_bA = Vertex(domain='b')
        v_bB = Vertex(domain='b')
        v_bC = Vertex(domain='b')
        v_cA = Vertex(domain='c')

        e_aA_bA = Edge(v_aA, v_bA)
        e_aB_bB = Edge(v_aB, v_bB)
        e_aB_bC = Edge(v_aB, v_bC)
        e_bA_cA = Edge(v_bA, v_cA)
        e_bB_cA = Edge(v_bB, v_cA)

        g = Graph([v_aA, v_aB, v_bA, v_bB, v_bC, v_cA],
                  [e_aA_bA, e_aB_bB, e_bA_cA, e_bB_cA, e_aB_bC])
        g.prepare()
        self.assertItemsEqual(g.get_links(('b', 'c')),
                              [e_bA_cA, e_bB_cA])
        self.assertItemsEqual(g.get_links(('a', 'b')),
                              [e_aA_bA, e_aB_bB, e_aB_bC])
        self.assertDictEqual(g.get_links(), {
            ('a', 'b'): set([e_aA_bA, e_aB_bB, e_aB_bC]),
            ('b', 'c'): set([e_bA_cA, e_bB_cA])
        })


    def test_delete_vertex(self):
        """
        a - b - c
        -----
        A - A - A
              /
        B - B
          \
            C
        """
        v_aA = Vertex(domain='a')
        v_aB = Vertex(domain='a')
        v_bA = Vertex(domain='b')
        v_bB = Vertex(domain='b')
        v_bC = Vertex(domain='b')
        v_cA = Vertex(domain='c')

        e_aA_bA = Edge(v_aA, v_bA)
        e_aB_bB = Edge(v_aB, v_bB)
        e_aB_bC = Edge(v_aB, v_bC)
        e_bA_cA = Edge(v_bA, v_cA)
        e_bB_cA = Edge(v_bB, v_cA)

        g = Graph([v_aA, v_aB, v_bA, v_bB, v_bC, v_cA],
                  [e_aA_bA, e_aB_bB, e_bA_cA, e_bB_cA, e_aB_bC])
        g.prepare()

        self.assertItemsEqual(g.get_edges(), [e_aA_bA, e_aB_bB, e_aB_bC,
                                              e_bA_cA, e_bB_cA])
        self.assertItemsEqual(g.get_vertices(), [v_aA, v_aB, v_bA,
                                                 v_bB, v_bC, v_cA])
        self.assertFalse(g.is_neighborhood_corrupted())

        """
        a - b - c
        -----
        X   x   A
              /
        B - B
          \
            C
        """
        g.delete_vertex(v_aA)
        self.assertItemsEqual(g.get_edges(), [e_aB_bB, e_aB_bC, e_bB_cA])
        self.assertItemsEqual(g.get_vertices(), [v_aB, v_bB, v_bC, v_cA])
        self.assertFalse(g.is_neighborhood_corrupted())
        self.assertItemsEqual(g.get_domain('b'), [v_bB, v_bC])

        """
        a - b - c
        -----
                x
               
        B   X
          \
            C
        """
        g.delete_vertex(v_bB)
        self.assertItemsEqual(g.get_edges(), [e_aB_bC])
        self.assertItemsEqual(g.get_vertices(), [v_aB, v_bC])
        self.assertTrue(g.is_neighborhood_corrupted())
        self.assertItemsEqual(g.get_domain('a'), [v_aB])
        self.assertItemsEqual(g.get_domain('b'), [v_bC])

        """
        a - b - c
        -----
        x 
          
            X
        """
        g.delete_vertex(v_bC)
        self.assertEqual(g.get_edges(), set())
        self.assertEqual(g.get_vertices(), set())
        self.assertTrue(g.is_neighborhood_corrupted())

        g.restore()
        self.assertItemsEqual(g.get_edges(), [e_aA_bA, e_aB_bB, e_aB_bC,
                                              e_bA_cA, e_bB_cA])
        self.assertItemsEqual(g.get_vertices(), [v_aA, v_aB, v_bA,
                                                 v_bB, v_bC, v_cA])
        self.assertFalse(g.is_neighborhood_corrupted())


    def test_delete_edge(self):
        """
        a - b
        -----
        B
          \
            C
        """
        v_aB = Vertex(domain='a')
        v_bC = Vertex(domain='b')

        e_aB_bC = Edge(v_aB, v_bC)

        g = Graph([v_aB, v_bC],
                  [e_aB_bC])
        g.prepare()
        g.delete_edge(e_aB_bC)
        self.assertItemsEqual(g.get_edges(), [])
        self.assertItemsEqual(g.get_vertices(), [])
        self.assertTrue(g.is_neighborhood_corrupted())
        """
        a - b
        -----
        x
          
            X
        """


    def test_prepare(self):
        start = Vertex('start')
        finish = Vertex('finish')

        a = Vertex('a')
        b = Vertex('b')
        c = Vertex('c')

        start_a = Edge(start, a, SemiringMinPlusElement(5))
        a_b = Edge(a, b, SemiringMinPlusElement(1))
        a_c = Edge(a, c, SemiringMinPlusElement(5))
        b_c = Edge(b, c, SemiringMinPlusElement(3))
        c_finish = Edge(c, finish, SemiringMinPlusElement(9))

        g = Graph([start, finish, a, b, c],
                  [start_a, a_b, b_c, a_c, c_finish])

        g.prepare(SemiringMinPlusElement)
        self.assertItemsEqual(a.get_outputs(), [a_b, a_c])
        self.assertItemsEqual(b.get_inputs(), [a_b])
        self.assertItemsEqual(b.get_outputs(), [b_c])
        self.assertItemsEqual(c.get_inputs(), [b_c, a_c])


    def test_deep_copy(self):
        v_a = Vertex()
        v_b = Vertex()
        e = Edge(v_a, v_b)
        g = Graph([v_a, v_b], [e])
        g_copy = deepcopy(g)
        self.assertIsNot(g, g_copy)
        e = g.get_edges().pop()
        e_copy = g_copy.E.pop()
        self.assertIsNot(e, e_copy)
        self.assertEqual(e.get_value(), e_copy.get_value())
        self.assertIsNot(e.get_vertices(), e_copy.get_vertices())
        self.assertEqual([v.get_value() for v in e.get_vertices()],
                         [v.get_value() for v in e_copy.get_vertices()])
        [v.set_value(1) for v in e.get_vertices()]
        [v.set_value(2) for v in e_copy.get_vertices()]
        self.assertNotEqual([v.get_value() for v in e.get_vertices()],
                         [v.get_value() for v in e_copy.get_vertices()])
        e.set_value(1)
        e_copy.set_value(2)
        self.assertEqual(e.get_value(), 1)
        self.assertEqual(e_copy.get_value(), 2)
        self.assertEqual(len(g.get_vertices().intersection(g_copy.V)), 0)


if __name__ == '__main__':
    main()

