from flux_magasin.model.environnement import *

def builder(list):
    shop = Shop("Magasin")
    i = 0
    while i<len(list)-1:
        if list[i+1] not in ["entree","sortie","entree_sortie"]:
            shop.addWall(Wall(list[i][0],list[i][1],list[i+1][0],list[i+1][1]))
            i+=1
        elif list[i+1] == "entree":
            print("caca")