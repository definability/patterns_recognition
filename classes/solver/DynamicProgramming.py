from classes.graph import Graph


class DynamicProgramming(Graph):


    def __init__(self, V, E):
        super(DynamicProgramming, self).__init__(V, E)


    def set_start(self, vertex):
        if vertex not in self.V:
            raise ValueError("Vertex should be in graph's vertices set")
        self.start = vertex


    def set_end(self, vertex):
        if vertex not in self.V:
            raise ValueError("Vertex should be in graph's vertices set")
        self.end = vertex


    def prepare(self):
        for edge in self.E:
            vertices = edge.get_vertices()
            vertices[0].add_output(edge)
            vertices[1].add_input(edge)
            edge.set_visited(False)

