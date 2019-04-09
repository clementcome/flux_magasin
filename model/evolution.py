from flux_magasin.model.environnement import * #importé de cette façon et pas avec import flux_magasin.model.environnement, qui rendrait claque appel de mur illisible
import matplotlib.pyplot as plt

wall1 = Wall(1,2,3,4)

shop = Shop("Zara")

walls = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
stands = [Stand(0,0,25,50), Stand(150,150,250,180)]
clients = [Client(45,78,3,4,6), Client(187,23,7,7,7)]

for wall in walls:
    shop.addWall(wall)
for stand in stands:
    shop.addStand(stand)
for client in clients:
    shop.addClient(client)
shop.updateEntry(Entry(0,100,0,150,45))
shop.updateExit(Exit(200,0,250,0))

t = 0 #temps initial
dt = 0.1 #On calcule toutes les dt secondes
cnt = 0  #Initialisation du conteur
cntReset = 10 #on affiche toutes les cnt*dt secondes
T = 0.05 #durée de l'expérience

####

#zones de visibilité
####
while t<T:
    if cnt == cntReset:
        cnt = 0
        ##afficher

    #ajouter pour attendre dt
    t+=dt
    cnt+=1
print(id(shop),id(shop.getWalls()[0]),id(shop.getWalls()[1]),shop.getWalls()[1].getId())