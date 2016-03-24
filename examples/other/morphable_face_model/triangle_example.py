from load_model import *
from render_triangle import rasterize_triangles

from PIL import Image
from numpy import array

from calculations import get_normals, set_light

model = load_model()

coorinates = model['shapeMU']
points = coorinates.reshape(coorinates.shape[0]/3, 3)
triangles = model['tl'] - 1

normals = get_normals(points, triangles)
light_direction = array([-1, 0, -1])/(2**.5)
lights = set_light(normals, light_direction).astype('f')
rasterize_triangles(points, triangles.flatten(), lights)

