class Graph(object):


    def __init__(self, V, E):

        if not isinstance(V, set):
            raise ValueError("You should provide set of vertices")
        else:
            self.V = V

        if not isinstance(E, set):
            raise ValueError("You should provide set of edges")
        else:
            self.E = E

        for e in E:
            self.check_edge(e)


    def check_edge(self, e):
        if e.vertices[0] not in self.V or e.vertices[1] not in self.V:
            raise ValueError("All vertices should be in graph's vertices' set")

