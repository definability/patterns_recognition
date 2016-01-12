from classes.graph import Graph


class EnergyMinimization(Graph):


    def __init__(self, V, E):
        super(EnergyMinimization, self).__init__(V, E)


    def __gamma(self, k):
        n = 1.
        for i in xrange(k):
            yield n/(i+1)


    def __iteration(self, phi, gamma):
        for domain in self.get_domains():
            max_k = dict()
            for v in self.get_domain(domain):
                print 'ITER', len(v.get_outputs()), len(self.E)
                print v.get_domain(), v.get_value()
                for e in v.get_outputs():
                    print e.get_vertices()[0].get_domain(), e.get_vertices()[0].get_value(), e.get_vertices()[1].get_domain(), e.get_vertices()[1].get_value()
                    target_domain = e.get_vertices()[1].domain
                    if (domain, target_domain) not in max_k:
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
        results = []
        for e in phi:
            v1, v2 = e
            results.append('%s->%s, %d %d %f'%(v1.get_domain(), v2.get_domain(),
                    v1.get_value(), v2.get_value(), phi[e]))
        print '\n'.join(sorted(results))
        print
        print

        for domain in self.get_domains():
            max_k = (None, float('-inf'))
            for v in self.get_domain(domain):
                tmp = v.get_value()
                for e in v.get_outputs():
                    if e.get_vertices() not in phi:
                        phi[e.get_vertices()] = 0
                    else:
                        tmp -= phi[e.get_vertices()]
                if max_k[1] < tmp:
                    max_k = (v, tmp)
            for e in max_k[0].get_outputs():
                phi[e.get_vertices()] += gamma


    def solve(self):
        self.prepare()
        phi = dict()
        for gamma in self.__gamma(1000):
            self.__iteration(phi, gamma)
        result = dict()
        print
        for domain in self.get_domains():
            result[domain] = (None, float('-inf'))
            for v in self.get_domain(domain):
                tmp = v.get_value() - sum(phi[e.get_vertices()] \
                                          for e in v.get_outputs())
                print '%s (%d): %f'%(v.get_domain(), v.get_value(), tmp)
                if result[domain][1] < tmp:
                    result[domain] = (v, tmp)
        print
        ##print phi
        print [(result[domain][0].get_value(), result[domain][1]) for domain in result]
        return set(result[domain][0] for domain in result)

