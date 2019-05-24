from model.environnement import Wall, StandWall, Shop, Stand, Customer, Entry, Exit
import numpy as np
import matplotlib.pyplot as plt
import skfmm
from math import inf


def builder(walls_list, flux, stands_list):
    """
    Returns a shop built with the points in the list
    :param walls_list: (list) List of the coordinates of the walls, and the entries/exits
    :param flux: (float) Flux of the entries
    :param stands_list: list of the stands in the shop
    :return: (Shop) The shop built with theses components
    """

    shop = Shop("Magasin")

    i = 0
    while i < len(walls_list)-1:
        if walls_list[i+1] not in ["entree", "sortie", "entree_sortie"]:
            shop.addWall(Wall(walls_list[i][0], walls_list[i][1], walls_list[i+1][0], walls_list[i+1][1]))
            i += 1
        elif walls_list[i+1] == "entree":
            shop.addEntry(Entry(walls_list[i][0], walls_list[i][1], walls_list[i+2][0], walls_list[i+2][1], flux))
            i += 2
        elif walls_list[i+1] == "sortie":
            shop.addExit(Exit(walls_list[i][0], walls_list[i][1], walls_list[i+2][0], walls_list[i+2][1]))
            i += 2
        elif walls_list[i+1] == "entree_sortie":
            shop.addEntry(Entry(walls_list[i][0], walls_list[i][1], walls_list[i + 2][0], walls_list[i + 2][1], flux))
            shop.addExit(Exit(walls_list[i][0], walls_list[i][1], walls_list[i + 2][0], walls_list[i + 2][1]))
            i += 2

    for stand in stands_list:
        shop.addStand(stand)

    shop.calculate_x_y_max()

    return shop


def matrix_representation_for_fast_marching(shop):

    list_masked = []
    x_max = shop.get_x_max()
    y_max = shop.get_y_max()
    X, Y = np.meshgrid(np.linspace(0, x_max, x_max+1), np.linspace(0, y_max, y_max+1))
    phi = -1 * np.ones((y_max+1, x_max+1))

    for stand in shop.getStands():
        x1, y1, x2, y2 = stand.getPos()
        mask = np.logical_and(np.logical_and(x2 < X, X < x1), np.logical_and(y2 < Y, Y < y1))
        phi = np.ma.MaskedArray(phi, mask)

    return phi

