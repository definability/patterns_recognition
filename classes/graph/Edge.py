class Edge(object):


    def __init__(self, x, y, value=None):
        self.vertices = (x, y)
        self.value = value


    def get_vertices(self):
        return self.vertices


    def get_value(self):
        return self.value


    def set_value(self, value):
        self.value = value

