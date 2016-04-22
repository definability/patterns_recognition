class LinearSeparator:


    def __init__(self, dimensions, classes=2, max_iterations=float('inf')):
        self.dimensions = dimensions
        if type(classes) is int:
            self.classes = [[]] * classes
            self.planes = [[0] * dimensions for i in xrange(len(self.classes))]
        else:
            self.classes = {}
            self.planes = {}
            for c in classes:
                self.classes[c] = []
                self.planes[c] = [0] * dimensions
        self.__max_iterations = max_iterations
        self.passed_iterations = 0


    def __classes(self):
        if type(self.classes) is dict:
            return self.classes.items()
        elif type(self.classes) is list:
            return enumerate(self.classes)
        return None


    def __planes(self):
        if type(self.planes) is dict:
            return self.planes.items()
        elif type(self.planes) is list:
            return enumerate(self.planes)
        return None


    def setup(self, inputs=None):
        if type(inputs) is dict:
            gen = inputs.items()
        elif type(inputs) is list:
            gen = enumerate(inputs)
        else:
            return None

        for key, value in gen:
            self.classes[key] += value

        success = False
        while True:
            corrections = self.__setup_loop()

            if corrections == 0:
                success = True
                break

            self.passed_iterations += corrections
            if self.passed_iterations > self.__max_iterations:
                break
        return success


    def __setup_loop(self):
        corrections = 0
        for (i, c) in self.__classes():
            corrections += self.__setup_class(c, i)
        return corrections


    def __setup_class(self, sample, side):
        corrections = 0
        for s in sample:
            if self.classify_vertex(s) != side:
                self.__setup_iteration(s, side)
                corrections += 1
        return corrections


    def __setup_iteration(self, wrong, side):
        for i, plane in self.__planes():
            sign = 1 if i == side else -1
            self.planes[i] = self.__move_plane(plane, wrong, sign)


    def classify_vertex(self, vertex):
        value = float('-inf')
        side = None
        for i, plane in self.__planes():
            current = self.__get_projection(plane, vertex)
            if value < current:
                value = current
                side = i
            elif value == current:
                side = None
        return side


    def __get_projection(self, plane, vertex):
        return sum([a * x for a, x in zip(plane, vertex)])


    def __move_plane(self, plane, vertex, sign):
        return [a + sign * x for a, x in zip(plane, vertex)]

