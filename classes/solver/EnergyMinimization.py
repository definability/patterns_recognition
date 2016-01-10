from classes.graph import Graph


class EnergyMinimization(Graph):


    def __init__(self, V, E):
        super(EnergyMinimization, self).__init__(V, E)


    def __gamma(self):
        i = 0
        while True:
            yield n**(-i)
            i += 1


    def __iteration(self, phi, gamma):
        max_k = (None, float('-inf'))
        for v in self.V:
            for e in v.get_outputs():
                tmp = e.get_value() + phi[e.get_vertices()] \
                                    + phi[e.get_vertices()[::-1]]
                if max_k[1] < tmp:
                    max_k = (e.get_vertices(), tmp)
        phi[max_k[0].get_vertices()] -= gamma
        phi[max_k[0].get_vertices()[::-1]] -= gamma

        max_k = (None, float('-inf'))
        for v in self.V:
            tmp = v.get_value() - sum(phi[v.get_outputs()].values())
            if max_k[1] < tmp:
                max_k = (v, tmp)
        for e in max_k[0].get_outputs():
            phi[e.get_vertices()] += gamma

