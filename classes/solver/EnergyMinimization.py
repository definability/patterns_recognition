import logging

from classes.graph import Graph, Edge, Vertex


class EnergyMinimization(Graph):


    def __init__(self, V, E, tau=set()):
        self.max_edges = dict()
        self.max_vertices = dict()
        self.profile = None
        super(EnergyMinimization, self).__init__(V, E, tau)


    def __gamma(self, k=None):
        n = .5
        if k is None:
            i = 0
            while True:
                yield n/(i+1)
                i += 1
        else:
            for i in xrange(k):
                yield n/(i+1)


    def max_vertex(self, vertices):
        return max(vertices, key=lambda v: v.get_value())


    def max_edge(self, edges):
        return max(edges, key=lambda e: e.get_value())


    def get_max_vertex(self, domain, cached=True):
        if not cached:
            self.max_vertices[domain] = self.max_vertex(self.get_domain(domain))
        return self.max_vertices[domain]


    def get_max_edge(self, link, cached=True):
        if not cached:
            self.max_edges[link] = self.max_edge(self.get_link(link))
        return self.max_edges[link]


    def get_energy(self, cached=True):
        return (sum([self.get_max_vertex(domain, cached).get_value()
                    for domain in self.get_domains()]) +
               sum([self.get_max_edge(link, cached).get_value()
                    for link in self.get_tau()]))


    def __iteration(self, g, gamma):
        for link in g.get_tau():
            max_e = self.get_max_edge(link)
            max_e.set_value(max_e.get_value() - 2 * gamma)
            x, y = max_e.get_vertices()
            x.set_value(x.get_value() + gamma)
            y.set_value(y.get_value() + gamma)
        for domain in g.get_domains():
            max_v = g.get_max_vertex(domain)
            edges = max_v.get_inputs().union(max_v.get_outputs())
            max_v.set_value(max_v.get_value() - len(edges) * gamma)
            for e in edges:
                e.set_value(e.get_value() + gamma)


    def remove_small(self, treshold, domained_links=None):
        remove_after = True
        for domain in self.get_domains():
            vertices = self.get_domain(domain, True)
            if len(vertices) == 0:
                continue
            max_v = self.get_max_vertex(domain, False)
            max_value = max_v.get_value()
            for v in vertices:
                if max_value - v.get_value() > treshold:
                    self.delete_vertex(v, remove_after)
        for link in self.get_tau():
            edges = self.get_link(link)
            max_e = self.get_max_edge(link, False)
            max_value = max_e.get_value()
            for e in edges:
                if max_value - e.get_value() > treshold:
                    self.delete_edge(e, remove_after)
        if remove_after:
            if self.profile is not None:
                self.profile.enable()
            self.delete_corrupted(domained_links)
            if self.profile is not None:
                self.profile.disable()


    def get_mapped_copy(self):
        V_map = dict()
        V_map_inv = dict()
        E_map = dict()
        for v in self.V:
            v_copy = Vertex(v.get_name(), v.get_value(),
                            v.get_domain())
            V_map[v_copy] = v
            V_map_inv[v] = v_copy
        for e in self.E:
            x, y = e.get_vertices()
            E_map[Edge(V_map_inv[x], V_map_inv[y], e.get_value())] = e
        g = EnergyMinimization(V_map.keys(), E_map.keys(), self.get_tau())
        return g, V_map, V_map_inv


    def solve(self, make_copy=True, profile=None):
        self.profile = profile
        g, V_map, E_map = None, None, None
        if make_copy:
            g, V_map, E_map = self.get_mapped_copy()
        else:
            g = self
        g.prepare()
        domained_links = g.get_domained_links()
        step = 0
        for gamma in self.__gamma():
            g.remove_small(0.5, domained_links)
            logging.info('step %06d, gamma %f, energy %f'%(step, gamma, g.get_energy()))
            if not g.is_neighborhood_corrupted():
                break
            g.restore()
            self.__iteration(g, gamma)
            step += 1
        vertices_to_visit = [list(g.get_vertices())[0]]
        vertices = list()
        edges = list()
        domains = set([vertices_to_visit[0].get_domain()])
        edges_available = g.get_edges()
        while len(vertices_to_visit) > 0:
            vertex = vertices_to_visit.pop()
            vertices.append(vertex)
            for e in vertex.get_outputs().intersection(edges_available):
                end = e.get_vertices()[1]
                if end.get_domain() in domains:
                    continue
                edges.append(e)
                domains.add(end.get_domain())
                vertices_to_visit.append(end)
            for e in vertex.get_inputs().intersection(edges_available):
                start = e.get_vertices()[0]
                if start.get_domain() in domains:
                    continue
                edges.append(e)
                domains.add(start.get_domain())
                vertices_to_visit.append(start)
        if make_copy:
            #return (set(V_map[v] for v in vertices), set(E_map[e] for e in edges))
            return set(V_map[v] for v in vertices)
        else:
            return vertices

