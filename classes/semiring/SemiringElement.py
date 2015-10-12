class SemiringElement(object):


    def __init__(self, value=None):
        if value is None:
            self.value = self.zero()
        else:
            self.value = value


    def mul(self, element):
        raise NotImplementedError()


    def add(self, element):
        raise NotImplementedError()

    @classmethod
    def zero(cls):
        return cls(cls.get_zero())

    @classmethod
    def unity(cls):
        return cls(cls.get_unity())

    @staticmethod
    def get_zero():
        raise NotImplementedError()


    @staticmethod
    def get_unity():
        raise NotImplementedError()


    def __iadd__(self, b):
        return self.add(b)

    def __imul__(self, b):
        return self.mul(b)

    def __add__(self, b):
        return self.__class__(self.value).add(b)

    def __mul__(self, b):
        return self.__class__(self.value).mul(b)

    def __eq__(self, b):
        return self.value == b.value

    def __neq__(self, b):
        return self.value != b.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

