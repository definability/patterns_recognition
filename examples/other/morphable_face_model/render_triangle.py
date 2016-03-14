from numpy import array, column_stack
import ctypes

render_face = ctypes.cdll.LoadLibrary('./lib_render_face.so')

def rasterize_triangles(vertices, triangles):
    v = vertices[triangles]
    v /= max(v.max(), -v.min())
    print len(v), v.size, v.shape, triangles.max()*3+2
    #amount = triangles.size
    amount = 3 * len(v)
    render_face.render_face(v.ctypes.get_as_parameter(), triangles.ctypes.get_as_parameter(), amount)

