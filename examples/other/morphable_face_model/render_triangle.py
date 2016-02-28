from numpy import array
import ctypes

lib = ctypes.cdll.LoadLibrary('./lib_draw_line.so')

def rasterize_triangles(canvas, vertices, z_indices, colors, triangles):
    canvas_width = canvas.shape[1]
    canvas = canvas.ctypes.get_as_parameter()
    for triangle in triangles:
        current_vertices = vertices[triangle]
        color = z_indices[triangle].mean()
        lib.prepare_triangle(canvas, current_vertices.ctypes.get_as_parameter(),
                             int(color), canvas_width)

