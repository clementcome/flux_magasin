from model import builder
from model.environnement import Stand,Customer
from model.evolution import representation_evolution, evolution_list


T = 1000

# Walls_test = [Wall(0, 0, 0, 200), Wall(0, 200, 300, 200), Wall(300, 200, 300, 0), Wall(300, 0, 0, 0)]
# Entries_test = [Entry(200, 0, 245, 0, 45), Entry(150, 200, 180, 200, 45)]
# Exits_test = [Exit(0, 100, 0, 150), Exit(150, 200, 180, 200)]
Stands_test = [Stand(0, 0, 25, 50), Stand(100, 100, 120, 160)]
Customers_test = [Customer(210, 5, 0, 4), Customer(220, 10, -0, 4), Customer(225, 6, -0, 3)]


Shop_test = builder([[0, 0],
                     [0, 100], "sortie", [0, 150],
                     [0, 200],
                     [150, 200], "entree", [180, 200],
                     [300, 200], [300, 0],
                     [245, 0], "entree", [200, 0],
                     [0, 0]], 4)
# Shop_test.addWall(Walls_test)
Shop_test.addStand(Stands_test)
# Shop_test.addEntry(Entries_test)
# Shop_test.addExit(Exits_test)
Shop_test.addCustomer(Customers_test)


evolution_list(Shop_test, T, 0.1, 1/2, 1, 200, 50, 10, 4, 10, 10, 10)

##optimisation
Shop_test_one_client = builder([[0, 0],
                     [0, 100], "sortie", [0, 150],
                     [0, 200],
                     [150, 200], "entree_sortie", [180, 200],
                     [300, 200], [300, 0],
                     [245, 0], "entree", [200, 0],
                     [0, 0]], 45)
Shop_test_one_client.addCustomer(Customers_test)
