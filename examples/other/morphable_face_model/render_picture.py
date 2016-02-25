from PIL import Image
from numpy import cross, array, dot
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
    j_z = - (normal.sum() - max_value) / max_value
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


def workflow(points, normal=array([0, 0, 1]), image_size=500):
    normal = normal / norm(normal)
    phi = find_basis(normal)
    rotated = rotate_shape(points, phi)
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


def rasterize_triangles(canvas, vertices, z_indices, colors, triangles):
    for triangle in triangles:
        current_vertices = vertices[triangle]
        z_index = z_indices[triangle].mean()
        color = 255
        try:
            flat = prepare_triangle(current_vertices[:,:2])
        except Exception:
            flat = None
        if len(flat) == 3:
            rasterize_triangle(canvas, flat, z_index, colors)
        elif flat is None:
            continue
        else:
            rasterize_triangle(canvas, flat[0], z_index, color, down=True)
            rasterize_triangle(canvas, flat[1], z_index, color, down=False)


def prepare_triangle(vertices):
    top, left, right = None, None, None
    vertices = vertices[vertices[:,1].argsort()]

    top = vertices[0]
    if vertices[2][0] > vertices[1][0]:
        left, right = vertices[1], vertices[2]
    else:
        left, right = vertices[2], vertices[1]

    if abs(right[1] - left[1]) < 1:
        return top, left, right

    k_left, a_left = get_ka(top, left)
    k_right, a_right = get_ka(top, right)

    middle_left, middle_right, bottom = None, None, None
    if left[1] > right[1]:
        middle_left = left
        middle_right = array([left[0] / k_right - a_right, left[1]])
        bottom = right
    else:
        middle_right = right
        middle_left = array([right[0] / k_left - a_left, right[1]])
        bottom = left

    return [
        [top, middle_left, middle_right],
        [bottom, middle_left, middle_right]
    ]


def get_ka(vertex_start, vertex_end):
    divider = vertex_end[0] - vertex_start[0]
    if abs(divider) < 1E-9:
        return float('inf'), float('inf')
    a = (vertex_end[1] - vertex_start[1]) / divider
    k = vertex_start[0] - a * vertex_start[0]
    return k, a


def rasterize_triangle(canvas, triangle, z_index, color, down=True):
    top, left, right = triangle[0], triangle[1], triangle[2]

    if down:
        top_point = int(top[1])
        down_point = int(left[1])
        k_left, a_left = get_ka(top, left)
        k_right, a_right = get_ka(top, right)
    else:
        return
        top_point = int(left[1])
        down_point = int(top[1])
        if top[1] < right[1]:
            k_left, a_left = get_ka(left, top)
            k_right, a_right = get_ka(left, right)
        else:
            k_left, a_left = get_ka(left, right)
            k_right, a_right = get_ka(left, top)

    for y in xrange(top_point, down_point - 1, -1):
        for x in xrange(int((y-a_left)/k_left), int((y-a_right)/k_right + 1)):
            try:
                if canvas[x][y] is None or canvas[x][y][1] < z_index:
                    canvas[x][y] = (color, z_index)
            except Exception as e:
                print 'From {fr} to {to}, down is {down}'.format(
                        fr=(top_point, int(y/k_left - a_left)),
                        to=(down_point-1, int(y/k_right - a_right + 1)),
                        down=down)
                print 'x, y are {coord}, k={k}, a={a}'.format(
                        coord=(x,y), k=(k_left, k_right),
                        a=(a_left, a_right))
                break

