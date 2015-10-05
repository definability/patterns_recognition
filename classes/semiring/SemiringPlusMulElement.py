from copy import copy

from SemiringElement import SemiringElement


class SemiringPlusMulElement(SemiringElement):


    def __init__(self, value=None):
        super(SemiringPlusMulElement, self).__init__(value)


    def mul(self, element):
        self.value *= element.value
        return self


    def add(self, element):
        self.value += element.value
        return self


    @staticmethod
    def get_zero():
        return 0


    @staticmethod
    def get_unity():
        return 1

