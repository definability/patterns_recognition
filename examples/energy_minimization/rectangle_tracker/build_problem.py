from math import sqrt

from classes.image import MatrixPointer
from classes.solver import EnergyMinimization
from classes.graph import *

from cProfile import Profile
from pstats import Stats


def get_penalty(model, raw, index_model, index_raw, prev_offset):
    distance = sqrt((index_model[0] + prev_offset[0] - index_raw[0])**2 +
                    (index_model[1] + prev_offset[1] - index_raw[1])**2)
    return - (model[index_model] - raw[index_raw])**2 - distance * 10


def process_image(model, raw, mask):
    to_visit = [{
        'target': (0,0),
        'penalties': dict(((i,j), Vertex((i,j), 0, (0,0)))
                          for i in xrange(raw.get_size()[0])
                          for j in xrange(raw.get_size()[1]))
    }]

    vertices = set(to_visit[0]['penalties'].values())
    edges = set()
    domains = dict()
    eds = set()

    while True:
        if len(to_visit) == 0:
            break
        current_pixel = to_visit.pop()

        for pixel in current_pixel['penalties']:
            offset = (pixel[0] - current_pixel['target'][0],
                      pixel[1] - current_pixel['target'][1])
            v = Vertex(offset, current_pixel['penalties'][pixel],
                               current_pixel['target'])
            neighbours = []
            if current_pixel['target'][0] < model.get_size()[0] - 1 \
                    and mask[current_pixel['target'][0] + 1,
                             current_pixel['target'][1]]:
                neighbours.append((current_pixel['target'][0] + 1,
                                   current_pixel['target'][1]))
            if current_pixel['target'][1] < model.get_size()[1] - 1 \
                    and mask[current_pixel['target'][0],
                             current_pixel['target'][1] + 1]:
                neighbours.append((current_pixel['target'][0],
                                   current_pixel['target'][1] + 1))
            for n in neighbours:
                penalties = dict()
                for i in xrange(pixel[0], raw.get_size()[0]):
                    for j in xrange(pixel[1], raw.get_size()[1]):
                        v = None
                        if n not in domains:
                            domains[n] = dict()
                        if (i,j) not in domains[n]:
                            domains[n][(i,j)] = Vertex((i,j), 0, n)
                            vertices.add(domains[n][(i,j)])
                        v = domains[n][(i,j)]
                        penalty = get_penalty(model, raw, n, (i,j), offset)
                        penalties[(i,j)] = v
                        if (current_pixel['penalties'][pixel],v) not in eds:
                            edge = Edge(current_pixel['penalties'][pixel], v, penalty)
                            edges.add(edge)
                            eds.add((current_pixel['penalties'][pixel],v))
                to_visit.append({
                    'target': n,
                    'penalties': penalties
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

