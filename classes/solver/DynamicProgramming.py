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


    def __prepare(self, semiring):

        for vertex in self.V:
            vertex.clear_inputs()
            vertex.clear_outputs()
            vertex.set_value(semiring.zero())

        for edge in self.E:
            vertices = edge.get_vertices()
            vertices[0].add_output(edge)
            vertices[1].add_input(edge)


    def __process_vertex(self, vertex, reached, to_visit):
        for edge in vertex.get_outputs():

            end = edge.get_vertices()[1]
            end.set_value(vertex.get_value() * edge.get_value() + end.get_value())

            end.remove_input(edge)
            reached.add(end)

            if len(end.get_inputs()) == 0:
                to_visit.add(end)
                reached.remove(end)


    def solve(self, semiring):

        self.__prepare(semiring)

        to_visit = set([self.end, self.start])
        reached = set()

        while len(to_visit) and self.end not in reached:
            self.__process_vertex(to_visit.pop(), reached, to_visit)

        return self.end.get_value()

