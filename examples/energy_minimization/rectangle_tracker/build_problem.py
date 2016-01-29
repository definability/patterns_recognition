from math import sqrt

from classes.image import MatrixPointer
from classes.solver import EnergyMinimization
from classes.graph import *

from cProfile import Profile
from pstats import Stats


def build_problem(model_image, raw_image, model_image_mask=None):
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
    vertices, edges = process_image(model, raw, mask)
    profile.disable()
    Stats(profile).sort_stats('time').print_stats()
    problem = EnergyMinimization(vertices, edges)
    return problem


def process_image(model, raw, mask):
    vertices = list()
    edges = list()
    domains = dict()

    for i in xrange(model.get_size()[0]):
        for j in xrange(model.get_size()[1]):
            if not mask[i,j]:
                continue
            domains[(i,j)] = create_vertices((i,j), raw, model)
            vertices.extend(domains[(i,j)].values())

    for domain in domains:
        neighbours = get_neighbours(model, domain, mask)
        for pixel in domains[domain]:
            vertex = domains[domain][pixel]
            for neighbour_domain in neighbours:
                process_domain(model, raw, neighbour_domain,
                               vertex, pixel, domains, vertices, edges)

    return (set(vertices), set(edges))


def process_domain(model, raw, domain, start, pixel, domains, vertices, edges):
    needed_offset = (domain[0] - start.get_domain()[0],
                     domain[1] - start.get_domain()[1])
    start_pos = start.get_name()
    max_i, max_j = raw.get_size()
    for i in xrange(pixel[0], max_i):
        for j in xrange(pixel[1], max_j):
            end_pos = (i,j)
            process_end(edges, start, domains[domain][end_pos],
                        start_pos, end_pos, needed_offset)


def process_end(edges, start, end, start_pos, end_pos, needed_offset):
    real_offset = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    edge_penalty = get_distance_penalty(needed_offset, real_offset)
    edge = Edge(start, end, edge_penalty)
    edges.append(edge)


def create_vertices(domain, raw, model):
    return dict(((i,j), Vertex((i,j),
                        get_value_penalty(model[domain], raw[i,j]), domain))
               for i in xrange(raw.get_size()[0])
               for j in xrange(raw.get_size()[1]))


def get_neighbours(model, pos, mask):
    max_y, max_x = model.get_size()
    neighbours = [(pos[0] + 1, pos[1]), (pos[0], pos[1] + 1)]
    return [r for r in neighbours if r[0] < max_y and r[1] < max_x and mask[r]]


def get_distance_penalty(needed_offset, real_offset):
    return - ((needed_offset[0] - real_offset[0])**2
           +  (needed_offset[1] - real_offset[1])**2)


def get_value_penalty(needed_value, real_value):
    return - (needed_value - real_value)**2

