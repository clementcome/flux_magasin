from math import inf
import numpy as np
from model.forces import *

idWall = 0
idStandWall = 0
idStand = 0
idClient = 0
idEntry = 0
idExit = 0
idShop = 0

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        global idWall
        self.id = idWall
        idWall+=1

    def getPos(self):
        return [self.x1,self.y1,self.x2,self.y2]

    def getId(self):
        return self.id

    def getNormal(self):
        if (self.y2-self.y1)!=0:
            return np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0,1])

class StandWall:
    def __init__(self,x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        global idStandWall
        self.id = idStandWall
        idStandWall +=1
    def getPos(self):
        return [self.x1,self.y1,self.x2,self.y2]
    def getId(self):
        return self.id
    def getNormal(self):
        if (self.y2-self.y1)!=0:
            return np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0,1])


class Stand:
    def __init__(self, x1, y1, x2, y2):
        if x1<x2:
            x1,x2 = x2,x1
        if y1 < y2:
            y1, y2 = y2, y1
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        global idStand
        self.id = idStand
        idStand += 1


        self.standWalls = [StandWall(self.x1, self.y1, self.x1, self.y2),
                           StandWall(self.x1 , self.y1 , self.x2 , self.y1 ),
                           StandWall(self.x1 , self.y2 , self.x2 , self.y2),
                           StandWall(self.x2, self.y1 , self.x2, self.y2)]

    def getPos(self):
        return [self.x1,self.y1,self.x2,self.y2]

    def getStandWalls(self): #position de la partie solide du meuble (se comporte comme un mur)
        return self.standWalls

    def getCenter(self):
        return np.array([(self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2])

    def inside(self,pos): # on regarde si un point est dans le meuble (il faut implémenter un meuble intérieur (
        # probablement en rajoutant des murs) ou les gens ne peuvent pas rentrer
        if pos[0]>self.x1 and pos[0]<self.x2 and pos[1]>self.y1 and pos[1]<self.y2:
            return True
        else:
            return False
    def getId(self):
        return self.id


class Client:
    def __init__(self, x, y, v_x, v_y, tRemain, nbPurchased=0, nbRemain=inf, attractCoef=1):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.t_remain = tRemain
        self.nbPurchased = nbPurchased
        self.nb_remain = nbRemain
        self.attract_coef = attractCoef
        self.leaving = False

        global idClient
        self.id = idClient
        idClient += 1

    def getPos(self):
        return np.array([self.x,self.y])

    def getSpeed(self):
        return np.array([self.v_x, self.v_y])

    def getTime(self):
        return self.t_remain

    def getNbPurchased(self):
        return self.nbPurchased

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
        self.nb_remain -= 1

    def getId(self):
        return self.id

class Entry:
    def __init__(self,x1,y1,x2,y2,flow):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.flow = flow

        global idEntry
        self.id = idEntry
        idEntry+=1

    def getPos(self):
        return [self.x1,self.y1,self.x2,self.y2]

    def getFlow(self):
        return self.flow

    def getId(self):
        return self.id

class Exit:
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        global idExit
        self.id = idExit
        idExit+=1

    def getPos(self):
        return [self.x1,self.y1,self.x2,self.y2]

    def getId(self):
        return self.id

class Shop:
    def __init__(self,name):
        self.name = name
        self.articlesBought = 0
        self.walls = []
        self.stands = []
        self.clients = []
        self.entries = []
        self.exits = []

        global idShop
        self.id = idShop
        idShop+=1

    def getWalls(self):
        return self.walls

    def getStands(self):
        return self.stands

    def getClients(self):
        return self.clients

    def getEntry(self):
        return self.entries

    def getExit(self):
        return self.exits

    def getNumberClients(self):
        return len(self.clients)

    def addWall(self,wall):
        if type(wall) == list:
            self.walls = self.walls + wall
        else:
            self.walls.append(wall)

    def addStand(self,stand):
        if type(stand) == list:
            self.stands = self.stands + stand
        else:
            self.stands.append(stand)

    def addClient(self,client):
        if type(client) == list:
            self.clients = self.clients + client
        else:
            self.clients.append(client)

    def addEntry(self,entry):
        if type(entry) == list:
            self.entries = self.entries + entry
        else:
            self.entries.append(entry)

    def addExit(self,exit):
        if type(exit) == list:
            self.exits = self.exits + exit
        else:
            self.exits.append(exit)

    def removeEntry(self,id):
        for i in range(len(self.entries)):
            if self.entries[i].getId() == id:
                self.entries.remove(i)

    def removeExit(self,id):
        for i in range(len(self.exits)):
            if self.exits[i].getId() == id:
                self.exits.remove(i)

    def purchase(self,n=1):
        self.articlesBought += n

    def getId(self):
        return self.id

    def getClientById(self,idC):
        for client in self.clients:
            if client.getId() == idC:
                return client