from os.path import join as pjoin, dirname
from sys import argv
from random import randint

from PIL import Image

from Texture import Texture
from neighbourhood import neighbourhoods

from cProfile import Profile
from pstats import Stats

if __name__ == '__main__':
    image_name = argv[1]
    mask_name = argv[2]
    test_name = argv[3]
    result_name = argv[4]
    colors = int(argv[5])
    textures = int(argv[6])
    neighbourhood_class = int(argv[7])

    cur_neighbourhood = neighbourhoods[neighbourhood_class]

    texture = Texture(len(cur_neighbourhood), colors, textures)
    image = Image.open(pjoin(dirname(__file__), image_name))
    mask = Image.open(pjoin(dirname(__file__), mask_name))
    width, height = image.size

    data = list(image.getdata())
    mask_data = list(mask.getdata())
    known_classes = []
    border = neighbourhood_class - 1 if neighbourhood_class > 1 else 0

    profile = Profile()
    profile.enable()
    for x in xrange(border, height-border-1):
        for y in xrange(border, width-border-1):
            d = data[x*width+y]
            rgb = (d[0] * (2**8) + d[1]) * (2**8) + d[2]
            cur = ((colors-1) * (rgb + 1)) / (2**24)

            params = {}

            for key, n in enumerate(cur_neighbourhood):
                i, j = n(x, y)
                d = data[i*width+j]
                rgb = (d[0] * (2**8) + d[1]) * (2**8) + d[2]
                p = ((colors-1) * (rgb + 1)) / (2**24)
                params[key] = (cur, p)

            cur_mask = mask_data[x*width+y]
            if sum(cur_mask) == 0:
                continue
            if cur_mask not in known_classes:
                known_classes.append(cur_mask)

            print 'Pick {}: ({}, {})'.format(known_classes.index(cur_mask), x, y)
            texture.pick_texture_sample(params, known_classes.index(cur_mask))
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()

    test_image = Image.open(pjoin(dirname(__file__), test_name)).convert('L')
    test_width, test_height = test_image.size
    test_data = list(test_image.getdata())
    results = []

    profile = Profile()
    profile.enable()
    for x in xrange(test_height):
        row = []
        for y in xrange(test_width):
            cur = ((colors-1) * (test_data[x*test_width+y] + 1)) / 256

            params = {}
            for key, n in enumerate(cur_neighbourhood):
                i, j = n(x, y)
                if i < test_height and j < test_width and i>0 and j>0:
                    p = ((colors-1) * (test_data[i*test_width+j] + 1)) / 256
                params[key] = (cur, p)

            t = texture.recognize_texture(params)
            row.append(t)
        results += row
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()

    result_colors = {}
    result_colors[None] = (0, 0, 0)
    for i in xrange(len(cur_neighbourhood)):
        result_colors[i] = (randint(0, 255), randint(0, 255), randint(0, 255))
    results = [result_colors[r] for r in results]
    result = Image.new('RGB', test_image.size)
    result.putdata(results)
    result.save(pjoin(dirname(__file__), result_name))

