from random import randint, random
from math import pi, sin, cos

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse

from classes.solver import Perceptron


X0 = 0
Y0 = 0

LEFT_X = -1
RIGHT_X = 1
LIMITS_X = (LEFT_X, RIGHT_X)

UPPER_Y = 1
BOTTOM_Y = -1
LIMITS_Y = (BOTTOM_Y, UPPER_Y)

fig = plt.figure()

ax = plt.axes(xlim=LIMITS_X, ylim=LIMITS_Y)

a = (random() * 2 + 1) / 4
b = (random() * 2 + 1) / 4
x0 = X0
y0 = Y0
angle = (random() - 0.5) * 2 * pi
w = 2 * a
h = 2 * b

patch = Ellipse((x0, y0), w, h, angle=180*angle/pi, color='r', fill=False)

inside_x_points = []
inside_y_points = []

outside_x_points = []
outside_y_points = []

inside, = ax.plot([], [], 'ro')
outside, = ax.plot([], [], 'bo')
calculated = Ellipse((0, 0), 0, 0, color='b', fill=False)
            
perceptron = Perceptron(5)


def init():
    ax.add_patch(patch)
    ax.add_patch(calculated)
    return calculated, inside, outside


def get_point_projection(new_x, new_y):
    r1 = (new_x * cos(angle) + new_y * sin(angle)) / a
    r2 = (new_x * sin(angle) - new_y * cos(angle)) / b
    return r1**2 + r2**2


def get_point_class(new_x, new_y):
    treshold = .3
    prj = get_point_projection(new_x, new_y)
    if prj < 1 - treshold:
        return -1
    if prj > 1 + treshold:
        return 1
    return 0


def add_new_point(new_x, new_y, x_list, y_list, plot):
    x_list.append(new_x)
    y_list.append(new_y)
    plot.set_data(x_list, y_list)
    #perceptron.setup(left=[Y2X(new_x, new_y)])


def process_perceptron_output():
    alpha = perceptron.alpha
    k = sum((beta**2) / (4 * gamma) for beta, gamma in zip(alpha[1:3], alpha[3:])) - alpha[0]
    prediction = {
        'x': -.5 * alpha[1]/alpha[3],
        'y': -.5 * alpha[2]/alpha[4],
        'a': k/alpha[3],
        'b': k/alpha[4]
    }
    print 'Calculated: x0={}, y0={}, a={}, b={}'.format(prediction['x'], prediction['y'], prediction['a'], prediction['b'])
    print 'Real: x0={}, y0={}, a={}, b={}'.format(x0, y0, a**2, b**2)
    calculated.center = (prediction['x'], prediction['y'])
    calculated.width = 2 * abs(prediction['a'])**.5
    calculated.height = 2 * abs(prediction['b'])**.5


def animate(i):
    new_x = (random() - .5) * 2
    new_y = (random() - .5) * 2

    point_class = get_point_class(new_x, new_y)
    if point_class == -1:
        add_new_point(new_x, new_y, inside_x_points, inside_y_points, inside)
    elif point_class == 1:
        add_new_point(new_x, new_y, outside_x_points, outside_y_points, outside)
    else:
        return calculated, inside, outside
    #process_perceptron_output()

    return calculated, inside, outside

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()

