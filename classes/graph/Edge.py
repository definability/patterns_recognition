class Edge(object):


    def __init__(self, x, y, value=None):
        self.vertices = (x, y)
        self.value = value


    def get_vertices(self):
        return set(self.vertices)


    def get_value(self):
        return self.value

