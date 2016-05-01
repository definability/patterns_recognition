from numpy import array, concatenate, unique, histogram, full
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


    def get_probabilities(self, i, values=None, exclude=None):
        if exclude is None:
            exclude = [i]
        else:
            exclude.append([i])

        if values is not None:
            mask = full(self.__sample.shape[1], True, dtype=bool)
            mask[exclude] = False
            indices = (self.__sample[:,mask] == values).all(axis=1)
            samples = self.__sample[indices]
        else:
            samples = self.__sample

        occurences = samples[:,i]
        if occurences.size == 0:
            return {}

        values = unique(occurences)
        values.sort()
        hist, _ = histogram(occurences, concatenate((values, [values[-1]])))

        return dict(izip(values, hist/hist.sum().astype('float')))

