from classes.graph import Graph


class EnergyMinimization(Graph):


    def __init__(self, V, E):
        super(EnergyMinimization, self).__init__(V, E)


    def __gamma(self):
        n = 1
        i = 0
        while True:
            yield n**(-i)
            i += 1


    def __iteration(self, phi, gamma):
        for domain in self.get_domains():
            max_k = dict()
            for v in self.get_domain(domain):
                for e in v.get_outputs():
                    target_domain = e.get_vertices()[1].domain
                    if target_domain not in max_k:
                        max_k[(domain, target_domain)] = (None, float('-inf'))
                    if e.get_vertices() not in phi:
                        phi[e.get_vertices()] = 0
                    if e.get_vertices()[::-1] not in phi:
                        phi[e.get_vertices()[::-1]] = 0
                    tmp = e.get_value() + phi[e.get_vertices()] \
                                        + phi[e.get_vertices()[::-1]]
                    if max_k[(domain, target_domain)][1] < tmp:
                        max_k[(domain, target_domain)] = (e.get_vertices(), tmp)
            for d in max_k:
                phi[max_k[d][0]] -= gamma
                phi[max_k[d][0][::-1]] -= gamma

        for domain in self.get_domains():
            max_k = (None, float('-inf'))
            for v in self.get_domain(domain):
                tmp = v.get_value()
                for e in v.get_outputs():
                    if (v, e[1]) not in phi:
                        phi[(v, e[1])] = 0
                    else:
                        tmp -= phi[(v, e[1])]
                if max_k[1] < tmp:
                    max_k = (v, tmp)
            for e in max_k[0].get_outputs():
                phi[e.get_vertices()] += gamma


    def solve(self):
        phi = dict()
        for gamma in self.__gamma():
            self.__iteration(phi, gamma)
            break
        result = dict()
        for domain in self.get_domains():
            result[domain] = (None, float('-inf'))
            for v in self.get_domain(domain):
                tmp = v.get_value() - sum(phi[v, e[1]] for e in v.get_outputs())
                if result[domain][1] < tmp:
                    result[domain] = (v, tmp)
        return set(result[domain][0] for domain in result)

