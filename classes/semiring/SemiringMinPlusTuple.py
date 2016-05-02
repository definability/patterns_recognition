from copy import copy

from .SemiringElement import SemiringElement


class SemiringMinPlusTuple(SemiringElement):


    def __init__(self, value=None, factor=1):
        self.factor = factor
        super(SemiringMinPlusTuple, self).__init__(value)


    def mul(self, element):
        self.value = (self.value[0] + element.value[0],
                      self.value[1] + element.value[1])
        return self


    def get_absolute_value(self):
        return self.value[0] + self.value[1]*self.factor


    def add(self, element):
        if self.get_absolute_value() > element.get_absolute_value():
            self.value = copy(element.value)
            self.factor = element.factor
        return self


    @staticmethod
    def get_zero():
        return (float('inf'), float('inf'))


    @staticmethod
    def get_unity():
        return (0, 0)

