from math import sqrt

from classes.image import MatrixPointer
from classes.solver import EnergyMinimization
from classes.graph import *

from cProfile import Profile
from pstats import Stats


def get_distance_penalty(needed_offset, real_offset):
    return - ((needed_offset[0] - real_offset[0])**2
           +  (needed_offset[1] - real_offset[1])**2)


def get_value_penalty(needed_value, real_value):
    return - (needed_value - real_value)**2


def get_neighbours(model, pos, mask):
    max_y, max_x = model.get_size()
    neighbours = [(pos[0] + 1, pos[1]), (pos[0], pos[1] + 1)]
    return [r for r in neighbours if r[0] < max_y and r[1] < max_x and mask[r]]


def process_domain(model, raw, domain, vertex, pixel, offset,
                               domains, vertices, edges, links):
    penalties = dict()
    if domain not in domains:
        domains[domain] = dict()
    needed_offset = (domain[0] - vertex.get_domain()[0],
                     domain[1] - vertex.get_domain()[1])
    start = vertex.get_name()
    end = None
    max_i, max_j = raw.get_size()
    for i in xrange(pixel[0], max_i):
        for j in xrange(pixel[1], max_j):
            if (i,j) not in domains[domain]:
                vertex_penalty = get_value_penalty(model[domain], raw[i,j])
                end = Vertex((i,j), vertex_penalty, domain)
                domains[domain][(i,j)] = end
                vertices.add(end)
            else:
                end = domains[domain][(i,j)]
            penalties[(i,j)] = end
            real_offset = (i - start[0], j - start[1])
            if (vertex,end) not in links:
                edge_penalty = get_distance_penalty(needed_offset, real_offset)
                edge = Edge(vertex, end, edge_penalty)
                edges.add(edge)
                links.add((vertex,end))
    return penalties


def process_image(model, raw, mask):
    to_visit = [{
        'domain': (0,0),
        'lables': dict(((i,j), Vertex((i,j), -(model[0,0]-raw[i,j])**2, (0,0)))
                          for i in xrange(raw.get_size()[0])
                          for j in xrange(raw.get_size()[1]))
    }]

    vertices = set(to_visit[0]['lables'].values())
    edges = set()
    domains = dict()
    links = set()

    while True:
        if len(to_visit) == 0:
            break
        current_pixel = to_visit.pop()
        domain = current_pixel['domain']
        neighbours = get_neighbours(model, domain, mask)
        for pixel in current_pixel['lables']:
            vertex = current_pixel['lables'][pixel]
            offset = (pixel[0] - domain[0], pixel[1] - domain[1])
            for neighbour_domain in neighbours:
                to_visit.append({
                    'domain': neighbour_domain,
                    'lables': process_domain(model, raw, neighbour_domain,
                        vertex, pixel, offset, domains, vertices, edges, links)
                })

    return (vertices, edges)


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

