from numpy import array
import ctypes

lib = ctypes.cdll.LoadLibrary('./lib_draw_line.so')
draw_scanline = lib.draw_scanline

def rasterize_triangles(canvas, vertices, z_indices, colors, triangles):
    for triangle in triangles:
        current_vertices = vertices[triangle]
        z_index = z_indices[triangle].mean()
        color = z_index
        prepare_triangle(canvas, current_vertices[:,:2], color)


def prepare_triangle(canvas, vertices, color):
    vertices = vertices[vertices[:,1].argsort()[::-1]]
    if int(.5+vertices[1][1]) == int(.5+vertices[2][1]):
        lib.fill_top_flat_triangle(canvas.ctypes.get_as_parameter(),
                vertices.ctypes.get_as_parameter(), int(color), canvas.shape[1])
    elif int(.5+vertices[0][1]) == int(.5+vertices[1][1]):
        lib.fill_bottom_flat_triangle(canvas.ctypes.get_as_parameter(),
                vertices.ctypes.get_as_parameter(), int(color), canvas.shape[1])
    else:
        middle = array([vertices[0][0] + ((vertices[1][1] - vertices[0][1])
                                        / (vertices[2][1] - vertices[0][1]))
                                        * (vertices[2][0] - vertices[0][0]),
                        vertices[1][1]])
        tf = array([vertices[0], vertices[1], middle])
        bf = array([vertices[1], middle, vertices[2]])
        lib.fill_bottom_flat_triangle(canvas.ctypes.get_as_parameter(),
                bf.ctypes.get_as_parameter(), int(color), canvas.shape[1])
        lib.fill_top_flat_triangle(canvas.ctypes.get_as_parameter(),
                tf.ctypes.get_as_parameter(), int(color), canvas.shape[1])

