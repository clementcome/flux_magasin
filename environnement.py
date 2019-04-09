from math import inf



class Mur:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def getCoordinates(self):
        return [self.x1, self.y1, self.x2, self.y2]


class Meuble:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def getPos(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def getCenter(self):
        return (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2

    def inside(self,pos): # on regarde si un point est dans le meuble (il faut implémenter un meuble intérieur (
        # probablement en rajoutant des murs) où les gens ne peuvent pas rentrer
        if pos[0]>self.x1 and pos[0]<self.x2 and pos[1]>self.y1 and pos[1]<self.y2:
            return True
        else:
            return False


class Client:
    def __init__(self, x, y, v_x, v_y, tRemain, nbRemain=None, attractCoef=None):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.t_remain = tRemain
        self.nb_remain = nbRemain
        self.leaving = False

        if nbRemain is None:
            self.nb_remain = inf
        else:
            self.nb_remain = nbRemain

        if attractCoef is None:
            self.attract_coef = 1
        else:
            self.attract_coef = attractCoef

    @property
    def getPos(self):
        return [self.x,self.y]

    def getSpeed(self):
        return [self.v_x, self.v_y]

    def getTime(self):
        return self.t_remain

    def getArticle(self):
        return self.nb_remain

    def getAttract(self):
        return self.attract_coef

    def setPos(self,pos):
        self.x = pos[0]
        self.y = pos[1]

    def setSpeed(self, speed):
        self.v_x = speed[0]
        self.v_y = speed[1]

    def updateTime(self,time_passed): #on enlève le temps qui s'est écoulé
        self.t_remain = self.t_remain - time_passed
        if self.t_remain < 0:
            self.leaving = True

    def updateArticle(self):
        self.nb_remain+=-1


class Entry:
    def __init__(self,x1,y1,x2,y2,flow):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.flow = flow

    @property

    def getPos(self):
        return [self.x1,self.y1,self.x2,self.y2]

    def getFlow(self):
        return self.flow


class Exit:
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property

    def getPos(self):
        return [self.x1,self.y1,self.x2,self.y2]
