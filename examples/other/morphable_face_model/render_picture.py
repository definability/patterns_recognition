from numpy import cross
from numpy.linalg import norm


def project_vector(v, n):
    return v - dot(v, n) * n


def points_center(points):
    return array([p.mean() for p in points.transpose()])


def project_vertices(shp, normal):
    shp_prj = shp.transpose()
    return shp_prj - shp_prj * normal - points_center(shp)


def find_basis(normal):
    k = normal.copy()

    max_value = normal.max()
    j_z = (normal.sum() - max_value) / max_value
    j_norm = (1 + j_z**2)**.5
    j = array([1, 1, j_z]) / j_norm

    i = cross(j, k)

    return array([i, j, k])


def rotate_shape(shape, phi):
    return dot(shape - points_center(shape), phi)


def get_z_index(shape, intensity=255):
    z_index = shape[:,2]
    return z_index * intensity / z_index.max()


def get_projection(shape, max_value):
    shape_prj = shape[:,:2]
    shape_prj = shape_prj - shape_prj.min()
    shape_prj *= 1. * max_value / shape_prj.max()
    return shape_prj


def workflow(normal, image_size=500):
    normal = normal / norm(normal)
    phi = find_basis(normal)
    rotated = rotate_shape(shape, phi)
    shp_prj = get_projection(rotated, image_size - 1)
    z_index = get_z_index(rotated)
    im = Image.new('L', (image_size, image_size))
    shp_prj = shp_prj[z_index.argsort()]
    z_index.sort()
    for i in xrange(shp_prj.shape[0]):
        x = int(shp_prj[i][0])
        y = image_size - 1 - int(shp_prj[i][1])
        im.putpixel((x, y), z_index[i])
    return im

