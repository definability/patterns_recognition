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

        for e in self.E:
            self.check_edge(e)

        self.domains = dict()
        for v in self.V:
            if v.domain not in self.domains:
                self.domains[v.domain] = [v]
            else:
                self.domains[v.domain].append(v)


    def check_edge(self, e):
        if not self.V.issuperset(set(e.get_vertices())):
            raise ValueError("All vertices should be in graph's vertices' set")


    def get_domains(self):
        return self.domains.keys()


    def get_domain(self, domain):
        return self.domains[domain]

