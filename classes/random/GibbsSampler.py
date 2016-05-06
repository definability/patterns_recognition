import logging
from numpy import array, zeros_like, ones_like, nditer, ndindex

from .ConditionalProbability import ConditionalProbability
try:
    range = xrange
except NameError:
    pass


class GibbsSampler:


    def __init__(self, classes=2):
        if type(classes) is list:
            self.__p = {}
            self.__classes = classes
            for c in classes:
                self.__p[c] = ConditionalProbability()
        else:
            self.__p = [ConditionalProbability() for i in range(classes)]
            self.__classes = list(range(classes))


    def add_sample(self, sample, texture=None):
        if texture is None:
            for c in self.__classes:
                if c in sample:
                    self.__p[c].add_sample(sample[c])
        self.__p[texture].add_sample(sample)


    def generate(self, mask, neighbor_getters=None, iterations=0):
        mask = array(mask)
        field = self.__get_initial_fill(mask)
        #field = self.__get_initial_negatives(mask)
        if iterations == 0 or neighbor_getters is None:
            return field
        for i in range(iterations):
            field = self.__get_field_iteration(field, mask, neighbor_getters, i)
        return field


    def __get_initial_negatives(self, mask):
        return ones_like(mask) * (-1)


    def __get_initial_fill(self, mask):
        field = zeros_like(mask)
        for i in ndindex(mask.shape):
            field[i] = self.__p[mask[i]].get_random(0)
        return field


    def __get_field_iteration(self, field, mask, neighbor_getters, it):
        row = 0
        negatives = 0
        for i in ndindex(field.shape):
            if row != i[0]:
                row = i[0]
            field[i] = self.__get_pixel_iteration(field, i, mask[i],
                                                  neighbor_getters)
            if field[i] < 0:
                field[i] = self.__p[mask[i]].get_random(0)
                negatives += 1
        logging.debug('{}: {} negatives found'.format(it, negatives))
        return field


    def __get_pixel_iteration(self, field, position, texture, neighbor_getters):
        exclude = []
        values = []
        for i, n in enumerate(neighbor_getters):
            try:
                v = field[n(*position)]
                if v > 0:
                    values.append(v)
                else:
                    exclude.append(i+1)
            except IndexError:
                exclude.append(i+1)
        if len(exclude) == 0:
            exclude = None
        return self.__p[texture].get_random(0, values, exclude, -1)

