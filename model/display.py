from tkinter import Tk, Canvas
from model.static_graphic_display import store_display
import time
import matplotlib.pyplot as plt
import numpy as np


def display_comparison(real_trajectory, calculated_trajectory, other_trajectories, shop):
    T = len(calculated_trajectory)
    N = len(other_trajectories[0])
    for t in range(T):
        if len(other_trajectories[t]) > N:
            N = len(other_trajectories[t])
    shop.calculate_x_y_max()
    x_max, y_max = shop.get_x_max(), shop.get_y_max()

    # Windows creation
    root = Tk()
    root.title('Magasin')

    murs = shop.getWalls()

    store = Canvas(root, width=x_max+15, height=y_max+15)
    store.pack()

    # Display the shop
    store_display(shop, store)

    # Display the customers' starting point and retrieves the list of clients
    balls_list = {i: '' for i in range(N)}

    i = 0
    for customer in other_trajectories[0]:
        coord = customer
        balls_list[i] = store.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='grey')
        i += 1

    coord = real_trajectory[0]
    balls_list[N] = store.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='green')
    coord = calculated_trajectory[0]
    balls_list[N+1] = store.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='deep pink')

    # Movement of the customers

    for t in range(T):
        for i in range(len(other_trajectories[t])):
            if balls_list[i] != '':
                coord = other_trajectories[t][i]
                store.coords(balls_list[i], coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15)
            else:
                coord = other_trajectories[t][i]
                balls_list[i] = store.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='grey')
        coord = real_trajectory[t]
        store.coords(balls_list[N], coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15)
        coord = calculated_trajectory[t]
        store.coords(balls_list[N+1], coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15)

        root.update()
        time.sleep(.05)

    root.mainloop()


def display_trajectory(real_trajectory, calculated_trajectory, other_trajectories):
    plt.figure()
    T = [i for i in range(len(calculated_trajectory))]
    N = len(other_trajectories[0])
    for t in T:
        if len(other_trajectories[t]) > N:
            N = len(other_trajectories[t])
    Xx = [[] for j in range(N)]
    Xy = [[] for j in range(N)]
    Rx = []
    Ry = []
    Cx = []
    Cy = []
    for t in T:
        for i in range(len(other_trajectories[t])):
            Xx[i].append(other_trajectories[t][i][0])
            Xy[i].append(other_trajectories[t][i][1])
        Rx.append(real_trajectory[t][0])
        Cx.append(calculated_trajectory[t][0])
        Ry.append(real_trajectory[t][1])
        Cy.append(calculated_trajectory[t][1])

    plt.plot(Xx[0], Xy[0], 'grey', label='Trajectoires des autres personnes')
    for i in range(1, N):
        plt.plot(Xx[i], Xy[i], 'grey')
    plt.plot(Rx, Ry, 'navy', label='Trajectoire réelle')
    plt.plot(Cx, Cy, 'orangered', label='Trajectoire simulée')

    axes = plt.gca()
    axes.set_xlabel('X (en mètres)')
    axes.set_ylabel('Y (en mètres)')

    axes.xaxis.set_ticks([i for i in range(850) if i%200==0])
    axes.xaxis.set_ticklabels(['0', '5', '10', '15', '20', '25', '30'])
    axes.yaxis.set_ticks([i for i in range(400) if i%200==0])
    axes.yaxis.set_ticklabels(['0', '5', '10', '15', '20'])
    axes.set_aspect(1)

    plt.legend(loc=2)

    plt.show()


def display_ideal(shop, trajectory):
    plt.figure()
    plt.imshow(shop)
    X = []
    Y = []
    for i in range(len(trajectory)):
        X.append(trajectory[i][0])
        Y.append(trajectory[i][1])
    plt.plot(X,Y)
    plt.show()
