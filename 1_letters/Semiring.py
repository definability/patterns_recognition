class SemiringElement:


    def __init__(self, value):
        self.value = value


    def mul(self, element):
        raise NotImplementedError()


    def add(self, element):
        raise NotImplementedError()


    def get_zero(self):
        raise NotImplementedError()


    def get_unity(self):
        raise NotImplementedError()

