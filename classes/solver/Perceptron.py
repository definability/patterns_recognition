class Perceptron:
    

    def __init__(self, dimensions, epsilon=0):
        self.dimensions = dimensions
        self.left = []
        self.right = []
        self.alpha = [0]*dimensions
        self.__epsilon = epsilon


    def setup(self, left, right):
        self.left.extend(list(left))
        self.right.extend(list(right))
        while self.__setup_loop():
            continue


    def __setup_loop(self):
        wrong = False
        for l in self.left:
            if self.classify_vertex(l) >= 0:
                self.__setup_iteration(l, -1)
                wrong = True
        for r in self.right:
            if self.classify_vertex(r) <= 0:
                self.__setup_iteration(r, 1)
                wrong = True
        return wrong


    def __setup_iteration(self, wrong, sign):
        self.alpha = [a + sign * x for a, x in zip(self.alpha, wrong)]


    def classify_vertex(self, vertex):
        result = sum([a * x for a, x in zip(self.alpha, vertex)])
        if abs(result) <= self.__epsilon:
            return 0
        return 1 if result > 0 else -1

