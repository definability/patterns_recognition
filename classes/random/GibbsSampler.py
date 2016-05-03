import logging
from numpy import array, zeros_like, nditer, ndindex

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


    def generate(self, mask):
        mask = array(mask)
        field = self.__get_initial_fill(mask)
        return field


    def __get_initial_fill(self, mask):
        field = zeros_like(mask)
        for i in ndindex(mask.shape):
            field[i] = self.__p[mask[i]].get_random(0)
        return field

