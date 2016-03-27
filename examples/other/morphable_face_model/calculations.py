from numpy import array, cross, dot
from numpy.linalg import norm

def get_neighbours(vertices_amount, triangles):
    result = [[] for i in xrange(vertices_amount)]
    for triangle, vertices in enumerate(triangles):
        for v in vertices:
            result[v].append(triangle)
    return [array(r) for r in result]

def get_normal(a, b):
    result = cross(a, b)
    return result / norm(result)

def get_normals(points, triangles):
    vertices = points[triangles]
    first_edges = vertices[:,1] - vertices[:,0]
    second_edges = vertices[:,2] - vertices[:,0]
    normals = array([get_normal(f, s) for f, s in zip(first_edges, second_edges)])
    return [sum(normals[neighbours]) / len(neighbours)
        for neighbours in get_neighbours(len(points), triangles)]

def set_light(normals, n):
    result = dot(normals, n)
    result -= result.min()
    result /= result.max()
    return result

