from load_model import *
from render_triangle import rasterize_triangles
from numpy import empty

from PIL import Image
from numpy import cross, array, dot
from numpy.linalg import norm


model = load_model()

coorinates = model['shapeMU']
points = coorinates.reshape(coorinates.shape[0]/3, 3)

rasterize_triangles(points, model['tl'] - 1)

