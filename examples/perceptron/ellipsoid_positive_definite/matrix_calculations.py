from numpy.linalg import eigvals
from numpy import array

def Y2X_eigenvector(x, y):
    return (0, x**2, x*y, y*x, y**2)

def is_positive_definite(alpha):
    return (eigvals(array(alpha[1:]).reshape(2, 2)) > 0).all()

