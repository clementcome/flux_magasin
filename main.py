from model import builder, representation_evolution
from model.environnement import Stand,Customer


T = 300

#Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
#Entrees_test = [Entry(200,0,245,0,45), Entry(150,200,180,200,45)]
#Sorties_test = [Exit(0,100,0,150), Exit(150,200,180,200)]
Meubles_test = [Stand(0,0,25,50), Stand(150,150,250,180)]
Clients_test = [Customer(210,5,0,4,6), Customer(220,10,-0,4,6), Customer(225,6,-0,3,6)]


Shop_test = builder([[0,0],[0,100],"sortie",[0,150],[0,200],[150,200],"entree_sortie",[180,200],[300,200],[300,0],[245,0],"entree",[200,0],[0,0]],45)
#Shop_test.addWall(Murs_test)
Shop_test.addStand(Meubles_test)
#Shop_test.addEntry(Entrees_test)
#Shop_test.addExit(Sorties_test)
Shop_test.addCustomer(Clients_test)


representation_evolution(Shop_test, 1, T)
