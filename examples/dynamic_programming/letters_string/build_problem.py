from classes.semiring import *
from classes.graph import *
from classes.image import *
from classes.solver import *

from cProfile import Profile
from pstats import Stats


def process_img(img, patterns, previous_vertex, offset=0, vertices=None, edges=None):

    if vertices is None:
        vertices = dict()
    if edges is None:
        edges = set()
    keys = set()

    for p in patterns:

        if patterns[p].get_size()[0] > img.get_size()[0]:
            continue


        current_key = offset+patterns[p].get_size()[0]
        current_vertex = None

        if current_key in vertices:
            for vertex in vertices[current_key]:
                if vertex.get_name() == p:
                    current_vertex = vertex
                    break
        else:
            vertices[current_key] = [Vertex('', (0, []))]

        if current_key not in keys:
            keys.add(current_key)
            edges.add(Edge(previous_vertex, vertices[current_key][0], (0, [])))

        if current_vertex is not None:
            continue

        img_left, img_right = img.split_vertical(patterns[p].get_size()[0])
        sigma = img_left.reduce(lambda accumulator, x, y: accumulator + (x - y)**2, 0, patterns[p])
        current_vertex = Vertex(p, (sigma, p))

        vertices[current_key].append(current_vertex)

        edges.add(Edge(vertices[current_key][0], current_vertex, (0, [])))

        process_img(img_right, patterns, current_vertex, offset+patterns[p].get_size()[0], vertices, edges)

    return vertices, edges


def build_problem(main_img, patterns_imgs, Semiring=SemiringArgminPlusElement):

    image = MatrixPointer(list(main_img.getdata()), (main_img.size[0], main_img.size[1]))
    patterns = dict()
    for p in patterns_imgs:
        patterns[p] = MatrixPointer(list(patterns_imgs[p].getdata()), (patterns_imgs[p].size[0], patterns_imgs[p].size[1]))

    start = Vertex('start')
    end = Vertex('end')
    fake_edge = Edge(start, end, Semiring.get_zero())

    min_width = min(patterns[p].get_size()[0] for p in patterns)
    if min_width > image.get_size()[0]:
        return Graph([start, end], fake_edge)

    profile = Profile()
    profile.enable()
    vertices, edges = process_img(image, patterns, start)
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()
    vertices['start'] = [start]
    vertices['end'] = [end]
    if vertices.has_key(image.get_size()[0]):
        edges = edges.union(Edge(v, end, Semiring.get_unity())
                            for v in vertices[image.get_size()[0]])

    problem = DynamicProgramming(sum(vertices.values(), []), edges)
    problem.set_start(start)
    problem.set_finish(end)

    return problem

