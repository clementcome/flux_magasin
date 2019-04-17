from environnement import Wall,StandWall,Shop,Stand,Client,Entry,Exit
# from forces import exteriorForces
from representation_graphique_statique import affichage_magasin, affichage_clients
from utils import norm
from tkinter import Tk, Canvas
import random as rd
import time
from forces import exteriorForces


def representation_evolution(shop, dt, T):
    t = 0

    #création fenêtre
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

    magasin = Canvas(root, width=x_max+15, height=y_max+15)
    magasin.pack()

    #Afficher le magasin
    affichage_magasin(shop, magasin)
    #Afficher le point de départ des clients et récupérer la liste des clients
    liste_boules = affichage_clients(shop, magasin)

    i = 0
    while t < T:
        #Calcul de la position suivante des clients
        for client in shop.getClients():
            dv = dt*exteriorForces(client, shop)
            pos = client.getPos()
            speed = client.getSpeed()
            if norm(speed+dv)<v_max:
                client.setSpeed(speed + dv)
            else:
                client.setSpeed(((speed + dv)/norm(speed + dv))*v_max)
            #print(norm(speed))
            client.setPos(pos+dt*speed+dt*dv)
            #Déplacement des clients
            magasin.move(liste_boules[client.getId()], speed[0], speed[1])
            root.update()
            #magasin.postscript(file="image{}.ps".format(i), colormode='color')
            i += 1
            time.sleep(.01)
        t += dt
    root.mainloop()


if __name__ == '__main__':

    T = 2000
    v_max = 4

    Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
    Entrees_test = [Entry(200,0,245,0,45), Entry(150,200,180,200,45)]
    Sorties_test = [Exit(0,100,0,150), Exit(150,200,180,200)]
    Meubles_test = [Stand(0,0,25,50), Stand(150,150,250,180)]
    Clients_test = [Client(200,78,0.8,0.8,6), Client(45,78,-0.9,0.8,6)]


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


    representation_evolution(Shop_test, 1, T)
