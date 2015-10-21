import numpy


class Image:


    def __init__(self, data, height=None, width=None):
        self.height = height or len(data)
        self.data = numpy.array(data).flatten()
        self.width = width or self.data.size/self.height


    def get_matrix(self):
        return self.data.reshape(self.height, self.width)


    def crop_vertical(self, height, offset=0):
        return self.get_matrix()[offset:offset+height]


    def crop_horizontal(self, width, offset=0):
        return self.get_matrix()[:,offset:offset+width]

