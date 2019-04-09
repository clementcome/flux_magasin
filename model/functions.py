def intersectionTop(x, y, xA, yA, xB, yB): #regarde si la demi verticale  qui part de (x,y) coute [A,B]
    if x < xA and x < xB:
        return False
    if x > xA and x > xB:
        return False
    if xB < xA:
        return intersectionTop(x, y, xB, yB, xA, yA)
    return (x-xA)*(yB-yA) - (y-yA)*(xB-xA) > 0

def intersectionSeg(xA,yA,xB,yB,xC,yC,xD,yD): #regarde si les semgments [A,B] et [C,D] font une intersection
    return False

def intesectionHalf(xA,yA,xB,yB,xC,yC,xD,yD):#regarde si la demi-droite [A,B) et le segment [C,D] font une intersection
    return False