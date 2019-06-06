from model.environnement import Wall,StandWall,Shop,Stand,Customer,Entry,Exit
from model.intersections import intersectionHalf,intersectPointLine, intersectionSeg
from model.static_graphic_display import store_display
from model.utils import norm
import numpy as np
from tkinter import Tk, Canvas
from math import inf

def view_field(stand, shop):
    '''
    Returns the view field of the stand inside the shop
    :param stand: (Stand) Stand considered
    :param shop: (Shop) Shop considered
    :return: (list) Polygone representing the view field
    '''
    center = stand.getCenter()
    poly = []
    for wall in shop.getWalls(): #on parcours tous les points d'intérêts des murs
        pos = wall.getPos()
        interest_points = [[pos[0],pos[1]],[pos[2],pos[3]]]
        for point in interest_points:
            if unobstructed_stand_wall(center,point,stand,wall,shop):
                poly.append([point,"wall",True]) #la variable True est vraie si le point n'est pas une intersection de points sélectionné
    for stand_test in shop.getStands():# on refait la même chose avec les points d'intérêts des stands, mais là il y en a plus car pour chque stand il y a 4 stand mur
        if stand_test.getId() != stand.getId():
            for stand_wall in stand_test.getStandWalls():
                pos = stand_wall.getPos()
                interest_points = [[pos[0],pos[1]],[pos[2], pos[3]]]
                for point in interest_points:
                    if unobstructed_stand_stand(center,point,stand,stand_wall,shop):
                        poly.append([point,"stand",True])
    #Il y a des duplicatats, donc on les enlèves
    poly_singles = []
    points_added = []
    for point in poly:
        if point[0] not in points_added:
            poly_singles.append(point)
            points_added.append(point[0])
    poly = poly_singles
    #On a déterminé tous les points d'intérêts dans le champ de vision, on va maintenant ajouter les points qui sont le prolongement ce des points sauvegardés
    wall_dic = {} #pour faire ça on va parcourir les murs pour chaque point et voir si ils sont adjacents, à chaque mur on va associer le nombre de points selectionnés qui sont leurs bords. On va ensuite enlever les points qui sont voisins de deux murs qui ont eux mêmes deux pointsselectionnés sur eux
    stand_wall_dic = {}
    for wall in shop.getWalls():
        wall_dic[wall.getId()] = 0
    for stand_test in shop.getStands():
        for stand_wall in stand_test.getStandWalls():
            stand_wall_dic[stand_wall.getId()] = 0
    for point in poly:
        if point[1] == "wall":
            for wall in shop.getWalls():
                if point_on_wall(point[0],wall):
                    wall_dic[wall.getId()] = wall_dic[wall.getId()] + 1
        elif point[1] == "stand":
            for stand_test in shop.getStands():
                for stand_wall in stand_test.getStandWalls():
                    if point_on_stand_wall(point[0],stand_wall):
                        stand_wall_dic[stand_wall.getId()] = stand_wall_dic[stand_wall.getId()] + 1
    for i in range(len(poly)):
        if poly[i][1] == "wall":
            walls = find_wall(poly[i][0],shop)
            n=0
            for wall in walls:
                if wall_dic[wall.getId()]>1:
                    n+=1
            if n>1:
                poly[i][2] =False
        if poly[i][1] == "stand":
            stand_walls = find_stand_wall(poly[i][0],shop)
            n = 0
            for stand_wall in stand_walls:
                if stand_wall_dic[stand_wall.getId()]>1:
                    n+=1
            if n >1:
                poly[i][2] = False
    #On regarde les intersections pour les poins qui marchent
    other_points = []
    for point in poly:
        dist = inf
        point_inter = [0,0]
        if point[1] == "wall":
            if point[2]: #si il est dans 2, c'est un coin et donc on ne le considère pas
                for wall in shop.getWalls():
                    if not point_on_wall(point[0],wall):
                        if (wall.getPos()[0] != point[0][0] and wall.getPos()[1] != point[0][1]) and (wall.getPos()[2] != point[0][0] and wall.getPos()[3] != point[0][1]):
                            if intersectionHalf(center[0],center[1],point[0][0],point[0][1],wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3]):
                                I = intersectPointLine(center[0],center[1],np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]),wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3])
                                if dist> norm(I-np.array([center[0],center[1]])) and np.dot(I-np.array(center[0],center[1]),np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]))>0:
                                    dist = norm(I-np.array([center[0],center[1]]))
                                    point_inter = I
                for stand_test in shop.getStands():
                    if stand_test.getId()!= stand.getId():
                        for stand_wall in stand_test.getStandWalls():
                            if intersectionHalf(center[0],center[1],point[0][0],point[0][1],stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3]):
                                I = intersectPointLine(center[0],center[1],np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]),stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3])
                                if dist>norm(I-np.array([center[0],center[1]])) and np.dot(I-np.array(center[0],center[1]),np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]))>0:
                                    dist = norm(I-np.array([center[0],center[1]]))
                                    point_inter = I
        if point[1] == "stand":
            if point[2]:
                for wall in shop.getWalls():
                    if intersectionHalf(center[0],center[1],point[0][0],point[0][1],wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3]):
                        I = intersectPointLine(center[0],center[1],np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]),wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3])
                        if dist> norm(I-np.array([center[0],center[1]])) and np.dot(I-np.array(center[0],center[1]),np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]))>0:
                            dist = norm(I - np.array([center[0], center[1]]))
                            point_inter = I
                for stand_test in shop.getStands():
                    if stand_test.getId()!=stand_test.getId():
                        for stand_wall in stand_test.getStandWalls():
                            if not point_on_stand_wall(point[0],stand_wall):
                                if intersectionHalf(center[0],center[1],point[0][0],point[0][1],stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3]):
                                    I = intersectPointLine(center[0],center[1],np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]),stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3])
                                    if dist > norm(I - np.array([center[0], center[1]])) and np.dot(I-np.array(center[0],center[1]),np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]))>0:
                                        dist = norm(I - np.array([center[0], center[1]]))
                                        point_inter = I
        if dist!= inf:
            other_points.append([point_inter,0,0])
    return poly +other_points

def unobstructed_stand_wall(pointStand,pointWall,stand,wall,shop):
    '''
    Checks if in the shop there is an intersection between the point on the stand and the point on the wall
    :param pointStand:(list) point that belongs to a stand
    :param pointWall: (list) point that belongs to a wall
    :param stand: (Stand) stand on witch the pointStand is located
    :param wall: (Wall) wall on witch the pointWall is located
    :param shop: (Shop) the shop
    :return: (boolean) True if there is no intersection in the shop with the segment formed by these two points, False otherwise
    '''
    keep = True
    for wall_check in shop.getWalls():  # pour tous les autres murs on regarde si il y a une intersection
        if wall.getId() != wall_check.getId():
            if intersectionSeg(pointStand[0], pointStand[1], pointWall[0], pointWall[1], wall_check.getPos()[0], wall_check.getPos()[1],
                               wall_check.getPos()[2], wall_check.getPos()[3]):
                keep = False
    for stand_check in shop.getStands():
        if stand_check.getId() != stand.getId():
            for stand_wall in stand_check.getStandWalls():  # pour tous les autres standmur on regarde si il y a une intersection
                if intersectionSeg(pointStand[0], pointStand[1], pointWall[0], pointWall[1], stand_wall.getPos()[0],
                                   stand_wall.getPos()[1], stand_wall.getPos()[2], stand_wall.getPos()[3]):
                    keep = False
    return keep

def unobstructed_stand_stand(pointStand1,pointStand2,stand1,wallOfStand2,shop):
    '''
    Checks if there is an intersection in the shop with the segment [pointStand1, pointStand2]
    :param pointStand1: (list) point on stand1
    :param pointStand2: (list) point on wallOfStand2
    :param stand1: (Stand) stand that contains pointStand1
    :param wallOfStand2: (StandWall) stand wall that contains pointStand2
    :param shop: (Shop) the shop
    :return: (boolean) True if there is no intersection in the shop with the segment formed by these two points, False otherwise
    '''
    keep = True
    for wall_check in shop.getWalls():
        if intersectionSeg(pointStand1[0], pointStand1[1], pointStand2[0], pointStand2[1], wall_check.getPos()[0], wall_check.getPos()[1],
                           wall_check.getPos()[2], wall_check.getPos()[3]):
            keep = False
    for stand_check in shop.getStands():
        if stand_check.getId() != stand1.getId():
            for stand_wall_check in stand_check.getStandWalls():
                if stand_wall_check.getId() != wallOfStand2.getId():
                    if intersectionSeg(pointStand1[0], pointStand1[1], pointStand2[0], pointStand2[1], stand_wall_check.getPos()[0],
                                       stand_wall_check.getPos()[1], stand_wall_check.getPos()[2],
                                       stand_wall_check.getPos()[3]):
                        keep = False
    return keep

def point_on_wall(point,wall):
    '''
    Checks if the point is on the wall
    :param point: (list) coordinates of the point
    :param wall: (Wall) Wall
    :return: (boolean) True if the point is one of the edges of the wall, False otherwise
    '''
    if (point == [wall.getPos()[0],wall.getPos()[1]]) or (point ==[wall.getPos()[2],wall.getPos()[3]]):
        return True
    return False
def point_on_stand_wall(point,stand_wall):
    '''
    Checks if the point is on the wall stand
    :param point: (list) coordinates of the point
    :param stand_wall: (StandWall)  StandWall
    :return: (boolean) True if the point is one of the edges of the stand wall, False otherwise
    '''
    if (point == [stand_wall.getPos()[0],stand_wall.getPos()[1]]) or (point ==[stand_wall.getPos()[2],stand_wall.getPos()[3]]):
        return True
    return False
def find_wall(point,shop):
    '''
    Finds the walls on witch the point is one of the edges
    :param point: (list) Coordinates of the point
    :param shop: (Shop) Shop
    :return: (list) List of the walls where point is one of the edges
    '''
    res = []
    for wall in shop.getWalls():
        if (point == [wall.getPos()[0],wall.getPos()[1]]) or (point ==[wall.getPos()[2],wall.getPos()[3]]):
            res.append(wall)
    return res
def find_stand_wall(point,shop):
    '''
    Finds the stand walls on witch the point is one of the edges
    :param point: (list) Coordinates of the point
    :param shop: (Shop) Shop
    :return: (list) List of the stand walls where point is one of the edges
    '''
    res = []
    for stand in shop.getStands():
        for stand_wall in stand.getStandWalls():
            if (point == [stand_wall.getPos()[0],stand_wall.getPos()[1]]) or (point ==[stand_wall.getPos()[2],stand_wall.getPos()[3]]):
                res.append(stand_wall)
    return res
###
def creation_fenetre_fov(shop):
    '''
    Creates the frame
    :param shop: (Shop) The shop
    '''
    global root
    root = Tk()
    root.title('Magasin')

    murs = shop.getWalls()

    x_max = 0
    y_max = 0
    for mur in murs:
        coord = mur.getPos()
        if coord[0] > x_max:
            x_max = coord[0]
        if coord[2] > x_max:
            x_max = coord[2]
        if coord[1] > y_max:
            y_max = coord[1]
        if coord[3] > y_max:
            y_max = coord[3]

    global magasin
    magasin = Canvas(root, width=x_max+15, height=y_max+15)
    magasin.pack()
if __name__ == '__main__':

    Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
    Entrees_test = [Entry(200,0,245,0,45), Entry(150,200,180,200,45)]
    Sorties_test = [Exit(0,100,0,150), Exit(150,200,180,200)]
    Meubles_test = [Stand(0,0,25,50), Stand(150,150,250,180),Stand(100,100,170,140)]
    Clients_test = [Customer(45,78,3,4,6), Customer(187,23,7,7,7)]


    Shop_test = Shop('test')
    for wall in Murs_test:
        Shop_test.addWall(wall)
    for stand in Meubles_test:
        Shop_test.addStand(stand)
    for entry in Entrees_test:
        Shop_test.addEntry(entry)
    for exit in Sorties_test:
        Shop_test.addExit(exit)
    for client in Clients_test:
        Shop_test.addCustomer(client)



    creation_fenetre_fov(Shop_test)
    store_display(Shop_test, magasin)

    i = 0
    points = view_field(Shop_test.getStands()[i], Shop_test)
    magasin.create_oval(Shop_test.getStands()[i].getCenter()[0] + 5, Shop_test.getStands()[i].getCenter()[1] + 5, Shop_test.getStands()[i].getCenter()[0] + 20, Shop_test.getStands()[i].getCenter()[1] + 20, fill='pink')
    for point in points:
        magasin.create_oval(point[0][0] + 5, point[0][1] + 5, point[0][0] + 15, point[0][1] + 15, fill='cyan')


    root.mainloop()
