from flux_magasin.model.environnement import * #importé de cette façon et pas avec import flux_magasin.model.environnement, qui rendrait claque appel de mur illisible

wall1 = Wall(1,2,3,4)

shop = Shop("Zara")
shop.addWall(wall1)
print(shop.getWalls()[0].getPos())