from random import randint, random
from math import pi, sin, cos

from numpy import array, linspace, ones
from numpy.random import rand as random_matrix
from matplotlib import pyplot as plt
from matplotlib import animation

from classes.solver import Perceptron


LEFT_X = -2
RIGHT_X = 2
LIMITS_X = (LEFT_X, RIGHT_X)

UPPER_Y = 2
BOTTOM_Y = -2
LIMITS_Y = (BOTTOM_Y, UPPER_Y)

RESOLUTION = 100

POLY_ORDER = 3

fig = plt.figure()

ax = plt.axes(xlim=LIMITS_X, ylim=LIMITS_Y)

inside_x_points = []
inside_y_points = []

outside_x_points = []
outside_y_points = []

A = random_matrix(POLY_ORDER*2, POLY_ORDER*2) - .5

def get_poly(x):
    return ([1] + [x**i for i in xrange(1, POLY_ORDER)])[::-1]

def get_vector(x, y):
    return array(get_poly(x) + get_poly(y))

def get_eq(x, y, A):
    v = get_vector(x, y)
    return v.dot(A).dot(v)

inside, = ax.plot([], [], 'ro')
outside, = ax.plot([], [], 'bo')
perceptron = Perceptron((POLY_ORDER*2)**2)
x = linspace(LEFT_X, RIGHT_X, RESOLUTION)
y = linspace(BOTTOM_Y, UPPER_Y, RESOLUTION)
plt.contour(x, y[:,None].ravel(), get_eq(x, y[:,None], A), [0], colors='r')

def init():
    #ax.add_patch(patch)
    #ax.add_patch(calculated)
    return inside, outside


def get_point_projection(new_x, new_y):
    return get_eq(array([new_x]), array([new_y]), A)


def get_point_class(new_x, new_y):
    treshold = .1
    prj = get_point_projection(new_x, new_y)
    if prj < -treshold:
        return -1
    if prj > treshold:
        return 1
    return 0


def add_new_point(new_x, new_y, x_list, y_list, plot, side):
    x_list.append(new_x)
    y_list.append(new_y)
    plot.set_data(x_list, y_list)
    v = get_vector(new_x, new_y)
    points = (v * ones((POLY_ORDER*2, POLY_ORDER*2)) * v[:,None]).flatten().tolist()
    if side == -1:
        perceptron.setup(left=[points])
    if side == 1:
        perceptron.setup(right=[points])

def process_perceptron_output(previous_data):
    try:
        data = perceptron.alpha
    except:
        return previous_data
    if previous_data == data:
        return previous_data
    print 'Calculated data={}'.format(data)
    print 'Real data={}'.format(A)
    #print 'Calculated: a={}, b={}, angle={}'.format(*data)
    #print 'Real: a={}, b={}, angle={}'.format(a, b, angle)
    #calculated.center = (X0, Y0)
    #calculated.width = 2 * data[0]
    #calculated.height = 2 * data[1]
    #calculated.angle = 180 * data[2] / pi
    return data

perceptron_output = {
    'data': None
}
def animate(i):
    new_x = (random() - .5) * 4
    new_y = (random() - .5) * 4

    point_class = get_point_class(new_x, new_y)
    if point_class == -1:
        add_new_point(new_x, new_y, inside_x_points, inside_y_points, inside, -1)
    elif point_class == 1:
        add_new_point(new_x, new_y, outside_x_points, outside_y_points, outside, 1)
    else:
        return inside, outside
    if len(inside_x_points) == 0 or len(outside_x_points) == 0:
        return inside, outside

    perceptron_output['data'] = process_perceptron_output(perceptron_output['data'])

    new_A = array(perceptron_output['data']).reshape(POLY_ORDER*2, POLY_ORDER*2)
    plt.gca().clear()
    plt.contour(x, y[:,None].ravel(), get_eq(x, y[:,None], A), [0], colors='r')
    plt.contour(x, y[:,None].ravel(), get_eq(x, y[:,None], new_A), [0], colors='b')
    ax.plot(inside_x_points, inside_y_points, 'ro')
    ax.plot(outside_x_points, outside_y_points, 'bo')
    plt.draw()
    return inside, outside

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=360,
                               interval=200,
                               blit=True)

plt.show()

