import numpy


class Image:


    def __init__(self, data, height=None, width=None):
        self.height = height or len(data)
        self.data = numpy.array(data).flatten()
        self.width = width or self.data.size/self.height


    def get_matrix(self):
        return self.data.reshape(self.height, self.width)


    def get_data(self):
        return self.data


    def crop_horizontal(self, height, offset=0):
        return self.get_matrix()[offset:offset+height]


    def split_horizontal(self, height):
        return (self.get_matrix()[0:height], self.get_matrix()[height:])


    def crop_vertical(self, width, offset=0):
        return self.get_matrix()[:,offset:offset+width]


    def split_vertical(self, width, offset=0):
        return (self.get_matrix()[:,0:width], self.get_matrix()[:,width:])


    def __sub__(self, image):
        if self.height != image.height or self.width != image.width:
            raise ValueError('Images must have equal sizes')
        return Image(self.get_data() - image.get_data(), image.height, image.width)


    def __isub__(self, image):
        if self.height != image.height or self.width != image.width:
            raise ValueError('Images must have equal sizes')
        self.data -= image.get_data()
        return self

