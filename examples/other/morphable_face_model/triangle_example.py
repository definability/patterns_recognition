from load_model import *
from render_picture import *
from numpy import empty
from cProfile import Profile
from pstats import Stats

from PIL import Image
from numpy import cross, array, dot
from numpy.linalg import norm


model = load_model()

coorinates = model['shapeMU']
points = coorinates.reshape(coorinates.shape[0]/3, 3)


normal = array([0, 0, 1])
image_size = 2000
normal = normal / norm(normal)
phi = find_basis(normal)
rotated = rotate_shape(points, phi)
shp_prj = get_projection(rotated, image_size - 20)
z_index = get_z_index(rotated)
#im = Image.new('L', (image_size, image_size))
#for i in xrange(shp_prj.shape[0]):
#    x = int(shp_prj[i][0])
#    y = image_size - 1 - int(shp_prj[i][1])
#    im.putpixel((x, y), z_index[i])


#canvas = empty((image_size, image_size))
canvas = array([[0]*image_size for i in xrange(image_size)], dtype='d')
#canvas = [[0]*image_size for i in xrange(image_size)]
print 'Start'
profile = Profile()
profile.enable()
rasterize_triangles(canvas, shp_prj, z_index, [], model['tl'] - 1)
profile.disable()
im = Image.new('L', (image_size, image_size))
for y in xrange(len(canvas)):
    for x in xrange(len(canvas[i])):
        if canvas[y][x] is None:
            continue
        #print (i,j), canvas[i][j]
        im.putpixel((x,y), int(canvas[y][x]))
im.save('out.png')
Stats(profile).sort_stats('time').print_stats()

