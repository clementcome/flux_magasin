from math import inf
import numpy as np
from model.utils import norm

idWall = 0
idStandWall = 0
idStand = 0
idCustomer = 0
idEntry = 0
idExit = 0
idShop = 0

class Wall:
    def __init__(self, x1, y1, x2, y2):
        '''
        Creates the object wall
        :param x1: (float) X-axis coordinate of the start of the wall
        :param y1: (float) Y-axis coordinate of the start of the wall
        :param x2: (float) X-axis coordinate of the end of the wall
        :param y2: (float) Y-axis coordinate of the end of the wall
        '''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        global idWall
        self.id = idWall
        idWall += 1

    def getPos(self):
        '''
        Gives the position of the wall
        :return: (list) Position of the wall
        '''
        return [self.x1, self.y1, self.x2, self.y2]

    def getId(self):
        '''
        Returns the id of the wall
        :return: (integer) Id
        '''
        return self.id

    def getNormal(self):
        '''
        Returns the normal to the wall
        :return: (array) Normal to the wall
        '''
        if (self.y2-self.y1) != 0:
            return np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0, 1])

class StandWall:
    def __init__(self,x1, y1, x2, y2):
        '''
        Creates a wall attached to a stand
        :param x1:(float) X-axis coordinate of the start of the wall
        :param y1:(float) Y-axis coordinate of the start of the wall
        :param x2:(float) X-axis coordinate of the end of the wall
        :param y2:(float) Y-axis coordinate of the end of the wall
        '''

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        global idStandWall
        self.id = idStandWall
        idStandWall += 1

    def getPos(self):
        '''
        Gives the position
        :return: (list) Position of the wall
        '''
        return [self.x1, self.y1, self.x2, self.y2]

    def getId(self):
        '''
        Returns the id of the wall
        :return: (integer) Id
        '''
        return self.id

    def getNormal(self):
        '''
        Returns the normal to the wall
        :return: (array) Normal to the wall
        '''

        if (self.y2-self.y1) != 0:
            return np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0, 1])


class Stand:
    def __init__(self, x1, y1, x2, y2):
        '''
        Creates a stand, it is defined by it's lower left corner and upper right corner
        :param x1: (float) X-axis coordinate of the lower right corner
        :param y1: (float) Y-axis coordinate of the lower right corner
        :param x2: (float) X-axis coordinate of the upper left corner
        :param y2: (float) Y-axis coordinate of the upper left corner
        '''

        #If (x1, y1) are the coordinates of the upper right corner, we exchange (x1, y1) and (x2, y2)
        if x1 < x2:
            x1, x2 = x2, x1
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
                           StandWall(self.x1, self.y1, self.x2, self.y1),
                           StandWall(self.x1, self.y2, self.x2, self.y2),
                           StandWall(self.x2, self.y1, self.x2, self.y2)]

    def getPos(self):
        '''
        Gives the position of the stand
        :return: (list) Position of the stand
        '''
        return [self.x1, self.y1, self.x2, self.y2]

    def getStandWalls(self):
        '''
        Returns the list of stand walls associated to this stand
        :return: (list) List of StandWalls
        '''
        return self.standWalls

    def getCenter(self):
        '''
        Returns the center of the stand
        :return: (array) coordinates of the center of the stand
        '''
        return np.array([(self.x1 + self.x2)/2, (self.y1 + self.y2)/2])

    # def inside(self,pos):
    #     # on regarde si un point est dans le meuble (il faut implémenter un meuble intérieur (
    #     # probablement en rajoutant des murs) ou les gens ne peuvent pas rentrer
    #     '''
    #     Checks if the point pos is inside of the stand.
    #     :param pos: (list or array) Coordinates of the point considered
    #     :return: (boolean) True if it is inside the wall, False otherwiser
    #     '''
    #     if pos[0]>self.x1 and pos[0]<self.x2 and pos[1]>self.y1 and pos[1]<self.y2:
    #         return True
    #     else:
    #         return False

    def getId(self):
        '''
        Returns the id of the wall
        :return: (integer) Id
        '''
        return self.id


class Customer:
    def __init__(self, x, y, v_x, v_y, id = None):
        '''
        Creates a customer
        :param x: (float) X-axis coordinate of the customer
        :param y: (float) Y-axis coordinate of the customer
        :param v_x: (float) X-axis speed of the customer
        :param v_y: (float) Y-axis speed of the customer
        '''

        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y

        global idCustomer
        self.id = idCustomer
        idCustomer += 1

    def getPos(self):
        '''
        Gives the position of the customer
        :return: (list) Position of the customer
        '''
        return np.array([self.x,self.y])

    def getSpeed(self):
        '''
        Gives the speed
        :return: (list) Speed of the customer
        '''
        return np.array([self.v_x, self.v_y])

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

    def getId(self):
        '''
        Returns the Id
        :return: (integer) Id
        '''
        return self.id


class Entry:
    def __init__(self, x1, y1, x2, y2, flow):
        '''
        Creates an entry to the shop
        :param x1: (float) X-axis coordinate of the beginning of the entry
        :param y1: (float) Y-axis coordinate of the beginning of the entry
        :param x2: (float) X-axis coordinate of the end of the entry
        :param y2: (float) Y-axis coordinate of the end of the entry
        :param flow: (float) Flow of arrival of clients
        '''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.flow = flow

        global idEntry
        self.id = idEntry
        idEntry += 1

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
        :return: (array) Normal to the entry
        '''
        if (self.y2-self.y1) != 0:
            return np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0, 1])

class Exit:
    def __init__(self, x1, y1, x2, y2):
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
        idExit += 1

    def getPos(self):
        '''
        Returns the position of the exit
        :return: (list) Position of the exit
        '''
        return [self.x1, self.y1, self.x2, self.y2]

    def getId(self):
        '''
        Returns the Id of the exit
        :return: (integer) Id
        '''
        return self.id

    def getNormal(self):
        '''
        Returns the normal to the exit
        :return: (array) Normal to the exit
        '''
        if (self.y2-self.y1) != 0:
            return np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)])/norm(np.array([1, -(self.x2-self.x1)/(self.y2-self.y1)]))
        else:
            return np.array([0, 1])


class Shop:
    def __init__(self, name):
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
        self.x_max = 0
        self.y_max = 0
        self.x_min = 0
        self.y_min = 0

        global idShop
        self.id = idShop
        idShop += 1

    def get_x_max(self):
        """
        Return the maximal x of the shop
        :return: x_max
        """
        return self.x_max

    def get_x_min(self):
        """
        Return the minimal x of the shop
        :return: x_min
        """
        return self.x_min

    def get_y_min(self):
        """
        Return the minimal y of the shop
        :return: y_min
        """
        return self.y_min

    def get_y_max(self):
        """
        :return: y_max
        """
        return self.y_max

    def calculate_x_y_max(self):
        x_max = 0
        y_max = 0
        for wall in self.getWalls():
            coord = wall.getPos()
            if coord[0] > x_max:
                x_max = coord[0]
            if coord[2] > x_max:
                x_max = coord[2]
            if coord[1] > y_max:
                y_max = coord[1]
            if coord[3] > y_max:
                y_max = coord[3]
        for exit in self.getExits():
            coord = exit.getPos()
            if coord[0] > x_max:
                x_max = coord[0]
            if coord[2] > x_max:
                x_max = coord[2]
            if coord[1] > y_max:
                y_max = coord[1]
            if coord[3] > y_max:
                y_max = coord[3]
        for entry in self.getEntries():
            coord = entry.getPos()
            if coord[0] > x_max:
                x_max = coord[0]
            if coord[2] > x_max:
                x_max = coord[2]
            if coord[1] > y_max:
                y_max = coord[1]
            if coord[3] > y_max:
                y_max = coord[3]
        self.x_max = x_max
        self.y_max = y_max

    def calculate_x_y_min(self):
        x_min = 0
        y_min = 0
        for wall in self.getWalls():
            coord = wall.getPos()
            if coord[0] < x_min:
                x_min = coord[0]
            if coord[2] < x_min:
                x_min = coord[2]
            if coord[1] < y_min:
                y_min = coord[1]
            if coord[3] < y_min:
                y_min = coord[3]
        for exit in self.getExits():
            coord = exit.getPos()
            if coord[0] < x_min:
                x_min = coord[0]
            if coord[2] < x_min:
                x_min = coord[2]
            if coord[1] < y_min:
                y_min = coord[1]
            if coord[3] < y_min:
                y_min = coord[3]
        for entry in self.getEntries():
            coord = entry.getPos()
            if coord[0] < x_min:
                x_min = coord[0]
            if coord[2] < x_min:
                x_min = coord[2]
            if coord[1] < y_min:
                y_min = coord[1]
            if coord[3] < y_min:
                y_min = coord[3]
        self.x_min = x_min
        self.y_min = y_min

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

    def getCustomers(self):
        '''
        Return the list of the customers of the shop
        :return: (list) Customers of the shop
        '''
        return self.clients

    def getEntries(self):
        '''
        Return a list of the entries of the shop
        :return: (list) Entries of the shop
        '''
        return self.entries

    def getExits(self):
        '''
        Return a list of the exists of the shop
        :return: (list) Exits of the shop
        '''
        return self.exits

    def getNumberCustomers(self):
        '''
        Returns the number of customers inside the shop
        :return: (integer) Number of clients
        '''
        return len(self.clients)

    def addWall(self, wall):
        '''
        Adds a wall or walls to the shop
        :param wall: (Wall or list) Wall(s) to be added
        '''
        if type(wall) == list:
            self.walls = self.walls + wall
        else:
            self.walls.append(wall)

    def addStand(self, stand):
        '''
        Adds a stand or stands to the shop
        :param stand: (Stand or list) Stand(s) to be added
        '''
        if type(stand) == list:
            self.stands = self.stands + stand
        else:
            self.stands.append(stand)

    def addCustomer(self, customer):
        '''
        Adds a customer or customers to the shop
        :param client: (Customer or list) Customer(s) to be added
        '''
        if type(customer) == list:
            self.clients = self.clients + customer
        else:
            self.clients.append(customer)

    def addEntry(self, entry):
        '''
        Adds an entry or entries to the shop
        :param entry: (Entry or list) Entry(ies) to be added
        '''
        if type(entry) == list:
            self.entries = self.entries + entry
        else:
            self.entries.append(entry)

    def addExit(self, exit):
        '''
        Adds an exit or exits to the shop
        :param exit: (Exit or list) Exit(s) to be added
        '''
        if type(exit) == list:
            self.exits = self.exits + exit
        else:
            self.exits.append(exit)

    def removeCustomer(self, customer):
        '''
        Removes a customer
        :param client : the customer to be removed
        '''
        self.clients.remove(customer)

    def removeEntry(self, id):
        '''
        Removes an entry by it's id
        :param id: (integer) Id of the entry
        '''
        for i in range(len(self.entries)):
            if self.entries[i].getId() == id:
                self.entries.remove(i)

    def removeExit(self, id):
        '''
        Removes an exit by it's id
        :param id: (integer) Id of the exit
        '''
        for i in range(len(self.exits)):
            if self.exits[i].getId() == id:
                self.exits.remove(i)

    def purchase(self, n=1):
        '''
        Increases the number of articles bought
        :param n: (integer) Number of articles added
        '''
        self.articlesBought += n

    def getId(self):
        '''
        Returns the Id of the shop
        :return: (integer) Id
        '''
        return self.id

    def getCustomerById(self, idC):
        '''
        Returns a client by it's Id
        :param idC: (integer) Id of the client
        :return: (Customer) Customer returned
        '''
        for client in self.clients:
            if client.getId() == idC:
                return client



