from os import path

from build_problem import build_problem

from PIL import Image, ImageDraw
from cProfile import Profile
from pstats import Stats


if __name__ == '__main__':
    model_image = Image.open(path.join(path.dirname(__file__), 'rect_model_10x10.png'))
    model_image_mask = [p[3] > 0 for p in list(model_image.getdata())]
    model_image_grayscale = model_image.convert('L')

    raw_image = Image.open(path.join(path.dirname(__file__), 'rect_big_20x20.png'))
    raw_image_grayscale = raw_image.convert('L')

    problem = build_problem(model_image_grayscale, raw_image_grayscale,
                            model_image_mask)
    profile = Profile()
    profile.enable()
    solution = problem.solve(False)
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()
    result = sorted([(v.get_name(), v.get_domain())
                  for v in solution], key=lambda x: x[0][0] * raw_image.size[0] + x[0][1])
    for r in result:
        print 'Model', r[1], 'to', r[0]

