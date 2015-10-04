from Semiring import SemiringElement


class SemiringMinPlusElement(SemiringElement):


    def __init__(self, value):
        self.value = value


    def mul(self, element):
        return self.value+element


    def add(self, element):
        return min(self.value, element)


    def get_zero(self):
        return float('inf')


    def get_unity(self):
        return 0

