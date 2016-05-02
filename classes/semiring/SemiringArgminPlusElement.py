from copy import copy

from .SemiringElement import SemiringElement


class SemiringArgminPlusElement(SemiringElement):


    def __init__(self, value=None):
        if value is not None and type(value[1]) is not list:
            value = (value[0], [value[1]])
        super(SemiringArgminPlusElement, self).__init__(value)


    def mul(self, element):
        self.value = (self.value[0] + element.value[0],
                      self.value[1] + element.value[1])
        return self


    def add(self, element):
        if self.value[0] > element.value[0]:
            self.value = (element.value[0], element.value[1])
        return self


    @staticmethod
    def get_zero():
        return (float('inf'), [])


    @staticmethod
    def get_unity():
        return (0, [])


