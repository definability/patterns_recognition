from math import sqrt

from classes.image import MatrixPointer
from classes.solver import EnergyMinimization
from classes.graph import *

from cProfile import Profile
from pstats import Stats


def get_penalty(model, raw, index_model, index_raw, prev_offset):
    deviation = (model[index_model] - raw[index_raw])**2
    distance = ((index_model[0] + prev_offset[0] - index_raw[0])**2 +
                (index_model[1] + prev_offset[1] - index_raw[1])**2)
    return - (deviation + distance)


def get_neighbours(model, pos, mask):
    max_y, max_x = model.get_size()
    neighbours = [(pos[0] + 1, pos[1]), (pos[0], pos[1] + 1)]
    return [r for r in neighbours if r[0] < max_y and r[1] < max_x and mask[r]]


def process_domain(model, raw, domain, vertex, pixel, offset,
                               domains, vertices, edges, links):
    penalties = dict()
    if domain not in domains:
        domains[domain] = dict()
    for i in xrange(pixel[0], raw.get_size()[0]):
        for j in xrange(pixel[1], raw.get_size()[1]):
            if (i,j) not in domains[domain]:
                domains[domain][(i,j)] = Vertex((i,j), 0, domain)
                vertices.add(domains[domain][(i,j)])
            end = domains[domain][(i,j)]
            penalty = get_penalty(model, raw, domain, (i,j), offset)
            penalties[(i,j)] = end
            if (vertex,end) not in links:
                edge = Edge(vertex, end, penalty)
                edges.add(edge)
                links.add((vertex,end))
    return penalties


def process_image(model, raw, mask):
    to_visit = [{
        'domain': (0,0),
        'lables': dict(((i,j), Vertex((i,j), 0, (0,0)))
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

