import numpy as np
from model.utils import norm

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def counterclockwise(A, B, C):  # regarde si les les points A B et C sont ordonnées dans le sens trigonométrique
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


def intersectionTop(x, y, xA, yA, xB, yB):  # regarde si la demi-droite verticale  qui part de (x,y) coupe [A,B]
    if x < xA and x < xB:
        return False
    if x > xA and x > xB:
        return False
    if xB < xA:
        return intersectionTop(x, y, xB, yB, xA, yA)
    return (x - xA) * (yB - yA) - (y - yA) * (xB - xA) > 0


def intersectionSeg(xA, yA, xB, yB, xC, yC, xD,
                    yD):  # regarde si les semgments [A,B] et [C,D] font une intersection, j'utilise la méthode de Bryce Boe https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    A = Point(xA, yA)
    B = Point(xB, yB)
    C = Point(xC, yC)
    D = Point(xD, yD)
    return counterclockwise(A, C, D) != counterclockwise(B, C, D) and counterclockwise(A, B, C) != counterclockwise(A,B,D)


def intersectionHalf(xA, yA, xB, yB, xC, yC, xD,
                     yD):  # regarde si la demi-droite [A,B) et le segment [C,D] ont une intersection
    vect = np.array([xB - xA,
                     yB - yA])  # je me ramène au cas précédent déplaçant B par le vecteur AB mutliplié par un coefficient suffisamment grand (déterminé en fonction de la position des autres points)
    #mu = max(abs(xB / xC), abs(xB / xD), abs(yB / yC), abs(yB / yD))
    mu = np.sqrt(sum([abs(i) for i in [xA, xB, xC, xD]])**2+sum([abs(i) for i in [yA, yB,yC,yD]])**2)
    vect = vect / norm(vect)
    vect = mu * vect
    return intersectionSeg(xA, yA, xB + vect[0], yB + vect[1], xC, yC, xD, yD)


def intersectPointLine(x, y, vect_norm, xA, yA, xB, yB):  # on calcule la distance entre un point et une droite, en connaissant le vecteur perpendiculaire à cette droite
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
