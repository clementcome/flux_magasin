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

def creation_legende():
    window = Tk()
    window.title('Légende')

    canvas = Canvas(window)
    canvas.pack()

    canvas.create_line(30, 20, 60, 20, width=10, capstyle='projecting')
    canvas.create_text(110, 20, text='Mur')

    for i in range(5, 15):
        canvas.create_line(25, 50+i, 65, 50+i, width=1, fill='blue', dash=(1,1))
    canvas.create_text(110, 60, text='Entrée')

    for i in range(5, 15):
        canvas.create_line(25, 90+i, 65, 90+i, width=1, fill='red', dash=(1,1))
    canvas.create_text(110, 100, text='Sortie')

    for i in range(5, 15):
        canvas.create_line(25, 130+i, 65, 130+i, width=1, fill='blue', dash=(1,1))
        canvas.create_line(28, 130+i, 65, 130+i, width=1, fill='red', dash=(1,1))
    canvas.create_text(110, 140, text='Entrée et sortie')

    canvas.create_rectangle(28, 170, 58, 200, fill='purple')
    canvas.create_text(110, 185, text='Meuble')

    canvas.create_oval(38, 220, 48, 230, fill='green')
    canvas.create_text(110, 225, text='Client')

    window.mainloop()

def affichage_magasin(shop, canevas):

    meubles = shop.getStands()
    murs = shop.getWalls()
    entrees = shop.getEntry()
    sorties = shop.getExit()

    for meuble in meubles:
        coord = meuble.getPos()
        canevas.create_rectangle(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, fill='purple')

    for mur in murs:
        coord = mur.getPos()
        canevas.create_line(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, width=10, capstyle='projecting')

    for entree in entrees:
        coord = entree.getPos()
        canevas.create_line(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, width=10, fill='white')
    for sortie in sorties:
        coord = sortie.getPos()
        canevas.create_line(coord[0]+10, coord[1]+10, coord[2]+10, coord[3]+10, width=10, fill='white')

    for entree in entrees:
        coord = entree.getPos()
        if coord[0] == coord[2]:
            for i in range(5,15):
                canevas.create_line(coord[0]+i, coord[1]+10, coord[2]+i, coord[3]+10, width=1, fill='blue', dash=(1,1))
        elif coord[1] == coord[3]:
            for i in range(5,15):
                canevas.create_line(coord[0]+10, coord[1]+i, coord[2]+10, coord[3]+i, width=1, fill='blue', dash=(1,1))
    for sortie in sorties:
        coord = sortie.getPos()
        if coord[0] == coord[2]:
            for i in range(5,15):
                canevas.create_line(coord[0]+i, coord[1]+13, coord[2]+i, coord[3]+10, width=1, fill='red', dash=(1,1))
        elif coord[1] == coord[3]:
            for i in range(5,15):
                canevas.create_line(coord[0]+13, coord[1]+i, coord[2]+10, coord[3]+i, width=1, fill='red', dash=(1,1))

def affichage_clients(shop, canevas, direction=False):

    clients = shop.getClients()
    liste_boules = []
    for client in clients:
        coord = client.getPos()
        liste_boules.append(canevas.create_oval(coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15, fill='green'))
        if direction:
            vitesse = client.getSpeed()
            canevas.create_line(coord[0]+10, coord[1]+10, coord[0]+5*vitesse[0]+10, coord[1]+5*vitesse[1]+10, fill='green', arrow='last')
    return liste_boules




if __name__ == '__main__':

    Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
    Entrees_test = [Entry(200,0,245,0,45), Entry(150,200,180,200,45)]
    Sorties_test = [Exit(0,100,0,150), Exit(150,200,180,200)]
    Meubles_test = [Stand(0,0,25,50), Stand(150,150,250,180)]
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


    creation_fenetre(Shop_test)
    affichage_magasin(Shop_test, magasin)
    affichage_clients(Shop_test, magasin)
    root.mainloop()

    creation_legende()
