from model import builder
from model.environnement import Stand,Customer
from model.evolution import representation_evolution


T = 300

# Walls_test = [Wall(0, 0, 0, 200), Wall(0, 200, 300, 200), Wall(300, 200, 300, 0), Wall(300, 0, 0, 0)]
# Entries_test = [Entry(200, 0, 245, 0, 45), Entry(150, 200, 180, 200, 45)]
# Exits_test = [Exit(0, 100, 0, 150), Exit(150, 200, 180, 200)]
Stands_test = [Stand(0, 0, 25, 50), Stand(150, 150, 250, 180)]
Customers_test = [Customer(210, 5, 0, 4, 6), Customer(220, 10, -0, 4, 6), Customer(225, 6, -0, 3, 6)]


Shop_test = builder([[0, 0],
                     [0, 100], "sortie", [0, 150],
                     [0, 200],
                     [150, 200], "entree_sortie", [180, 200],
                     [300, 200], [300, 0],
                     [245, 0], "entree", [200, 0],
                     [0, 0]], 45)
# Shop_test.addWall(Walls_test)
Shop_test.addStand(Stands_test)
# Shop_test.addEntry(Entries_test)
# Shop_test.addExit(Exits_test)
Shop_test.addCustomer(Customers_test)


representation_evolution(Shop_test, 1, T)

##optimisation
Shop_test_one_client = builder([[0, 0],
                     [0, 100], "sortie", [0, 150],
                     [0, 200],
                     [150, 200], "entree_sortie", [180, 200],
                     [300, 200], [300, 0],
                     [245, 0], "entree", [200, 0],
                     [0, 0]], 45)
Shop_test_one_client.addCustomer(Customers_test)