from numpy import array
import ctypes

lib = ctypes.cdll.LoadLibrary('./lib_draw_line.so')

def rasterize_triangles(canvas, vertices, z_indices, colors, triangles):
    for triangle in triangles:
        current_vertices = vertices[triangle]
        z_index = z_indices[triangle].mean()
        color = z_index
        prepare_triangle(canvas, current_vertices[:,:2], color)


def prepare_triangle(canvas, vertices, color):
    vertices = vertices[vertices[:,1].argsort()[::-1]]
    lib.prepare_triangle(canvas.ctypes.get_as_parameter(),
                vertices.ctypes.get_as_parameter(), int(color), canvas.shape[1])

