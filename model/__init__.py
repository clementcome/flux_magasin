from model.environnement import *

def builder(list,flux):
    shop = Shop("Magasin")
    i = 0
    while i<len(list)-1:
        if list[i+1] not in ["entree","sortie","entree_sortie"]:
            shop.addWall(Wall(list[i][0],list[i][1],list[i+1][0],list[i+1][1]))
            i+=1
        elif list[i+1] == "entree":
            shop.addEntry(Entry(list[i][0],list[i][1],list[i+2][0],list[i+2][1], flux))
            i+=2
        elif list[i+1] == "sortie":
            shop.addExit(Exit(list[i][0],list[i][1],list[i+2][0],list[i+2][1]))
            i+=2
        elif list[i+1] == "entree_sortie":
            shop.addEntry(Entry(list[i][0], list[i][1], list[i + 2][0], list[i + 2][1], flux))
            shop.addExit(Exit(list[i][0], list[i][1], list[i + 2][0], list[i + 2][1]))
            i += 2
    return shop