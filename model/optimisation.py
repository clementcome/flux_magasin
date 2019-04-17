from flux_magasin.model.evolution import  *

T = 150
v_max = 4
F_0 = 10
F_wall0 = 15
d_0 = 1
F_stand0 = F_wall0 / 4
dt = 1

Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
Entrees_test = [Entry(200,0,245,0,45), Entry(150,200,180,200,45)]
Sorties_test = [Exit(0,100,0,150), Exit(150,200,180,200)]
Meubles_test = [Stand(0,0,25,50), Stand(150,150,250,180)]
Clients_test = [Client(210,5,0,4,6), Client(220,10,-0,4,6), Client(225,6,-0,3,6)]

print(type(Clients_test))

shop = Shop('test')

shop.addWall(Murs_test)
for stand in Meubles_test:
    shop.addStand(stand)
for entry in Entrees_test:
    shop.addEntry(entry)
for exit in Sorties_test:
    shop.addExit(exit)
for client in Clients_test:
    shop.addClient(client)

print(evolution_list(shop,T, dt,lambd,d_0,F_wall0,F_stand0,F_0, v_max))