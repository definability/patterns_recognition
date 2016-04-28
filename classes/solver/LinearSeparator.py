from numpy import array, zeros, ndenumerate, ones


class LinearSeparator:


    def __init__(self, dimensions, classes=2, max_iterations=float('inf'),
                       binary=False):
        self.dimensions = dimensions
        self.__class_to_number = None
        self.__number_to_class = None
        if type(classes) is int:
            self.classes = [[] for i in xrange(classes)]
        else:
            self.classes = [[] for c in classes]
            self.__class_to_number = {}
            self.__number_to_class = []
            for i, c in enumerate(classes):
                self.__class_to_number[c] = i
                self.__number_to_class.append(c)
        self.planes = zeros((len(self.classes), dimensions))
        self.__max_iterations = max_iterations
        self.passed_iterations = 0
        self.__binary = binary


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
        self.__append_setup_set(inputs)
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


    def __append_setup_set(self, inputs):
        if type(inputs) is dict:
            gen = inputs.items()
        elif type(inputs) is list:
            gen = enumerate(inputs)
        else:
            return None

        if self.__class_to_number is not None:
            for key, value in gen:
                self.classes[self.__class_to_number[key]] += map(array, value)
        else:
            for key, value in gen:
                self.classes[key] += map(array, value)


    def __setup_loop(self):
        corrections = 0
        for (i, c) in self.__classes():
            corrections += self.__setup_class(c, i)
        return corrections


    def __setup_class(self, sample, side):
        corrections = 0
        for s in sample:
            corrections += self.__setup_iteration(s, side)
        return corrections


    def __setup_iteration(self, wrong, side):
        products = self.__get_projections(wrong)
        value = products[side]
        indices = (products >= value)
        if indices.sum() == 1:
            return 0
        if self.__binary:
            self.planes[side][wrong] += 1
            indices[side] = False
            self.planes[indices][:,wrong] -= 1
        else:
            self.planes[side] += wrong
            indices[side] = False
            self.planes[indices] -= wrong
        return 1


    def classify_vertex(self, vertex):
        products = self.__get_projections(vertex)
        side = products.argmax()
        if (products==products[side]).sum() != 1:
            return None
        elif self.__number_to_class is None:
            return side
        else:
            return self.__number_to_class[side]


    def __get_projections(self, vertex):
        if self.__binary:
            return self.planes[:,vertex].sum(axis=1)
        else:
            return self.planes.dot(vertex)

