from flux_magasin.model.environnement import *
from flux_magasin.model.intersections import *
from flux_magasin.model.representation_graphique_statique import *
from math import inf

def field_of_view(stand,shop): #pas fini
    center = stand.getCenter()
    poly = []
    for wall in shop.getWalls(): #on parcours tous les points d'intérêts des murs
        pos = wall.getPos()
        interest_points = [[pos[0],pos[1]],[pos[2],pos[3]]]
        for point in interest_points:
            if unobstructed_stand_wall(center,point,stand,wall,shop):
                poly.append([point,"wall",wall])
    for stand_test in shop.getStands():# on refait la même chose avec les points d'intérêts des stands, mais là il y en a plus car pour chque stand il y a 4 stand mur
        if stand_test.getId() != stand.getId():
            for stand_wall in stand_test.getStandWalls():
                pos = stand_wall.getPos()
                interest_points = [[pos[0],pos[1]],[pos[2], pos[3]]]
                for point in interest_points:
                    if unobstructed_stand_stand(center,point,stand,stand_wall,shop):
                        poly.append([point,"stand",stand_wall])
    #On a déterminé tous les points d'intérêts dans le champ de vision, on va maintenant ajouter les points qui sont le prolongement ce des points sauvegardés
    list_walls = []
    list_stand_walls = []
    for point in poly:
        if point[1] == "wall":
            list_walls.append(point[2])
        elif point[1] == "stand":
            list_stand_walls.append(point[2])
    other_points = []
    for point in poly:
        dist = inf
        point_inter = [0,0]
        if point[1] == "wall":
            n = 0 #nombre de murs dans lequel notre point apparait
            for wall in list_walls:
                if point[2].getId() == wall.getId():
                    n+=1
            if n == 1: #si il est dans 2, c'est un coin et donc on ne le considère pas
                for wall in shop.getWalls():
                    if wall.getId()!=point[2].getId():
                        if intersectionHalf(center[0],center[1],point[0][0],point[0][1],wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3]):
                            I = intersectPointLine(center[0],center[1],np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]),wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3])
                            if dist> norm(I-np.array([center[0],center[1]])):
                                dist = norm(I-np.array([center[0],center[1]]))
                                point_inter = I
                for stand_test in shop.getStands():
                    if stand_test.getId()!= stand.getId():
                        for stand_wall in stand_test.getStandWalls():
                            if intersectionHalf(center[0],center[1],point[0][0],point[0][1],stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3]):
                                I = intersectPointLine(center[0],center[1],np.arrray([point[0][0],point[0][1]])-np.array([center[0],center[1]]),stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3])
                                if dist>norm(I-np.array([center[0],center[1]])):
                                    dist = norm(I-np.array([center[0],center[1]]))
                                    point_inter = I
        if point[1] == "stand":
            n = 0 #nombre de murs de stand dans lequel notre point apparait
            for stand_wall in list_stand_walls:
                if point[2].getId() == stand_wall.getId():
                    n+=1
            if n == 1:
                for wall in shop.getWalls():
                    if intersectionHalf(center[0],center[1],point[0][0],point[0][1],wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3]):
                        I = intersectPointLine(center[0],center[1],np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]),wall.getPos()[0],wall.getPos()[1],wall.getPos()[2],wall.getPos()[3])
                        if dist> norm(I-np.array([center[0],center[1]])) and np.dot(I-np.array(center[0],center[1]),np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]))>0:
                            dist = norm(I - np.array([center[0], center[1]]))
                            point_inter = I
                for stand_test in shop.getStands():
                    if stand_test.getId()!=stand_test.getId():
                        for stand_wall in stand_test.getStandWalls():
                            if stand_wall.getId()!=point[2].getId():
                                if intersectionHalf(center[0],center[1],point[0][0],point[0][1],stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3]):
                                    I = intersectPointLine(center[0],center[1],np.arrray([point[0][0],point[0][1]])-np.array([center[0],center[1]]),stand_wall.getPos()[0],stand_wall.getPos()[1],stand_wall.getPos()[2],stand_wall.getPos()[3])
                                    if dist > norm(I - np.array([center[0], center[1]])) and np.dot(I-np.array(center[0],center[1]),np.array([point[0][0],point[0][1]])-np.array([center[0],center[1]]))>0:
                                        dist = norm(I - np.array([center[0], center[1]]))
                                        point_inter = I
        if dist!= inf:
            other_points.append([point_inter,0,0])


    return poly+other_points

def unobstructed_stand_wall(pointStand,pointWall,stand,wall,shop):#regarde si dans le magasin il y a une intersection entre le point sur stand et le point sur wall
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


###
def creation_fenetre_fov(shop):
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
    Meubles_test = [Stand(0,0,25,50), Stand(150,150,290,180)]
    Clients_test = [Client(45,78,3,4,6), Client(187,23,7,7,7)]


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
        Shop_test.addClient(client)



    creation_fenetre_fov(Shop_test)
    affichage_magasin(Shop_test, magasin)

    points = field_of_view(Shop_test.getStands()[0], Shop_test)
    for point in points:
        magasin.create_oval(point[0][0] + 5, point[0][1] + 5, point[0][0] + 15, point[0][1] + 15, fill='green')


    root.mainloop()

