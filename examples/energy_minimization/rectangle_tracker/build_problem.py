from math import sqrt

from classes.image import MatrixPointer
from classes.solver import EnergyMinimization
from classes.graph import *

from cProfile import Profile
from pstats import Stats


def build_problem(model_image, raw_image, model_image_mask=None,
        max_vertical_offset=float('inf'), max_horizontal_offset=float('inf')):
    if model_image_mask is None:
        model_image_mask = [True] * len(model_image.getdata())
    model = MatrixPointer(list(model_image.getdata()),
                         (model_image.size[0], model_image.size[1]))
    mask  = MatrixPointer(model_image_mask,
                         (model_image.size[0], model_image.size[1]))
    raw   = MatrixPointer(list(raw_image.getdata()),
                         (raw_image.size[0], raw_image.size[1]))
    profile = Profile()
    profile.enable()
    vertices, edges = process_image(model, raw, mask, max_vertical_offset,
                                    max_horizontal_offset)
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()
    problem = EnergyMinimization(vertices, edges)
    return problem


def process_image(model, raw, mask, max_vertical_offset, max_horizontal_offset):
    vertices = list()
    edges = list()
    domains = dict()

    raw_size = raw.get_size()
    for i in xrange(model.get_size()[0]):
        for j in xrange(model.get_size()[1]):
            if not mask[i,j]:
                continue
            vertical_from = max(0, i - max_vertical_offset)
            horizontal_from = max(0, j - max_horizontal_offset)
            vertical_to = min(raw_size[0], i + max_vertical_offset + 1)
            horizontal_to = min(raw_size[1], j + max_horizontal_offset + 1)
            domains[(i,j)] = create_vertices((i,j), raw, model,
                    xrange(vertical_from, vertical_to),
                    xrange(horizontal_from, horizontal_to))
            vertices += domains[(i,j)].values()

    for domain in domains:
        neighbours = get_neighbours(model, domain, mask)
        for pixel in domains[domain]:
            vertex = domains[domain][pixel]
            vertex_pos = vertex.get_name()
            for neighbour_info in neighbours:
                neighbour_domain = neighbour_info[0]
                vertical_range, horizontal_range  = neighbour_info[1](
                        vertex_pos[0], vertex_pos[1],
                        max_vertical_offset, max_horizontal_offset,
                        raw_size[0], raw_size[1])
                process_domain(model, raw, neighbour_domain, vertex, pixel,
                               domains, vertices, edges,
                               vertical_range, horizontal_range)

    return (set(vertices), set(edges))


def process_domain(model, raw, domain, start, pixel, domains, vertices, edges,
        vertical_range, horizontal_range):
    needed_offset = (domain[0] - start.get_domain()[0],
                     domain[1] - start.get_domain()[1])
    start_pos = start.get_name()
    for i in vertical_range:
        for j in horizontal_range:
            end_pos = (i,j)
            if end_pos not in domains[domain]:
                continue
            process_end(edges, start, domains[domain][end_pos],
                        start_pos, end_pos, needed_offset)


def process_end(edges, start, end, start_pos, end_pos, needed_offset):
    real_offset = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    edge_penalty = get_distance_penalty(needed_offset, real_offset)
    edge = Edge(start, end, edge_penalty)
    edges.append(edge)


def create_vertices(domain, raw, model, vertical_range, horizontal_range):
    return dict(((i,j), Vertex((i,j),
                        get_value_penalty(model[domain], raw[i,j]), domain))
               for i in vertical_range
               for j in horizontal_range)


def get_neighbours(model, pos, mask):
    max_y, max_x = model.get_size()
    neighbours = [((pos[0] + 1, pos[1]), get_bottom_neighbours),
                  ((pos[0], pos[1] + 1), get_right_neighbours)]
    return [r for r in neighbours
            if r[0][0] < max_y
            and r[0][1] < max_x
            and mask[r[0]]]


def get_right_neighbours(i, j, max_vertical_offset, max_horizontal_offset,
                         height, width):
    return (xrange(max(i - max_vertical_offset, 0),
                   min(i + max_vertical_offset + 1, height)),
            xrange(j,
                   min(j + max_horizontal_offset + 1, width)))


def get_bottom_neighbours(i, j, max_vertical_offset, max_horizontal_offset,
                          height, width):
    return (xrange(i,
                   min(i + max_vertical_offset + 1, height)),
            xrange(max(j - max_horizontal_offset, 0),
                   min(j + max_horizontal_offset + 1, width)))


def get_distance_penalty(needed_offset, real_offset):
    return - ((needed_offset[0] - real_offset[0])**2
           +  (needed_offset[1] - real_offset[1])**2)


def get_value_penalty(needed_value, real_value):
    return - (needed_value - real_value)**2

