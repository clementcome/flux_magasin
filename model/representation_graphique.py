from tkinter import *
from flux_magasin.model.environnement import *

def creation_fenetre(shop):
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


def affichage_magasin(murs, meubles, entrees, sorties, canevas):
    for meuble in meubles:
        coord = meuble.getPos()
        canevas.create_rectangle(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, fill='purple')

    for mur in murs:
        coord = mur.getPos()
        canevas.create_line(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, width=10, capstyle='projecting')

    for entree in entrees:
        coord = entree.getPos()
        canevas.create_line(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, width=10, fill='blue')

    for sortie in sorties:
        coord = sortie.getPos()
        canevas.create_line(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, width=10, fill='red')


def affichage_clients(clients, canevas, direction=False):

    for client in clients:
        coord = client.getPos()
        canevas.create_oval(coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15, fill='green')
        if direction:
            vitesse = client.getSpeed()
            canevas.create_line(coord[0]+10, coord[1]+10, coord[0]+5*vitesse[0]+10, coord[1]+5*vitesse[1]+10, fill='green', arrow='last')


Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
Entrees_test = Entry(0,100,0,150,45)
Sorties_test = Exit(200,0,250,0)
Meubles_test = [Stand(0,0,25,50), Stand(150,150,250,180)]
Clients_test = [Client(45,78,3,4,6), Client(187,23,7,7,7)]

Shop_test = Shop('test')
for wall in Murs_test:
    Shop_test.addWall(wall)
for stand in Meubles_test:
    Shop_test.addStand(stand)
Shop_test.updateEntry(Entrees_test)
Shop_test.updateExit(Sorties_test)


creation_fenetre(Shop_test)
affichage_magasin(Murs_test, Meubles_test, Entrees_test, Sorties_test, magasin)
affichage_clients(Clients_test, magasin)
root.mainloop()
