import numpy as np
from model.utils import norm

class Point:
    def __init__(self, x, y):
        '''
        Defines the class of a point
        :param x: X-axis coordinate of the point
        :param y: Y-axis coordinate of the point
        '''
        self.x = x
        self.y = y

def norm(vect):
    '''
    Returns the norm of a vector
    :param vect: (list or array) vector
    :return: (float) norm of the vector
    '''
    return np.sqrt(vect[0]**2+vect[1]**2)

def counterclockwise(A, B, C):
    '''
    Checks if A, B and C are in trigonometrical order
    :param A: Point A (from class point)
    :param B: Point B (from class point)
    :param C: Point C (from class point)
    :return: (Boolean) True if they are in trigonometrical order, false otherwise
    '''
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


def intersectionTop(x, y, xA, yA, xB, yB):
    '''
    Checks if the vertical infinite half strait line that starts at M = (x,y) and and goes to y = infinity intersects with [A,B]
    :param x: (float) X-axis coordinate of the point M
    :param y: (float) Y-axis coordinate of the point M
    :param xA: (float) X-axis coordinate of the point A
    :param yA: (float) Y-axis coordinate of the point A
    :param xB: (float) X-axis coordinate of the point B
    :param yB: (float) Y-axis coordinate of the point B
    :return: (Boolean) True if they intersect, False if they don't
    '''
    if x < xA and x < xB:
        return False
    if x > xA and x > xB:
        return False
    if xB < xA:
        return intersectionTop(x, y, xB, yB, xA, yA)
    return (x - xA) * (yB - yA) - (y - yA) * (xB - xA) > 0


def intersectionSeg(xA, yA, xB, yB, xC, yC, xD, yD):
    """
    Checks if the segments [A,B] and [C,D] form an intersection
    :param xA: X-axis coordinate of the point A (float)
    :param yA: Y-axis coordinate of the point A (float)
    :param xB: X-axis coordinate of the point B (float)
    :param yB: Y-axis coordinate of the point B (float)
    :param xC: X-axis coordinate of the point C (float)
    :param yC: Y-axis coordinate of the point C (float)
    :param xD: X-axis coordinate of the point D (float)
    :param yD: Y-axis coordinate of the point D (float)
    :return: (Bool) True if [A,B] intersects [C,D], False otherwise
    """
    A = Point(xA, yA)
    B = Point(xB, yB)
    C = Point(xC, yC)
    D = Point(xD, yD)
    return counterclockwise(A, C, D) != counterclockwise(B, C, D) and counterclockwise(A, B, C) != counterclockwise(A, B, D)


def intersectionHalf(xA, yA, xB, yB, xC, yC, xD,yD):
    """
    Checks if the infinite half strait line that goes from A to B intersects the segment [C,D]
    :param xA: (float) X-axis coordinate of the point A
    :param yA: (float) Y-axis coordinate of the point A
    :param xB: (float) X-axis coordinate of the point B
    :param yB: (float) Y-axis coordinate of the point B
    :param xC: (float) X-axis coordinate of the point C
    :param yC: (float) Y-axis coordinate of the point C
    :param xD: (float) X-axis coordinate of the point D
    :param yD: (float) Y-axis coordinate of the point D
    :return: (Bool) True if they intersect, False if they don't
    """
    vect = np.array([xB - xA, yB - yA])  # we go back to the last case by moving B of the vect AB multiplied by a big enough coef (found according to the other points positions)
    #mu = max(abs(xB / xC), abs(xB / xD), abs(yB / yC), abs(yB / yD))
    mu = np.sqrt(sum([abs(i) for i in [xA, xB, xC, xD]])**2 + sum([abs(i) for i in [yA, yB, yC, yD]])**2)
    vect = vect / norm(vect)
    vect = mu * vect
    return intersectionSeg(xA, yA, xB + vect[0], yB + vect[1], xC, yC, xD, yD)

def intersectionSegDroite(xA, yA, xB, yB, x, y, vect_norm):
    '''
    Checks if there is an intersection between the segment [A,B] and the strait line that is directed by vect_norm and that passes through M = (x,y)
    :param xA: (float) X-axis coordinate of the point A
    :param yA: (float) Y-axis coordinate of the point A
    :param xB: (float) X-axis coordinate of the point B
    :param yB: (float) Y-axis coordinate of the point B
    :param x: (float) X-axis coordinate of the point M
    :param y: (float) Y-axis coordinate of the point M
    :param vect_norm: (list or array) Normed vector
    :return: (Boolean) True if the intersect, False if they don't
    '''
    mu = np.sqrt(sum([abs(i) for i in [xA, xB, x]])**2 + sum([abs(i) for i in [yA, yB, y]])**2)
    vect = (mu * vect_norm)/norm(vect_norm)
    return intersectionSeg(xA, yA, xB, yB, x-vect[0], y-vect[0], x+vect[0], y+vect[0])


def intersectPointLine(x, y, vect_norm, xA, yA, xB, yB):
    '''
    Returns the intersection between the strait line that passes through A and B and the strait line directed by vect_norm that passes through M = (x,y)
    :param x: (float) X-axis coordinate of the point M
    :param y: (float) Y-axis coordinate of the point M
    :param vect_norm: (list or array) Vector
    :param xA: (float) X-axis coordinate of the point A
    :param yA: (float) Y-axis coordinate of the point A
    :param xB: (float) X-axis coordinate of the point B
    :param yB: (float) Y-axis coordinate of the point B
    :return: (array) Coordinates of the intersection
    '''
    if (xB - xA) != 0 and vect_norm[0] != 0:
        a1 = (yB - yA) / (xB - xA)  # slope of the first considered strait line
        b1 = yB - a1 * xB
        a2 = vect_norm[1] / vect_norm[0] # slope of the second strait line
        b2 = y - a2 * x
        return np.array([(b2 - b1) / (a1 - a2), a1 * ((b2 - b1) / (a1 - a2)) + b1])
    elif (xB - xA) != 0:
        a1 = (yB - yA) / (xB - xA)  # slope of the first considered strait line
        b1 = yB - a1 * xB
        return np.array([x, a1*x+b1])  # in that case, yA = yB
    elif vect_norm[0] != 0:
        a2 = vect_norm[1] / vect_norm[0]
        b2 = y - a2 * x
        return np.array([xA, a2*xA+b2])  # in that case, xA = xB
    else:
        raise Exception('The given wall is a point.')


def inside(x, y, polygon):
    """
    Checks whether a point is inside a polygon
    :param x: X-axis coordinate
    :param y: Y-axis coordinate
    :param polygon: Polygon (list of points)
    :return: A boolean
    """
    count = 0

    n = len(polygon)
    for i in range(n-1):
        xA, yA = polygon[i]
        xB, yB = polygon[i+1]
        if intersectionTop(x, y, xA, yA, xB, yB):
            count += 1
    return count % 2 == 1
