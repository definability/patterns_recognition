class Edge(object):


    def __init__(self, x, y, value=None):
        self.vertices = (x, y)
        self.value = value
        self.visited = False


    def get_vertices(self):
        return self.vertices


    def get_value(self):
        return self.value


    def set_visited(self, is_visited=True):
        self.visited = is_visited


    def is_visited(self):
        return self.visited

