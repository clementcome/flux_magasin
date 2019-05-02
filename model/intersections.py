import numpy as np
from model.utils import norm

class Point:
    def __init__(self, x, y):
        '''
        Defines the class of a point
        :param x: Coordinate of the point on Ox
        :param y: Coordinate of the point on Oy
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
    :param x: (float) Coordonnates on Ox of the point M
    :param y: (float) Coordonnates on Oy of the point M
    :param xA: (float) Coordonnates on Ox of the point A
    :param yA: (float) Coordonnates on Oy of the point A
    :param xB: (float) Coordonnates on Ox of the point B
    :param yB: (float) Coordonnates on Oy of the point B
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
    '''
    Checks if the segments [A,B] and [C,D] form an intersection
    :param xA: Coordonnates on Ox of the point A (float)
    :param yA: Coordonnates selon Oy of the point A (float)
    :param xB: Coordonnates selon Ox of the point B (float)
    :param yB: Coordonnates selon Oy of the point B (float)
    :param xC: Coordonnates selon Ox of the point C (float)
    :param yC: Coordonnates selon Oy of the point C (float)
    :param xD: Coordonnates selon Ox of the point D (float)
    :param yD: Coordonnates selon Oy of the point D (float)
    :return: (Bool) True if [A,B] intersects [C,D], False otherwise
    '''
    A = Point(xA, yA)
    B = Point(xB, yB)
    C = Point(xC, yC)
    D = Point(xD, yD)
    return counterclockwise(A, C, D) != counterclockwise(B, C, D) and counterclockwise(A, B, C) != counterclockwise(A,B,D)


def intersectionHalf(xA, yA, xB, yB, xC, yC, xD,yD):
    '''
    Checks if the infinite half strait line that goes from A to B intersects the segment [C,D]
    :param xA: (float) Coordonnates on Ox of the point A
    :param yA: (float) Coordonnates on Oy of the point A
    :param xB: (float) Coordonnates on Ox of the point B
    :param yB: (float) Coordonnates on Oy of the point B
    :param xC: (float) Coordonnates on Ox of the point C
    :param yC: (float) Coordonnates on Oy of the point C
    :param xD: (float) Coordonnates on Ox of the point D
    :param yD: (float) Coordonnates on Oy of the point D
    :return: (Bool) True if they intersect, False if they don't
    '''
    vect = np.array([xB - xA, yB - yA])  # je me ramène au cas précédent déplaçant B par le vecteur AB mutliplié par un coefficient suffisamment grand (déterminé en fonction de la position des autres points)
    #mu = max(abs(xB / xC), abs(xB / xD), abs(yB / yC), abs(yB / yD))
    mu = np.sqrt(sum([abs(i) for i in [xA, xB, xC, xD]])**2+sum([abs(i) for i in [yA, yB,yC,yD]])**2)
    vect = vect / norm(vect)
    vect = mu * vect
    return intersectionSeg(xA, yA, xB + vect[0], yB + vect[1], xC, yC, xD, yD)

def intersectionSegDroite(xA, yA, xB, yB, x, y, vect_norm):
    '''
    Checks if there is an intersection between the segment [A,B] and the strait line that is directed by vect_norm and that passes through M = (x,y)
    :param xA: (float) Coordonnates on Ox of the point A
    :param yA: (float) Coordonnates on Oy of the point A
    :param xB: (float) Coordonnates on Ox of the point B
    :param yB: (float) Coordonnates on Oy of the point B
    :param x: (float) Coordonnates on Ox of the point M
    :param y: (float) Coordonnates on Oy of the point M
    :param vect_norm: (list or array) Vector
    :return: (Boolean) True if the intersect, False if they don't
    '''
    mu = np.sqrt(sum([abs(i) for i in [xA,xB,x]])**2+sum([abs(i) for i in [yA,yB,y]])**2)
    vect = (mu * vect_norm)/norm(vect_norm)
    return intersectionSeg(xA,yA,xB,yB,x-vect[0],y-vect[0],x+vect[0],y+vect[0])



def intersectPointLine(x, y, vect_norm, xA, yA, xB, yB):
    '''
    Returns the intersection bewteen the strait line that passes through A and B and the strait line directed by vect_norm that passes through M = (x,y)
    :param x: (float) Coordonnates on Ox of the point M
    :param y: (float) Coordonnates on Oy of the point M
    :param vect_norm: (list or array) Vectorn
    :param xA: (float) Coordonnates on Ox of the point A
    :param yA: (float) Coordonnates on Oy of the point A
    :param xB: (float) Coordonnates on Ox of the point B
    :param yB: (float) Coordonnates on Oy of the point B
    :return: (array) Coordonnates of the intersection
    '''
    if (xB - xA) != 0 and vect_norm[0] != 0:
        a1 = (yB - yA) / (xB - xA)  # les coefficients des deux droites considérées (on calcule l'intersection de la droite AB et de la droite qui passe par M dirigée par le vecteur vect_norm
        b1 = yB - a1 * xB
        a2 = vect_norm[1] / vect_norm[0]
        b2 = y - a2 * x
        return np.array([(b2 - b1) / (a1 - a2), a1 * ((b2 - b1) / (a1 - a2)) + b1])
    elif (xB - xA) != 0:
        a1 = (yB - yA) / (xB - xA)  # les coefficients des deux droites considérées (on calcule l'intersection de la droite AB et de la droite qui passe par M dirigée par le vecteur vect_norm
        b1 = yB - a1 * xB
        return np.array([x, a1*x+b1])  # dans ce cas yA=yB
    elif vect_norm[0] != 0:
        a2 = vect_norm[1] / vect_norm[0]
        b2 = y - a2 * x
        return np.array([xA, a2*xA+b2])  # dans ce cas xA=xB
    else:
        raise Exception('Le mur donné est un point')


def inside(x, y, polygone):
    """
    Checks whether a point is inside a polygon
    :param x: Coordonnate on the X axis
    :param y: Coordonnate on the Y axis
    :param polygone: Polygon (list of points)
    :return: A boolean
    """

    compteur = 0

    n = len(polygone)
    for i in range(n-1):
        xA, yA = polygone[i]
        xB, yB = polygone[i+1]
        if intersectionTop(x, y, xA, yA, xB, yB):
            compteur += 1
    return compteur % 2 == 1
