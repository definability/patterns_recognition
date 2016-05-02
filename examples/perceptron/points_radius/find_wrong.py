from numpy import array, column_stack, abs
from numpy.linalg import norm


def find_wrong(alpha, r, points):
    source_alpha = array(alpha)
    source_alpha /= norm(source_alpha)

    gamma = -source_alpha[0]
    alpha = source_alpha[1:]
    alpha /= norm(alpha)
    gamma /= norm(alpha)
    points = array(points)

    distances = gamma - points.dot(alpha.transpose())
    intersecting = (abs(distances) <= r)
    if not intersecting.any():
        return None

    intersecting_center = points[intersecting][0]
    intersecting_direction = distances[intersecting][0] * alpha
    intersecting_direction /= norm(intersecting_direction)
    intersecting_border = intersecting_center + r * intersecting_direction
    #pring 'R={}'.format(r),
    #pring 'Direction={}, norm={}'.format(intersecting_direction, norm(intersecting_direction)),
    #pring 'Center proj={}, border proj={}'.format(source_alpha.dot([1] + intersecting_center.tolist()), source_alpha.dot([1] + intersecting_border.tolist()))
    #pring 'Center pred={}, border pred={}'.format(gamma - alpha.dot(intersecting_center), gamma - alpha.dot(intersecting_border))
    return intersecting_border


def get_correction_point(alpha, r, points):
    nearest = find_wrong(alpha, r, points)
    if nearest is None:
        return None
    return [0] + nearest.tolist()

