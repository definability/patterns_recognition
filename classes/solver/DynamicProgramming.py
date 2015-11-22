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
            vertex.clear_inputs()
            vertex.clear_outputs()
            if vertex.get_value() is not None and not isinstance(vertex.get_value(), semiring):
                vertex.set_value(semiring(vertex.get_value()))


        for edge in self.E:
            vertices = edge.get_vertices()
            vertices[0].add_output(edge)
            vertices[1].add_input(edge)
            if not isinstance(edge.get_value(), semiring):
                edge.set_value(semiring(edge.get_value()))


    def __process_vertex(self, vertex, visited, to_visit, caddy, semiring):
        for edge in vertex.get_outputs():

            finish = edge.get_vertices()[1]
            finish_value = semiring.unity() if finish.get_value() is None \
                                            else finish.get_value()
            edge_value = semiring.unity() if edge.get_value() is None \
                                          else edge.get_value()
            if finish not in caddy:
                caddy[finish] = caddy[vertex] * edge_value * finish_value
            else:
                caddy[finish] += caddy[vertex] * edge_value * finish_value


            finish.remove_input(edge)

            if len(finish.get_inputs()) == 0:
                to_visit.add(finish)


    def solve(self, semiring):

        self.__prepare(semiring)

        to_visit = set([self.finish, self.start])
        visited = set()

        caddy = {
            self.start: semiring.unity() if self.start.get_value() is None \
                                         else self.start.get_value()
        }

        while len(to_visit) and self.finish not in visited:
            self.__process_vertex(to_visit.pop(), visited, to_visit, caddy, semiring)

        return caddy[self.finish]

