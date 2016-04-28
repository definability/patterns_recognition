from numpy import array, zeros

from classes.solver import LinearSeparator


class Texture:

    def __init__(self, neighborhoods, colors, textures=2):
        self.dimensions = neighborhoods * (colors * colors) + 1
        self.colors = colors
        self.neighborhoods = neighborhoods
        self.textures = {}
        self.__separator = LinearSeparator(self.dimensions, classes=textures,
                                           binary=True)


    def pick_texture_sample(self, params, texture):
        if texture not in self.textures:
            self.textures[texture] = [self.__get_vector(params)]
        else:
            self.textures[texture].append(self.__get_vector(params))


    def setup(self):
        result = self.__separator.setup(self.textures)
        self.textures = {}
        return result


    def __get_vector(self, params):
        return [self.__get_element_number(key, value)
                for key, value in params.items()] + [-1]


    def __get_element_number(self, neighbourhood, colors):
        assert(len(colors) == 2)
        return neighbourhood * self.colors * self.colors + \
               (colors[0] * self.colors + colors[1])


    def recognize_texture(self, params):
        return self.__separator.classify_vertex(self.__get_vector(params))

