from copy import deepcopy

from classes.graph import Graph, Edge, Vertex


class EnergyMinimization(Graph):


    def __init__(self, V, E, tau=set()):
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


    def __iteration(self, g, gamma):
        for domain in g.get_domains():
            max_edges = dict()
            for v in self.get_domain(domain):
                outputs = v.get_outputs()
                if len(outputs) == 0:
                    continue
                for output in outputs:
                    end = output.get_vertices()[1]
                    d = end.get_domain()
                    if d not in max_edges or max_edges[d].get_value() < output.get_value():
                        max_edges[d] = output
            #max_e = []
            #for v in g.get_domain(domain):
            #    outputs = v.get_outputs()
            #    if len(outputs) == 0:
            #        continue
            #    max_e.append(g.max_edge(outputs))
            #if len(max_e) == 0:
            #    continue
            #max_e = g.max_edge(max_e)
            for e in max_edges:
                max_e = max_edges[e]
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
        remove_after = True
        nrg = 0
        for domain in self.get_domains():
            vertices = self.get_domain(domain, True)
            if len(vertices) == 0:
                continue
            max_v = self.max_vertex(vertices)
            nrg += max_v.get_value()
            for v in vertices:
                if max_v.get_value() - v.get_value() > treshold:
                    self.delete_vertex(v, remove_after)
        for domain in self.get_domains():
            max_e = dict()
            for v in self.get_domain(domain):
                outputs = v.get_outputs()
                if len(outputs) == 0:
                    continue
                for output in outputs:
                    end = output.get_vertices()[1]
                    d = end.get_domain()
                    if d not in max_e or max_e[d].get_value() < output.get_value():
                        max_e[d] = output
            nrg += sum(max_e[e].get_value() for e in max_e)
            for v in self.get_domain(domain):
                for e in v.get_outputs():
                    if max_e[e.get_vertices()[1].get_domain()].get_value() - e.get_value() > treshold:
                        self.delete_edge(e, remove_after)
        if remove_after:
            self.delete_corrupted()
        return nrg


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


    def solve(self, make_copy=True):
        g, V_map, E_map = None, None, None
        if make_copy:
            g, V_map, E_map = self.get_mapped_copy()
        else:
            g = self
        g.prepare()
        step = 0
        for gamma in self.__gamma():
            nrg = g.remove_small(0.5)
            print 'step %06d, gamma %f, energy %f'%(step, gamma, nrg)
            if not g.is_neighborhood_corrupted():
                break
            g.restore()
            self.__iteration(g, gamma)
            step += 1
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
        if make_copy:
            #return (set(V_map[v] for v in vertices), set(E_map[e] for e in edges))
            return set(V_map[v] for v in vertices)
        else:
            return vertices

