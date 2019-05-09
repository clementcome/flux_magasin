from model.environnement import Wall,StandWall,Shop,Stand,Client,Entry,Exit
from model.representation_graphique_statique import affichage_magasin, affichage_clients
from model.utils import norm
from model.forces import exteriorForces
import numpy as np
from model import builder
from tkinter import Tk, Canvas
import random as rd
import time



def representation_evolution(shop, dt, T):
    '''
    Fonction that displays and computes the evolution of the system
    :param shop: (Shop) The shop considered
    :param dt: (float) Time step
    :param T: (float) Time frame considered
    '''
    t = 0
    F_0 = 10
    F_wall0 = 400
    d_0 = 1
    F_stand0 = F_wall0
    F_exit = 1
    v_max = 4

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
    liste_boules, liste_lignes = affichage_clients(shop, magasin, True)

    # i = 0
    while t < T:
        #Calcul de la position suivante des clients
        for client in shop.getClients():

            dv = dt*exteriorForces(client, shop,lambda x : np.exp(-x**0.4),d_0,F_wall0,F_stand0,F_0, F_exit)
            pos = client.getPos()
            speed = client.getSpeed()
            if norm(speed+dv)<v_max:
                client.setSpeed(speed + dv)
            else:
                client.setSpeed(((speed + dv)/norm(speed + dv))*v_max)
            #print(norm(speed))
            client.setPos(pos+dt*speed+dt*dv)
            pos = client.getPos()

            #Déplacement des clients
            magasin.coords(liste_boules[client.getId()], pos[0]+5, pos[1]+5, pos[0]+15, pos[1]+15)
            speed = client.getSpeed()
            magasin.coords(liste_lignes[client.getId()], pos[0]+10, pos[1]+10, pos[0]+5*speed[0]+10, pos[1]+5*speed[1]+10)
            root.update()
            time.sleep(.01)
            # if i%3 == 0:
            #     magasin.postscript(file="C:\\Users\\coren\\Desktop\\Matieres\\Projet_Mouvement_Foule\\Programme_git\\images\\image{}.ps".format(i), colormode='color')
            # i += 1
        t += dt
    root.mainloop()

def evolution_list(shop,T, dt,lambd,d_0,F_wall0,F_stand0,F_0, v_max, F_exit):
    '''
    Fonction that computes the evolution of the system and returns the trajectories of the clients
    :param shop: (Shop) Shop considered
    :param T: (float) Time frame considered
    :param dt: (float) Time step
    :param lambd: (function) Fuction that caracterises the repultion of the walls
    :param d_0: (float) Diameter of a person
    :param F_wall0: (float) Module of the forces exerted by the walls
    :param F_stand0: (float) Module of the forces exerted by the stands
    :param F_0: (float) Coefficient applied to the social force
    :param v_max: (float) Module of the maximum speed of the client
    :param F_exit: (float) Coefficient applied to the force linked with the exit
    :return: (list) List of the positions of all the clients over time
    '''
    t = 0
    syst = {}
    for client in shop.getClients():
        syst[client.getId()] = []

    while t < T:
        #Calcul de la position suivante des clients
        for client in shop.getClients():
            syst[client.getId()] = syst[client.getId()] + [client.getPos()[0],client.getPos()[1]]

            dv = dt*exteriorForces(client,shop,lambd,d_0,F_wall0,F_stand0,F_0, F_exit)
            pos = client.getPos()
            speed = client.getSpeed()
            if norm(speed+dv)<v_max:
                client.setSpeed(speed + dv)
            else:
                client.setSpeed(((speed + dv)/norm(speed + dv))*v_max)
            #print(norm(speed))
            client.setPos(pos+dt*speed+dt*dv)

        t += dt
    return syst

if __name__ == '__main__':

    T = 150
    v_max = 4

    #Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
    #Entrees_test = [Entry(200,0,245,0,45), Entry(150,200,180,200,45)]
    #Sorties_test = [Exit(0,100,0,150), Exit(150,200,180,200)]
    Meubles_test = [Stand(0,0,25,50), Stand(150,100,250,130)]
    Clients_test = [Client(210,5,0,4,6), Client(220,10,-0,4,6), Client(225,6,-0,3,6)]


    Shop_test = builder([[0,0],[0,100],"sortie",[0,150],[0,200],[150,200],"entree_sortie",[180,200],[300,200],[300,0],[200,0],"entree",[245,0],[0,0]],45)
    #Shop_test.addWall(Murs_test)
    Shop_test.addStand(Meubles_test)
    #Shop_test.addEntry(Entrees_test)
    #Shop_test.addExit(Sorties_test)
    Shop_test.addClient(Clients_test)

    representation_evolution(Shop_test, 1, T)