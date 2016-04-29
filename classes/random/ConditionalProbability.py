from numpy import array, concatenate, unique, histogram, zeros
from itertools import izip


class ConditionalProbability:


    def __init__(self):
        self.__sample = None


    def add_sample(self, sample):
        if type(sample) is set:
            sample = list(sample)

        if self.__sample is None:
            self.__sample = array(sample)
        else:
            self.__sample = concatenate((self.__sample, sample))


    def get_probabilities(self, i, values):
        indices = (self.__sample == values)
        lefts = indices[:,:i].all(axis=1)
        rights = indices[:,i+1:].all(axis=1)
        indices = lefts & rights

        samples = self.__sample[lefts & rights]
        occurences = samples[:,i]
        if occurences.size == 0:
            return {}

        values = unique(occurences)
        values.sort()
        hist = histogram(occurences, concatenate((values, [values[-1]])))[0]

        return dict(izip(values, hist/hist.sum().astype('float')))

