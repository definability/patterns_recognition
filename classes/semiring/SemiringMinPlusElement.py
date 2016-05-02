from .SemiringElement import SemiringElement


class SemiringMinPlusElement(SemiringElement):


    def __init__(self, value=None):
        super(SemiringMinPlusElement, self).__init__(value)


    def mul(self, element):
        self.value += element.value
        return self


    def add(self, element):
        self.value = min(self.value, element.value)
        return self


    @staticmethod
    def get_zero():
        return float('inf')


    @staticmethod
    def get_unity():
        return 0

