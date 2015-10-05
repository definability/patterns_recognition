class Graph(object):


    def __init__(self, V=None, E=None):
        if V is None:
            self.V = set()
        else:
            self.V = V
        if E is None:
            self.E = set()
        else:
            self.E = E

