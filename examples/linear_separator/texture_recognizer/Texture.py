from classes.solver import LinearSeparator


class Texture:

    def __init__(self, neighborhoods, colors, textures=2):
        self.dimensions = neighborhoods * (colors) * (colors) + 1
        self.colors = colors
        self.neighborhoods = neighborhoods
        self.__separator = LinearSeparator(self.dimensions, classes=textures)


    def pick_texture_sample(self, params, texture):
        print self.__get_vector(params)
        return self.__separator.setup({texture: [self.__get_vector(params)]})


    def __get_vector(self, params):
        x = [0] * self.dimensions
        x[-1] = 1
        for key, value in params.items():
            x[self.__get_element_number(key, value)] = 1
        return x


    def __get_element_number(self, neighbourhood, colors):
        return neighbourhood * self.colors * self.colors + \
               (colors[0] * self.colors + colors[1])


    def recognize_texture(self, params):
        return self.__separator.classify_vertex(self.__get_vector(params))

