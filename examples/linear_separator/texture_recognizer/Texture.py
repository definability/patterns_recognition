from numpy import array, zeros

from classes.solver import LinearSeparator


class Texture:

    def __init__(self, neighborhoods, colors, textures=2):
        self.__colors = colors
        self.__neighborhoods = neighborhoods
        self.__dimensions = self.__neighborhoods * (self.__colors**2) + 1
        self.__textures = {}
        self.__separator = LinearSeparator(self.__dimensions,
                                           classes=self.__textures, binary=True)


    def pick_texture_sample(self, params, texture):
        if texture not in self.__textures:
            self.__textures[texture] = [self.__get_vector(params)]
        else:
            self.__textures[texture].append(self.__get_vector(params))


    def setup(self):
        result = self.__separator.setup(self.__textures)
        self.__textures = {}
        return result


    def __get_vector(self, params):
        return [self.__get_element_number(key, value)
                for key, value in params.items()] + [-1]


    def __get_element_number(self, neighbourhood, colors):
        assert(len(colors) == 2)
        return neighbourhood * self.__colors * self.__colors + \
               (colors[0] * self.__colors + colors[1])


    def recognize_texture(self, params):
        return self.__separator.classify_vertex(self.__get_vector(params))

