from os.path import join as pjoin, dirname
from sys import argv
from random import randint
from numpy import array
import logging

from PIL import Image

from .Texture import Texture
from .neighbourhood import neighbourhoods

from cProfile import Profile
from pstats import Stats
try:
    range = xrange
except NameError:
    pass


def process_colors(pixel, colors):
    if type(pixel) is tuple or type(pixel) is list:
        d = [(colors * p) // 256 for p in pixel]
        p = reduce(lambda x, y: x*colors+y, d, 0)
    else:
        p = colors * (pixel + 1) / 256
    return p


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    image_name = argv[1]
    mask_name = argv[2]
    test_name = argv[3]
    result_name = argv[4]
    colors = int(argv[5])
    textures = int(argv[6])
    neighbourhood_class = int(argv[7])

    RGB_MODE=True
    cur_neighbourhood = neighbourhoods[neighbourhood_class]

    image = Image.open(pjoin(dirname(__file__), image_name))
    if not RGB_MODE:
        image = Image.open(pjoin(dirname(__file__), image_name)).convert('L')
    mask = Image.open(pjoin(dirname(__file__), mask_name))
    width, height = image.size

    data = list(image.getdata())
    mask_data = list(mask.getdata())
    known_classes = []
    border = neighbourhood_class - 1 if neighbourhood_class > 1 else 0

    profile = Profile()
    profile.enable()
    texture = Texture(textures)
    np_data = (array(data)) * colors // 256
    if RGB_MODE:
        np_data = np_data[:,2] + colors * (np_data[:,1] + colors * np_data[:,0])
    data = np_data
    for x in range(border, height-border-1):
        for y in range(border, width-border-1):
            cur = data[x*width+y]

            sample = [cur]

            for key, n in enumerate(cur_neighbourhood):
                i, j = n(x, y)
                neighbour_color = data[i*width+j]
                sample.append(neighbour_color)

            cur_mask = mask_data[x*width+y]
            if sum(cur_mask) == 0:
                continue
            if cur_mask not in known_classes:
                known_classes.append(cur_mask)

            texture.pick_texture_sample(sample, known_classes.index(cur_mask))
    texture.setup()
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()

    test_image = Image.open(pjoin(dirname(__file__), test_name))
    if not RGB_MODE:
        test_image = test_image.convert('L')
    test_width, test_height = test_image.size
    test_data = list(test_image.getdata())
    results = []

    for x in range(test_height):
        row = []
        for y in range(test_width):
            cur = test_data[x*test_width+y]
            row.append(known_classes.index(cur))
        results.append(row)
    logging.debug('Mask is ready')

    profile = Profile()
    profile.enable()
    field = texture.generate(results, neighbourhoods[neighbourhood_class], 0)
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()

    profile = Profile()
    profile.enable()
    result = []
    def get_c(v, n):
        return (((v // (colors**(n-1))) % colors) * 256) // colors
        #return (v // (colors**(n-1))) % colors
    for i in range(len(field)):
        for j in range(len(field[i])):
            v = field[i][j]
            result.append((get_c(v, 3), get_c(v, 2), get_c(v, 1)))
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()

    result_image = Image.new('RGB', test_image.size)
    result_image.putdata(result)
    result_image.save(pjoin(dirname(__file__), result_name))

