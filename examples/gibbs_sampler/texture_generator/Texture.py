import logging
from numpy import array, zeros

from classes.random import GibbsSampler


class Texture:


    def __init__(self, textures=2):
        self.__sampler = GibbsSampler(textures)
        self.__samples = {}


    def pick_texture_sample(self, sample, texture):
        if texture not in self.__samples:
            self.__samples[texture] = []
        self.__samples[texture].append(sample)


    def setup(self):
        for k, s in self.__samples.items():
            self.__sampler.add_sample(s, k)


    def generate(self, mask, neighbor_getters=None, iterations=0):
        return self.__sampler.generate(mask, neighbor_getters, iterations)

