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
        color = z_index
        try:
            flat = prepare_triangle(canvas, current_vertices[:,:2], color)
        except Exception as e:
            print current_vertices[:,:2]
            raise e


def prepare_triangle(canvas, vertices, color):
    vertices = vertices[vertices[:,1].argsort()[::-1]]
    if int(.5+vertices[1][1]) == int(.5+vertices[2][1]):
        fill_top_flat_triangle(canvas, vertices, color)
    elif int(.5+vertices[0][1]) == int(.5+vertices[1][1]):
        fill_bottom_flat_triangle(canvas, vertices, color)
    else:
        middle = array([vertices[0][0] + ((vertices[1][1] - vertices[0][1]) / (vertices[2][1] - vertices[0][1])) * (vertices[2][0] - vertices[0][0]),
                        vertices[1][1]])
        tf = array([vertices[0], vertices[1], middle])
        bf = array([vertices[1], middle, vertices[2]])
        fill_bottom_flat_triangle(canvas, bf, color)
        fill_top_flat_triangle(canvas, tf, color)


def fill_bottom_flat_triangle(canvas, vertices, color):
    top = vertices[2]
    if vertices[0][0] < vertices[1][0]:
        left, right = vertices[0], vertices[1]
    else:
        left, right = vertices[1], vertices[0]

    invslope1 = (left[0] - top[0]) / (left[1] - top[1])
    invslope2 = (right[0] - top[0]) / (right[1] - top[1])

    curx1 = top[0]
    curx2 = top[0]

    for scanlineY in xrange(int(.5+top[1]), int(.5+left[1]) + 1):
        if abs(curx1 - curx2) > 100:
            print vertices
            print triangle_area(vertices)
        draw_scanline(canvas, scanlineY, curx1, curx2, color)
        curx1 += invslope1
        curx2 += invslope2


def triangle_area(vertices):
    return abs(vertices[0][0] * (vertices[1][1] - vertices[2][1]) +
               vertices[1][0] * (vertices[2][1] - vertices[0][1]) +
               vertices[2][0] * (vertices[0][1] - vertices[1][1])) * .5


def fill_top_flat_triangle(canvas, vertices, color):
    bottom = vertices[0]
    if vertices[1][0] < vertices[2][0]:
        left, right = vertices[1], vertices[2]
    else:
        left, right = vertices[2], vertices[1]

    invslope1 = (left[0] - bottom[0]) / (left[1] - bottom[1])
    invslope2 = (right[0] - bottom[0]) / (right[1] - bottom[1])
  
    curx1 = bottom[0]
    curx2 = bottom[0]
  
    for scanlineY in xrange(int(.5+bottom[1]), int(.5+left[1]) - 1, -1):
        if abs(curx1 - curx2) > 100:
            print vertices
            print triangle_area(vertices)
        draw_scanline(canvas, scanlineY, curx1, curx2, color)
        curx1 -= invslope1
        curx2 -= invslope2


def draw_scanline(canvas, y, left_x, right_x, color):
    for x in xrange(int(.5+left_x), int(.5+right_x) + 1):
        if canvas[y][x] < color:
            canvas[y][x] = color

