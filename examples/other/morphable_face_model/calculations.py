from numpy import array, cross, dot, apply_along_axis
from numpy.linalg import norm

def get_neighbours(vertices_amount, triangles):
    result = [[] for i in xrange(vertices_amount)]
    for triangle, vertices in enumerate(triangles):
        for v in vertices:
            result[v].append(triangle)
    return [array(r) for r in result]

def get_normals(points, triangles, neighbour_triangles):
    vertices = points[triangles]
    first_edges = vertices[:,1] - vertices[:,0]
    second_edges = vertices[:,2] - vertices[:,0]
    normal_vectors = cross(first_edges, second_edges)
    normals = array([sum(normal_vectors[neighbours])
                    for neighbours in get_neighbours(len(points), triangles)])
    lengths = apply_along_axis(norm, 1, normals)
    return normals / lengths[:,None]

def set_light(normals, n):
    result = dot(normals, n)
    result -= result.min()
    result /= result.max()
    return result

