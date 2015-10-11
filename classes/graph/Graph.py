from Edge import Edge
from Vertex import Vertex


class Graph(object):


    def __init__(self, V, E):

        if isinstance(V, Vertex):
            V = set([V])
        elif not isinstance(V, set):
            V = set(V)

        if isinstance(E, Edge):
            E = set([E])
        elif not isinstance(E, set):
            E = set(E)

        self.V = V
        self.E = E

        for e in E:
            self.check_edge(e)


    def check_edge(self, e):
        if not self.V.issuperset(set(e.get_vertices())):
            raise ValueError("All vertices should be in graph's vertices' set")

