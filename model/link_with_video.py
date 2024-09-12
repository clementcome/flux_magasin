from model import builder
from tkinter import Tk, Canvas
from math import inf
from model.static_graphic_display import store_display, customers_display
from model.environnement import Stand,Customer, Exit
from model.evolution import representation_evolution,one_client, fast_marching_to_exit, evolution_list
import json
import skfmm

def window_creation_test(shop):
    """
    Create the Tkinter window and canvas in which we will display the shop
    :param shop: (Shop) the shop to display
    :return: None
    """
    global root
    root = Tk()
    root.title('Shop')

    # Search the size of the window we should use
    walls = shop.getWalls()
    x_max = 0
    y_max = 0
    for wall in walls:
        coord = wall.getPos()
        if coord[0] > x_max:
            x_max = coord[0]
        if coord[2] > x_max:
            x_max = coord[2]
        if coord[1] > y_max:
            y_max = coord[1]
        if coord[3] > y_max:
            y_max = coord[3]


    global store
    store = Canvas(root, width=x_max + 15, height=y_max + 15)
    store.pack()


def shop_and_data(path):
    with open(path, "r") as inputfile:
        data = json.load(inputfile)
    x_min = inf
    x_max = -inf
    y_min = inf
    y_max = -inf
    for client_time in data["li_real_positions"]:
        for client in client_time:
            if client[0]<x_min:
                x_min = client[0]
            if client[0]>x_max:
                x_max = client[0]
            if client[1]<y_min:
                y_min = client[1]
            if client[1]>y_max:
                y_max = client[1]
    for client_time_ind in range(len(data["li_real_positions"])):
        for i in range(len(data["li_real_positions"][client_time_ind])):
            data["li_real_positions"][client_time_ind][i][0] = data["li_real_positions"][client_time_ind][i][0] - x_min
            data["li_real_positions"][client_time_ind][i][1] = data["li_real_positions"][client_time_ind][i][1] - y_min
    x_max = x_max - x_min
    y_max = y_max - y_min
    x_min = 0
    y_min = 0

    Shop = builder([[x_min,y_min],[x_max,y_min],[x_max,y_max],[x_min,y_max],[x_min,y_min]],1,[])
    return [Shop, data["li_real_positions"]]
