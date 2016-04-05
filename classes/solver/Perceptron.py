class Perceptron:
    

    def __init__(self, dimensions, epsilon=0, D=float('inf')):
        self.dimensions = dimensions
        self.left = None
        self.right = None
        self.alpha = [0]*dimensions
        self.__epsilon = epsilon
        self.__D = D
        self.__calculate_max_steps_count()


    def setup(self, left=None, right=None):
        if self.left is None:
            self.left = left
        else:
            self.left += left
        if self.right is None:
            self.right = right
        else:
            self.right += right

        success = False
        step = 0
        while True:
            corrections = self.__setup_loop()

            if corrections == 0:
                success = True
                break

            step += corrections
            if step > self.get_max_steps_count():
                break
        return success


    def __setup_loop(self):
        corrections = 0
        for l in self.left:
            if self.classify_vertex(l) >= 0:
                self.__setup_iteration(l, -1)
                corrections += 1
        for r in self.right:
            if self.classify_vertex(r) <= 0:
                self.__setup_iteration(r, 1)
                corrections += 1
        return corrections


    def __setup_iteration(self, wrong, sign):
        self.alpha = [a + sign * x for a, x in zip(self.alpha, wrong)]


    def classify_vertex(self, vertex):
        result = sum([a * x for a, x in zip(self.alpha, vertex)])
        if float(result) == 0.0:
            return 0
        return 1 if result > 0 else -1


    def __calculate_max_steps_count(self):
        if float(self.__epsilon) == 0.0 or self.__D == float('inf'):
            self.__steps = float('inf')
            return
        self.__steps = (self.__D/self.__epsilon)**2


    def get_max_steps_count(self):
        return self.__steps

