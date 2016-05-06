from numpy import array, vstack, unique, histogram, full
from numpy.random import choice
from scipy.stats.mstats import mode
try:
    from itertools import izip as zip
except ImportError:
    pass


class ConditionalProbability:


    def __init__(self):
        self.__sample = None
        self.__modes = {}


    def add_sample(self, sample):
        if type(sample) is set:
            sample = list(sample)

        if self.__sample is None:
            self.__sample = array(sample)
        else:
            self.__sample = vstack((self.__sample, sample))


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
            exclude.append(i)

        masked_sample = None
        if values is not None:
            masked_sample = self.__process_masked_sample(exclude, values)
        else:
            masked_sample = self.__sample

        return masked_sample if masked_sample.size > 0 else None


    def __process_masked_sample(self, exclude, values):
        mask = array([True] * self.__sample.shape[1])
        mask[exclude] = False
        indices = (self.__sample[:,mask] == values).all(axis=1)
        return self.__sample[indices]


    def get_mode(self, i):
        if i not in self.__modes:
            occurences = self.__sample[:,i]
            self.__modes[i] = mode(occurences)[0][0]
        return self.__modes[i]

