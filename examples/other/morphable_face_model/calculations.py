from numpy import array, cross, dot
from numpy.linalg import norm

def get_neighbours(vertices_amount, triangles):
    result = [[] for i in xrange(vertices_amount)]
    for tr in triangles:
        for v in tr:
            result[v].append(tr)
    return [array(r) for r in result]

def get_normal(triangle):
    a = (triangle[1] - triangle[0]).astype('d')
    b = (triangle[2] - triangle[0]).astype('d')
    result = cross(a, b)
    return result / norm(result)

def get_normals(points, triangles):
    return [sum(get_normal(triangle)
        for triangle in points[neighbours]) / len(neighbours)
        for neighbours in get_neighbours(len(points), triangles)]

def set_light(normals, n):
    result = dot(normals, n)
    result -= result.min()
    result /= result.max()
    return result

