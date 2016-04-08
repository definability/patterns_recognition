from numpy import array, column_stack
from numpy.linalg import norm

def find_wrong(alpha, r, points):
    alpha = array(alpha)
    alpha /= norm(alpha)
    points = array(points)
    signs = points.dot(alpha.transpose())
    signs = column_stack(array([signs/abs(signs)]*len(alpha)))
    opposites = (points - signs * r * alpha).dot(alpha.transpose())
    wrong = (points.dot(alpha.transpose()) * opposites < 0)
    if points[wrong].size == 0:
        return None
    print points[wrong][0].dot(alpha), (points - signs * r * alpha)[wrong][0].dot(alpha)
    return (points - signs * r * alpha)[wrong][0]

def get_correction_point(alpha, r, points):
    nearest = find_wrong(alpha, r, points)
    if nearest is None:
        return None
    return nearest.tolist()

