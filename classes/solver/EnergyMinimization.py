from copy import deepcopy

from classes.graph import Graph


class EnergyMinimization(Graph):


    def __init__(self, V, E):
        super(EnergyMinimization, self).__init__(V, E)


    def __gamma(self, k):
        n = 1.
        for i in xrange(k):
            yield n/(i+1)


    def max_vertex(self, vertices):
        return max(vertices, key=lambda v: v.get_value())


    def max_edge(self, edges):
        return max(edges, key=lambda e: e.get_value())


    def __iteration(self, g, gamma):
        for d in g.get_domains():
            max_e = g.max_edge(sum([v.get_outputs()
                                    for v in g.get_domain(domain)))
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
        for domain in g.get_domains():
            vertices = g.get_domain(domain)
            max_v = g.max_vertex(vertices)
            for v in vertices:
                if v.get_value() - max_v.get_value() > treshold:
                    g.delete_vertex(v)
        for domain in g.get_domains():
            edges = sum([v.get_outputs() for v in g.get_domain(domain))
            max_e = g.max_edge(edges)
            for e in edges:
                if e.get_value() - max_e.get_value() > treshold:
                    g.delete_edge(e)


    def solve(self):
        V_map = dict()
        V_map_inv = dict()
        E_map = dict()
        for v in self.V:
            V_map[deepcopy(v)] = v
            V_map_inv[v] = deepcopy(v)
        for e in self.E:
            x, y = e.get_vertices()
            E_map[Edge(V_map_inv(x), V_map_inv(y), deepcopy(e.get_value())) = e
        g = Graph(V_map.keys(), E_map.keys())
        self.prepare()
        for gamma in self.__gamma(10):
            g.remove_small(0.5)
            if g.is_neighborhood_corrupted():
                break
            g.restore()
            self.__iteration(g, gamma)
            break
        result = []
        domain = g.get_domains().pop()
        vertices.append(g.get_domain(domain).pop())
        edges = []
        while True:
            inputs = result[0].get_inputs()
            outputs = result[-1].get_outputs()
            if len(inputs) > 0:
                edges =  [inputs.pop()] + edges
                result = edges[0].get_vertices()[1] + result
            if len(outputs) > 0:
                edges =  edges + [outputs.pop()]
                result.append(edges[-1].get_vertices[0])
        #return (set(V_map[v] for v in vertices), set(E_map[e] for e in edges))
        return set(V_map[v] for v in vertices)

