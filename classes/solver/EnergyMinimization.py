from copy import deepcopy

from classes.graph import Graph, Edge, Vertex


class EnergyMinimization(Graph):


    def __init__(self, V, E, tau=set()):
        super(EnergyMinimization, self).__init__(V, E, tau)


    def __gamma(self, k=None):
        n = 1.
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


    def __iteration(self, g, gamma):
        for domain in g.get_domains():
            edges = sum([list(v.get_outputs()) for v in g.get_domain(domain)], [])
            if len(edges) == 0:
                continue
            max_e = g.max_edge(edges)
            max_e.set_value(max_e.get_value() - 2 * gamma)
            x, y = max_e.get_vertices()
            x.set_value(x.get_value() + gamma)
            y.set_value(y.get_value() + gamma)
        for d in g.get_domains():
            max_v = g.max_vertex(g.get_domain(domain))
            edges = max_v.get_inputs().union(max_v.get_outputs())
            max_v.set_value(max_v.get_value() - len(edges) * gamma)
            for e in edges:
                e.set_value(e.get_value() + gamma)


    def remove_small(self, treshold):
        for domain in self.get_domains():
            vertices = self.get_domain(domain, True)
            if len(vertices) == 0:
                continue
            max_v = self.max_vertex(vertices)
            for v in vertices:
                if max_v.get_value() - v.get_value() > treshold:
                    self.delete_vertex(v)
        for domain in self.get_domains():
            edges = sum([list(v.get_outputs()) for v in self.get_domain(domain, True)], [])
            if len(edges) == 0:
                continue
            max_e = self.max_edge(edges)
            for e in edges:
                if max_e.get_value() - e.get_value() > treshold:
                    self.delete_edge(e)


    def solve(self):
        V_map = dict()
        V_map_inv = dict()
        E_map = dict()
        for v in self.V:
            v_copy = Vertex(deepcopy(v.get_name()), deepcopy(v.get_value()),
                            v.get_domain())
            V_map[v_copy] = v
            V_map_inv[v] = v_copy
        for e in self.E:
            x, y = e.get_vertices()
            E_map[Edge(V_map_inv[x], V_map_inv[y], deepcopy(e.get_value()))] = e
        g = EnergyMinimization(V_map.keys(), E_map.keys(), self.get_tau())
        g.prepare()
        for gamma in self.__gamma():
            g.remove_small(0.5)
            if not g.is_neighborhood_corrupted():
                break
            g.restore()
            self.__iteration(g, gamma)
        domain = g.get_domains().pop()
        vertices = [g.get_domain(domain).pop()]
        edges = []
        while True:
            need_break = True
            inputs = vertices[0].get_inputs().intersection(g.get_edges())
            outputs = vertices[-1].get_outputs().intersection(g.get_edges())
            if len(inputs) > 0:
                edges =  [inputs.pop()] + edges
                vertices = [edges[0].get_vertices()[0]] + vertices
                need_break = False
            if len(outputs) > 0:
                edges =  edges + [outputs.pop()]
                vertices.append(edges[-1].get_vertices()[1])
                need_break = False
            if need_break:
                break
        #return (set(V_map[v] for v in vertices), set(E_map[e] for e in edges))
        return set(V_map[v] for v in vertices)

