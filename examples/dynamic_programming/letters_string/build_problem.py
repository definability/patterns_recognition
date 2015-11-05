from classes.semiring import *
from classes.graph import *
from classes.image import *
from classes.solver import *

from cProfile import Profile
from pstats import Stats


image_cache = {}

def get_cached(image, offset, width):
    if image_cache.has_key(offset):
        if image_cache[offset].has_key(width):
            return image_cache[offset][width]
        image_cache[offset][width] = image.split_vertical(width)
        return image_cache[offset][width]
    image_cache[offset] = dict()
    image_cache[offset][width] = image.split_vertical(width)
    return image_cache[offset][width]


def process_img(img, patterns, previous_vertex, offset=0, vertices=None, edges=None):

    if vertices is None:
        vertices = dict()
    if edges is None:
        edges = set()

    for p in patterns:

        if patterns[p].width > img.width:
            continue

        img_left, img_right = get_cached(img, offset, patterns[p].width)

        current_vertex = Vertex(p)
        current_key = offset+patterns[p].width
        if vertices.has_key(current_key):
            vertices[current_key].append(current_vertex)
        else:
            vertices[current_key] = [current_vertex]
        sigma = ((Image(img_left).data-patterns[p].data)**2).sum()

        edge = Edge(previous_vertex, current_vertex, (sigma,p))
        edges.add(edge)

        process_img(Image(img_right), patterns, current_vertex, offset+patterns[p].width, vertices, edges)

    return vertices, edges


def build_problem(main_img, patterns_imgs, Semiring=SemiringArgminPlusElement):

    image = Image(list(main_img.getdata()), main_img.size[1], main_img.size[0])
    patterns = dict()
    for p in patterns_imgs:
        patterns[p] = Image(list(patterns_imgs[p].getdata()), patterns_imgs[p].size[1], patterns_imgs[p].size[0])

    start = Vertex('start')
    end = Vertex('end')
    fake_edge = Edge(start, end, Semiring.get_zero())

    min_width = min(patterns[p].width for p in patterns)
    if min_width > image.width:
        return Graph([start, end], fake_edge)

    profile = Profile()
    profile.enable()
    vertices, edges = process_img(image, patterns, start)
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()
    vertices['start'] = [start]
    vertices['end'] = [end]
    if vertices.has_key(image.width):
        edges = edges.union(Edge(v, end, Semiring.get_unity())
                            for v in vertices[image.width])

    problem = DynamicProgramming(sum(vertices.values(), []), edges)
    problem.set_start(start)
    problem.set_finish(end)

    return problem

