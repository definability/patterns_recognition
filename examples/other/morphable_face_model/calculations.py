from numpy import array, cross, dot, apply_along_axis
from numpy.linalg import norm
from numpy import min as np_min, max as np_max

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
    normals = array([normal_vectors[neighbours].sum(axis=0)
                    for neighbours in neighbour_triangles])
    lengths = apply_along_axis(norm, 1, normals)
    return normals / lengths[:,None]

def set_light(normals, n):
    result = dot(normals, n)
    result -= result.min()
    result /= result.max()
    return result

def get_normal_map(normals):
    result = normals - apply_along_axis(np_min, 0, normals)
    return result / apply_along_axis(np_max, 0, result)

