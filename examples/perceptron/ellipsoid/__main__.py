from random import randint, random

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse

from classes.solver import Perceptron

fig = plt.figure()

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

a = random() * 2 + 1
b = random() * 2 + 1
w = 2 * a
h = 2 * b
x0 = random() * 5 + 3
y0 = random() * 5 + 3
patch = Ellipse((x0, y0), w, h, color='r', fill=False)

inside_x_points = []
inside_y_points = []

outside_x_points = []
outside_y_points = []

inside, = ax.plot([], [], 'ro')
outside, = ax.plot([], [], 'bo')
calculated = Ellipse((0, 0), 0, 0, color='b', fill=False)

perceptron = Perceptron(5)

def Y2X(x, y):
    return (1, x, y, x**2, y**2)

def init():
    patch.center = (x0, y0)
    ax.add_patch(patch)
    ax.add_patch(calculated)
    return calculated, inside, outside

def animate(i):
    new_x = random() * 10
    new_y = random() * 10

    if ((new_x - x0)/a)**2 + ((new_y - y0)/b)**2 < .7:
        inside_x_points.append(new_x)
        inside_y_points.append(new_y)
        inside.set_data(inside_x_points, inside_y_points)
        perceptron.setup(left=[Y2X(new_x, new_y)])
    if ((new_x - x0)/a)**2 + ((new_y - y0)/b)**2 > 1.3:
        outside_x_points.append(new_x)
        outside_y_points.append(new_y)
        outside.set_data(outside_x_points, outside_y_points)
        perceptron.setup(right=[Y2X(new_x, new_y)])

    alpha = perceptron.alpha
    k = sum((beta**2) / (4 * gamma) for beta, gamma in zip(alpha[1:3], alpha[3:])) - alpha[0]
    prediction = {
        'x': -.5 * alpha[1]/alpha[3],
        'y': -.5 * alpha[2]/alpha[4],
        'a': k/alpha[3],
        'b': k/alpha[4]
    }
    #pring 'Calculated: x0={}, y0={}, a={}, b={}'.format(prediction['x'], prediction['y'], prediction['a'], prediction['b'])
    #pring 'Real: x0={}, y0={}, a={}, b={}'.format(x0, y0, a**2, b**2)
    calculated.center = (prediction['x'], prediction['y'])
    calculated.width = 2 * abs(prediction['a'])**.5
    calculated.height = 2 * abs(prediction['b'])**.5

    return calculated, inside, outside

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=360,
                               interval=200,
                               blit=True)

plt.show()

