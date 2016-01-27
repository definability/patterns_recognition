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
                        penalty = get_penalty(model, raw, n, (i,j), offset)
                        v = Vertex((i,j), 0, n)
                        penalties[(i,j)] = v
                        vertices.add(v)
                        edges.add(Edge(current_pixel['penalties'][pixel], v, penalty))
                to_visit.append({
                    'target': n,
                    'penalties': penalties
                })

    print 'Original', len(vertices), len(edges)
    result = dict()
    domains = dict()
    verts = dict()
    to_remove = set()
    for e in edges:
        x, y = e.get_vertices()
        if x.get_domain() not in domains:
            domains[x.get_domain()] = list()
        if y.get_domain() not in domains:
            domains[y.get_domain()] = list()
        domains[x.get_domain()].append(x.get_name())
        domains[y.get_domain()].append(y.get_name())
        x_coord = (x.get_name(), x.get_domain())
        y_coord = (y.get_name(), y.get_domain())
        if x_coord not in verts:
            verts[x_coord] = list()
        if y_coord not in verts:
            verts[y_coord] = list()
        verts[x_coord].append(x.get_value())
        verts[y_coord].append(y.get_value())
        result[(x_coord, y_coord)] = e.get_value()
    print sum(len(set(domains[d])) for d in domains)
    vertices = set()
    edges = set()
    eds = dict()
    for d in domains:
        for v in set(domains[d]):
            if (v,d) in eds:
                print 'Conflict'
            vertex = Vertex(v, 0, d)
            vertices.add(vertex)
            eds[(v,d)] = vertex
    for r in result:
        edges.add(Edge(eds[r[0]], eds[r[1]], result[r]))
    print len(vertices), len(edges)
    #edges = edges.difference(to_remove)
    #print 'Edges', len(result), len(set(result))
    #for v in verts:
    #    i = verts[v][0]
    #    for a in verts[v]:
    #        if a != i:
    #            print a, i
    #print 'Vertices', len(vertices), len(set(verts))
    #for d in domains:
    #    print '"' + str(d) + '": ["' + '","'.join(str(a) for a in domains[d]) + '"],'
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

