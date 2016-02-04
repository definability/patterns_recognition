from Edge import Edge
from Vertex import Vertex


class Graph(object):


    def __init__(self, V, E, tau=set()):

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
        self.domains_list = self.domains.keys()

        self.deleted_edges = set()
        self.deleted_vertices = set()

        if len(tau) > 0:
            self.tau = tau
            if self.is_neighborhood_corrupted():
                raise ValueError("Not all neighbours exist")
        else:
            self.tau = self.get_neighboring_domains()

        self.links = None


    def check_edge(self, e):
        if not self.V.issuperset(set(e.get_vertices())):
            raise ValueError("All vertices should be in graph's vertices' set")


    def get_domains(self):
        return self.domains_list


    def get_domain(self, domain, with_deleted=False):
        if len(self.deleted_vertices) == 0 or with_deleted == True:
            return self.domains[domain]
        return set(v for v in self.domains[domain]
                     if v not in self.deleted_vertices)


    def get_tau(self):
        return self.tau


    def get_link(self, link):
        return self.links[link]


    def is_neighborhood_corrupted(self):
        return self.get_tau() != self.get_neighboring_domains()


    def get_neighboring_domains(self):
        neighboring_domains = set()
        vertices = self.get_vertices()
        for e in self.get_edges():
            v = e.get_vertices()
            if v[0] not in vertices or v[1] not in vertices:
                continue
            neighboring_domains.add((v[0].get_domain(), v[1].get_domain()))
        return neighboring_domains


    def delete_vertex(self, vertex, mark_only=False):
        if vertex not in self.V:
            raise ValueError('Edge does not belong to current graph')
        if mark_only:
            self.deleted_vertices.add(vertex)
        if vertex in self.deleted_vertices:
            return
        self.deleted_vertices.add(vertex)
        for e in vertex.get_outputs().union(vertex.get_inputs()) \
                                     .difference(self.deleted_edges):
            self.delete_edge(e)


    def delete_edge(self, edge, mark_only=False):
        if edge not in self.E:
            raise ValueError('Edge does not belong to current graph')
        if mark_only:
            self.deleted_edges.add(edge)
        if edge in self.deleted_edges:
            return
        start, end = edge.get_vertices()
        self.deleted_edges.add(edge)
        if start not in self.deleted_vertices \
        and start.get_outputs().issubset(self.deleted_edges):
            self.delete_vertex(start)
        if end not in self.deleted_vertices \
        and end.get_inputs().issubset(self.deleted_edges):
            self.delete_vertex(end)


    def get_domained_links(self):
        domained_links = dict((v, dict()) for v in self.V)
        for e in self.E:
            start, end = e.get_vertices()

            domain = end.get_domain()
            if domain not in domained_links[start]:
                domained_links[start][domain] = set()
            domained_links[start][domain].add(e)

            domain = start.get_domain()
            if domain not in domained_links[end]:
                domained_links[end][domain] = set()
            domained_links[end][domain].add(e)

        return domained_links


    def delete_corrupted(self, domained_links=None):
        if domained_links is None:
            domained_links = self.get_domained_links()
        deleted = True
        while deleted:
            deleted = False
            for v in self.V - self.deleted_vertices:
                for d in domained_links[v]:
                    if domained_links[v][d] <= self.deleted_edges:
                        self.deleted_vertices.add(v)
                        deleted = True
                        break
            for e in self.E - self.deleted_edges:
                start, end = e.get_vertices()
                if start in self.deleted_vertices \
                or end in self.deleted_vertices:
                    self.deleted_edges.add(e)
                    deleted = True


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

        self.links = dict([(neighbour, set()) for neighbour in self.tau])
        for domain in self.domains:
            for v in self.domains[domain]:
                edges = v.get_outputs()
                for e in edges:
                    self.links[domain, e.get_vertices()[1].get_domain()].add(e)
        for link in self.links:
            self.links[link] = list(self.links[link])


    def get_edges(self):
        return self.E.difference(self.deleted_edges)


    def get_vertices(self):
        return self.V.difference(self.deleted_vertices)


    def restore(self):
        self.deleted_edges.clear()
        self.deleted_vertices.clear()

