from numpy import array, concatenate


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

