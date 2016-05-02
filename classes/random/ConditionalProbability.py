from numpy import array, concatenate, unique, histogram, full
from numpy.random import choice
from scipy.stats.mstats import mode
try:
    from itertools import izip as zip
except ImportError:
    pass


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
        masked_sample = self.__masked_sample(i, values, exclude)
        if masked_sample is None:
            return {}
        occurences = self.__masked_sample(i, values, exclude)[:,i]

        values = unique(occurences)
        values.sort()
        hist, _ = histogram(occurences, concatenate((values, [values[-1]])))

        return dict(zip(values, hist/hist.sum().astype('float')))


    def get_random(self, i, values=None, exclude=None, default=None):
        masked_sample = self.__masked_sample(i, values, exclude)
        if masked_sample is None:
            return default

        occurences = masked_sample[:,i]
        return choice(occurences)


    def __masked_sample(self, i, values=None, exclude=None):
        if exclude is None:
            exclude = [i]
        else:
            exclude.append([i])

        masked_sample = None
        if values is not None:
            mask = full(self.__sample.shape[1], True, dtype=bool)
            mask[exclude] = False
            indices = (self.__sample[:,mask] == values).all(axis=1)
            masked_sample = self.__sample[indices]
        else:
            masked_sample = self.__sample

        return masked_sample if masked_sample.size > 0 else None


    def get_mode(self, i):
        occurences = self.__sample[:,i]
        return mode(occurences)[0][0]

