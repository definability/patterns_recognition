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

        if not isinstance(tau, set):
            tau = set(tau)

        self.V = V
        self.E = E

        for e in self.E:
            self.check_edge(e)

        self.domains = dict()
        for v in self.V:
            if v.domain not in self.domains:
                self.domains[v.get_domain()] = set([v])
            else:
                self.domains[v.get_domain()].add(v)

        self.tau = tau if len(tau) > 0 else self.get_neighboring_domains()
        if self.is_neighborhood_corrupted():
            raise ValueError("Not all neighbours exist")


    def check_edge(self, e):
        if not self.V.issuperset(set(e.get_vertices())):
            raise ValueError("All vertices should be in graph's vertices' set")


    def get_domains(self):
        return self.domains.keys()


    def get_domain(self, domain):
        return self.domains[domain]


    def get_tau(self):
        return self.tau


    def is_neighborhood_corrupted(self, V=None, E=None):
        V = self.V if V is None else V
        E = self.E if E is None else E
        return self.get_tau() != self.get_neighboring_domains(V, E)


    def get_neighboring_domains(self, V=None, E=None):
        V = self.V if V is None else V
        E = self.E if E is None else E
        neighboring_domains = set()
        for e in E:
            v = e.get_vertices()
            if v[0] not in self.V or v[1] not in self.V:
                continue
            neighboring_domains.add((v[0].get_domain(), v[1].get_domain()))
        return neighboring_domains


    def prepare(self, semiring=None):

        for vertex in self.V:
            vertex.clear_inputs()
            vertex.clear_outputs()
            if semiring is not None and vertex.get_value() is not None \
                and not isinstance(vertex.get_value(), semiring):
                vertex.set_value(semiring(vertex.get_value()))

        for edge in self.E:
            vertices = edge.get_vertices()
            vertices[0].add_output(edge)
            vertices[1].add_input(edge)
            if semiring is not None \
                and not isinstance(edge.get_value(), semiring):
                edge.set_value(semiring(edge.get_value()))

