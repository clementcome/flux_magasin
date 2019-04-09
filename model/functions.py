import numpy as np

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def counterclockwise(A,B,C): #regarde si les les points A B et C sont ordonnées dans le sens trigonométrique
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def intersectionTop(x, y, xA, yA, xB, yB): #regarde si la demi verticale  qui part de (x,y) coute [A,B]
    if x < xA and x < xB:
        return False
    if x > xA and x > xB:
        return False
    if xB < xA:
        return intersectionTop(x, y, xB, yB, xA, yA)
    return (x-xA)*(yB-yA) - (y-yA)*(xB-xA) > 0

def intersectionSeg(xA,yA,xB,yB,xC,yC,xD,yD): #regarde si les semgments [A,B] et [C,D] font une intersection, j'utilise la méthode de Bryce Boe https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    A = Point(xA, yA)
    B = Point(xB, yB)
    C = Point(xC, yC)
    D = Point(xD, yD)
    return counterclockwise(A,C,D) != counterclockwise(B,C,D) and counterclockwise(A,B,C) != counterclockwise(A,B,D)
def intersectionHalf(xA,yA,xB,yB,xC,yC,xD,yD):#regarde si la demi-droite [A,B) et le segment [C,D] font une intersection
    vect = np.array([xB-xA,yB-yA]) #je me ramène au cas précédent déplaçant B par le vecteur AB mutliplié par un coefficient suffisamment grand (déterminé en fonction de la position des autres points)
    mu = max(abs(xB/xC),abs(xB/xD),abs(yB/yC),abs(yB/yD))
    vect = mu*vect
    return intersectionSeg(xA,xB,xB+vect[0],yB+vect[1],xC,yC,xD,yD)

print(intersectionHalf(1,1,3,1,-11,-1,-1,-8))