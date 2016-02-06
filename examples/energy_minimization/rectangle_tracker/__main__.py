from os import path
import logging
from argparse import ArgumentParser

from build_problem import build_problem

from PIL import Image, ImageDraw
from cProfile import Profile
from pstats import Stats


if __name__ == '__main__':
    parser = ArgumentParser(description='Rectangle tracker example')
    logger_levels = [logging.getLevelName(i*10) for i in xrange(6)]
    parser.add_argument('-l', '--log', help='set logger level', type=str.upper,
                                       default='ERROR', choices=logger_levels)
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log))

    model_image = Image.open(path.join(path.dirname(__file__), 'rect_model_10x10.png'))
    model_image_mask = [p[3] > 0 for p in list(model_image.getdata())]
    model_image_grayscale = model_image.convert('L')

    raw_image = Image.open(path.join(path.dirname(__file__), 'rect_big_10x10_colorized.png'))
    raw_image_grayscale = raw_image.convert('L')

    problem = build_problem(model_image_grayscale, raw_image_grayscale,
                            model_image_mask, 2, 2)
    profile = Profile()
    #profile.enable()
    solution = problem.solve(False, profile)
    #profile.disable()
    Stats(profile).sort_stats('time').print_stats()
    result = sorted([(v.get_name(), v.get_domain())
                  for v in solution], key=lambda x: x[0][0] * raw_image.size[0] + x[0][1])
    for r in result:
        print 'Model', r[1], 'to', r[0]

