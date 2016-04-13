from numpy import array, arctan, cos, sin

def Y2X_ellipsoid(x, y):
    return (1, x**2, x*y, y*x, y**2)

def get_ellipse(alpha):
    alpha = array(alpha)/alpha[0]
    x = alpha[1]
    xy = alpha[2] + alpha[3]
    y = alpha[4]

    tg_double_angle = xy / (x - y)
    double_angle = arctan(tg_double_angle)

    c_dividend = (x + y) * cos(double_angle) + (x - y)
    c_divisor = (x + y) * cos(double_angle) - (x - y)
    c = c_dividend / c_divisor

    a = abs((sin(double_angle) * (c - 1)) / (c * xy))**.5
    b = a * c

    return (a, b, double_angle/2)

