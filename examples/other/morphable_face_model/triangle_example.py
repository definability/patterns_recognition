from load_model import *
from render_triangle import rasterize_triangles

from PIL import Image
from numpy import array

from calculations import get_normals, set_light, get_normal_map

from cProfile import Profile
from pstats import Stats

profile = Profile()
profile.enable()

model = load_model()

coorinates = model['shapeMU']
points = coorinates.reshape(coorinates.shape[0]/3, 3)
triangles = model['tl'] - 1

normals = get_normals(points, triangles)
light_direction = array([-1, 0, -1])/(2**.5)
lights = set_light(normals, light_direction).astype('f')
normal_map = get_normal_map(normals).astype('f')

profile.disable()
Stats(profile).sort_stats('tottime').print_stats()

colors = normal_map
rasterize_triangles(points, triangles.flatten(), colors)

