from math import inf
import numpy as np
from model.utils import norm

idWall = 0
idStandWall = 0
idStand = 0
idClient = 0
idEntry = 0
idExit = 0
idShop = 0

class Wall:
    def __init__(self, x1, y1, x2, y2):
        '''
        Creates the object wall
        :param x1: (float) Coordonates of the start of the wall on Ox
        :param y1: (float) Coordonates of the start of the wall on Oy
        :param x2: (float) Coordonates of the end of the wall on Ox
        :param y2: (float) Coordonates of the end of the wall on Oy
        '''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        global idWall
        self.id = idWall
        idWall+=1

    def getPos(self):
        '''
        Gives the position
        :return: (list) Position of the wall
        '''
        return [self.x1,self.y1,self.x2,self.y2]

    def getId(self):
        '''
        Returns the id of the wall
        :return: (integer) Id
        '''
        return self.id

    def getNormal(self):
        '''
        Returns the normal to the wall
        :return: (array) Normal of the wall
        '''
        if (self.y2-self.y1)!=0:
            return np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0,1])

class StandWall:
    def __init__(self,x1, y1, x2, y2):
        '''
        Creates a wall attached to a stall
        :param x1:(float) Coordonates of the start of the wall on Ox
        :param y1:(float) Coordonates of the start of the wall on Oy
        :param x2:(float) Coordonates of the end of the wall on Ox
        :param y2:(float) Coordonates of the end of the wall on Oy
        '''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        global idStandWall
        self.id = idStandWall
        idStandWall +=1
    def getPos(self):
        '''
        Gives the position
        :return: (list) Position of the wall
        '''
        return [self.x1,self.y1,self.x2,self.y2]
    def getId(self):
        '''
        Returns the id of the wall
        :return: (integer) Id
        '''
        return self.id
    def getNormal(self):
        '''
        Returns the normal to the wall
        :return: (array) Normal of the wall
        '''
        if (self.y2-self.y1)!=0:
            return np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0,1])


class Stand:
    def __init__(self, x1, y1, x2, y2):
        '''
        Creates a stand, it is defined by it's lower left corner and upper rigth corner
        :param x1: (float) Coordonates of the start of the wall on Ox
        :param y1: (float) Coordonates of the start of the wall on Oy
        :param x2: (float) Coordonates of the end of the wall on Ox
        :param y2: (float) Coordonates of the end of the wall on Oy
        '''
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

        #creation of the stand walls
        self.standWalls = [StandWall(self.x1, self.y1, self.x1, self.y2),
                           StandWall(self.x1 , self.y1 , self.x2 , self.y1 ),
                           StandWall(self.x1 , self.y2 , self.x2 , self.y2),
                           StandWall(self.x2, self.y1 , self.x2, self.y2)]

    def getPos(self):
        '''
        Gives the position
        :return: (list) Position of the stand
        '''
        return [self.x1,self.y1,self.x2,self.y2]

    def getStandWalls(self):
        '''
        Returns the list of stant wall associated to this stand
        :return: (list) List of StandWalls
        '''
        return self.standWalls

    def getCenter(self):
        '''
        Returns the center of the stand
        :return: (array) Coordonates of the center of the stand
        '''
        return np.array([(self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2])

    def inside(self,pos): # on regarde si un point est dans le meuble (il faut implémenter un meuble intérieur (
        # probablement en rajoutant des murs) ou les gens ne peuvent pas rentrer
        '''
        Checks if the point pos is inside of the stand.
        :param pos: (list or array) Coordinates of the point considered
        :return: (boolean) True if it is inside the wall, False otherwiser
        '''
        if pos[0]>self.x1 and pos[0]<self.x2 and pos[1]>self.y1 and pos[1]<self.y2:
            return True
        else:
            return False
    def getId(self):
        '''
        Returns the id of the wall
        :return: (integer) Id
        '''
        return self.id


class Client:
    def __init__(self, x, y, v_x, v_y, tRemain, nbPurchased=0, nbRemain=inf, repulsCoef=1):
        '''
        Creates a client
        :param x: (float) Coordinate of the client on the axis Ox
        :param y: (float) Coordinate of the client on the axis Oy
        :param v_x:(float) Speed of the client on the axis Ox
        :param v_y: (float) Speed of the client on the axis Oy
        :param tRemain: (float) Time until the client wants to leave
        :param nbPurchased:(integer) Number of itemps purchased
        :param nbRemain: (integer) Number of itemps he still wants to purchase
        :param repulsCoef: (float) Coeficient of repultion of the client
        '''
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.t_remain = tRemain
        self.nbPurchased = nbPurchased
        self.nb_remain = nbRemain
        self.attract_coef = repulsCoef
        self.leaving = False

        global idClient
        self.id = idClient
        idClient += 1

    def getPos(self):
        '''
        Gives the position
        :return: (list) Position of the client
        '''
        return np.array([self.x,self.y])

    def getSpeed(self):
        '''
        Gives the speed
        :return: (list) Speed of the client
        '''
        return np.array([self.v_x, self.v_y])

    def getTime(self):
        '''
        Gives the time until he wants to leave the shop
        :return: (float) Time remaining
        '''
        return self.t_remain

    def getNbPurchased(self):
        '''
        Gives the number of articles purchased
        :return: (integer) number of articles purchased
        '''
        return self.nbPurchased

    def getArticle(self):
        '''
        Gives the number of articles he wants to buy
        :return: (integer) Number of articles
        '''
        return self.nb_remain

    def getRepulstion(self):
        '''
        Return the repultion coefficient
        :return: (float) Repultion coefficient
        '''
        return self.repulsCoef

    def setPos(self,pos):
        '''
        Updates the position
        :param pos: (array or list) Updated position
        '''
        self.x = pos[0]
        self.y = pos[1]

    def setSpeed(self, speed):
        '''
        Updates the speed
        :param speed: (array or list) Updated speed
        '''
        self.v_x = speed[0]
        self.v_y = speed[1]

    def updateTime(self,time_passed): #on enlève le temps qui s'est écoulé
        '''
        We remove the time that has passed and set leaving to True if there is no time left
        :param time_passed: (float) Time passed
        '''
        self.t_remain = self.t_remain - time_passed
        if self.t_remain < 0:
            self.leaving = True

    def updateArticle(self):
        '''
        Update the number of articles
        '''
        self.nb_remain -= 1

    def getId(self):
        '''
        Returns the Id
        :return: (integer) Id
        '''
        return self.id

class Entry:
    def __init__(self,x1,y1,x2,y2,flow):
        '''
        Creates an entry to the shop
        :param x1: (float) Coordinate of the begining of the entry on the axis Ox
        :param y1: (float) Coordinate of the begining of the entry on the axis Oy
        :param x2: (float) Coordinate of the begining of the entry on the axis Ox
        :param y2: (float) Coordinate of the begining of the entry on the axis Oy
        :param flow: (float) Flow of arrival of the clients
        '''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.flow = flow

        global idEntry
        self.id = idEntry
        idEntry+=1

    def getPos(self):
        '''
        Returns the position of the entry
        :return: (list) Position of the entry
        '''
        return [self.x1,self.y1,self.x2,self.y2]

    def getFlow(self):
        '''
        Returns the flow of the entry
        :return: (float) Flow of the entry
        '''
        return self.flow

    def getId(self):
        '''
        Returns the Id of the entry
        :return: (integer) Id
        '''
        return self.id

    def getNormal(self):
        '''
        Returns the normal to the entry
        :return: (array) Normal of the entry
        '''
        if (self.y2-self.y1)!=0:
            return np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0,1])

class Exit:
    def __init__(self,x1,y1,x2,y2):
        '''
        Creates an exit
        :param x1: (float) Coordinate of the beginning of the exit on the axis Ox
        :param y1: (float) Coordinate of the beginning of the exit on the axis Oy
        :param x2: (float) Coordinate of the beginning of the exit on the axis Ox
        :param y2: (float) Coordinate of the beginning of the exit on the axis Oy
        '''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        global idExit
        self.id = idExit
        idExit+=1

    def getPos(self):
        '''
        Returns the position of the exit
        :return: (list) Position of the exit
        '''
        return [self.x1,self.y1,self.x2,self.y2]

    def getId(self):
        '''
        Returns the Id of the exit
        :return: (integer) Id
        '''
        return self.id

    def getNormal(self):
        '''
        Returns the normal to the exit
        :return: (array) Normal of the exit
        '''
        if (self.y2-self.y1)!=0:
            return np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1,-(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0,1])


class Shop:
    def __init__(self,name):
        '''
        Creates a shop
        :param name: (string) Name of the shop
        '''
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
        '''
        Return the list of the walls of the shop
        :return: (list) Walls of the shop
        '''
        return self.walls

    def getStands(self):
        '''
        Return the list of the stands of the shop
        :return: (list) Stands of the shop
        '''
        return self.stands

    def getClients(self):
        '''
        Return the list of the clients of the shop
        :return: (list) Clients of the shop
        '''
        return self.clients

    def getEntry(self):
        '''
        Return a list of the entries of the shop
        :return: (list) Entries of the shop
        '''
        return self.entries

    def getExit(self):
        '''
        Return a list of the exists of a shop
        :return: (list) Exits of a shop
        '''
        return self.exits

    def getNumberClients(self):
        '''
        Returns the numer of clients inside the shop
        :return: (integer) Number of clients
        '''
        return len(self.clients)

    def addWall(self,wall):
        '''
        Adds a wall to the shop
        :param wall: (Wall or list) Wall(s) to be added
        '''
        if type(wall) == list:
            self.walls = self.walls + wall
        else:
            self.walls.append(wall)

    def addStand(self,stand):
        '''
        Adds a stand to the shop
        :param stand: (Stand or list) Stand(s) to be added
        '''
        if type(stand) == list:
            self.stands = self.stands + stand
        else:
            self.stands.append(stand)

    def addClient(self,client):
        '''
        Adds a client to the shop
        :param client: (Client or list) Client(s) to be added
        '''
        if type(client) == list:
            self.clients = self.clients + client
        else:
            self.clients.append(client)

    def addEntry(self,entry):
        '''
        Adds an entry to the shop
        :param entry: (Entry or list) Entry(ies) to be added
        '''
        if type(entry) == list:
            self.entries = self.entries + entry
        else:
            self.entries.append(entry)

    def addExit(self,exit):
        '''
        Adds an exit to the shop
        :param exit: (Exit or list) Exit(s) to be added
        '''
        if type(exit) == list:
            self.exits = self.exits + exit
        else:
            self.exits.append(exit)

    def removeClient(self,client):
        '''
        Removes a client
        :param client : the client to be removed
        '''

        self.clients.remove(client)

    def removeEntry(self,id):
        '''
        Removes an entry by it's id
        :param id: (integer) Id of the entry
        '''
        for i in range(len(self.entries)):
            if self.entries[i].getId() == id:
                self.entries.remove(i)

    def removeExit(self,id):
        '''
        Removes an exit by it's id
        :param id: (integer) Id of the exit
        '''
        for i in range(len(self.exits)):
            if self.exits[i].getId() == id:
                self.exits.remove(i)

    def purchase(self,n=1):
        '''
        Increases the number of articles bougth
        :param n: (integer) Number of articles added
        '''
        self.articlesBought += n

    def getId(self):
        '''
        Returns the Id of the shop
        :return: (intger) Id
        '''
        return self.id

    def getClientById(self,idC):
        '''
        Returns a client by it's Id
        :param idC: (integer) Id of the client
        :return: (Client) Client returned
        '''
        for client in self.clients:
            if client.getId() == idC:
                return client
