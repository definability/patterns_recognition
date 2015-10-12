from classes.graph import Graph


class DynamicProgramming(Graph):


    def __init__(self, V, E):
        super(DynamicProgramming, self).__init__(V, E)


    def set_start(self, vertex):
        if vertex not in self.V:
            raise ValueError("Vertex should be in graph's vertices set")
        self.start = vertex


    def set_finish(self, vertex):
        if vertex not in self.V:
            raise ValueError("Vertex should be in graph's vertices set")
        self.finish = vertex


    def __prepare(self, semiring):

        for vertex in self.V:
            vertex.clear_outputs()
            vertex.set_value(semiring.zero())

        self.start.set_value(semiring.unity())

        for edge in self.E:
            vertices = edge.get_vertices()
            vertices[0].add_output(edge)
            vertices[1].add_input(edge)


    def __process_vertex(self, vertex, visited, to_visit):
        for edge in vertex.get_outputs():

            finish = edge.get_vertices()[1]
            finish.set_value(vertex.get_value() * edge.get_value() + finish.get_value())

            finish.remove_input(edge)

            if len(finish.get_inputs()) == 0:
                to_visit.add(finish)


    def solve(self, semiring):

        self.__prepare(semiring)

        to_visit = set([self.finish, self.start])
        visited = set()

        while len(to_visit) and self.finish not in visited:
            self.__process_vertex(to_visit.pop(), visited, to_visit)

        return self.finish.get_value()

