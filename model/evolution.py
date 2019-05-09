from model.environnement import Wall,StandWall,Shop,Stand,Customer,Entry,Exit
from model.static_graphic_display import store_display, customers_display
from model.utils import norm
from model.forces import exterior_forces, customers_exit
import numpy as np
from model import builder
from tkinter import Tk, Canvas
import random as rd
import time



def representation_evolution(shop, dt, T):
    """
    Fonction that displays and computes the evolution of the system
    :param shop: (Shop) The shop considered
    :param dt: (float) Time step
    :param T: (float) Time frame considered
    """

    # Constants
    t = 0
    F_0 = 10
    F_wall0 = 1000
    d_0 = 1
    F_stand0 = F_wall0/4
    F_exit = 10
    v_max = 4
    lambd = 1/2
    beta_customer = 10
    beta_wall = 10

    # Windows creation
    root = Tk()
    root.title('Magasin')

    murs = shop.getWalls()

    x_max = 0
    y_max = 0
    for mur in murs:
        coord = mur.getPos()
        if coord[0] > x_max:
            x_max = coord[0]
        if coord[2] > x_max:
            x_max = coord[2]
        if coord[1] > y_max:
            y_max = coord[1]
        if coord[3] > y_max:
            y_max = coord[3]


    magasin = Canvas(root, width=x_max+15, height=y_max+15)
    magasin.pack()

    # Display the shop
    store_display(shop, magasin)

    # Display the customers' starting point and retrieves the list of clients
    balls_list, lines_list = customers_display(shop, magasin, False)

    i = 0
    while t < T:
        if i%10 == 0 and i != 0:
            shop.addCustomer(Customer(210, 5, 0, 4, 6))
            balls_list.append(magasin.create_oval(215, 10, 225, 20, fill='green'))
        # Calculation of the next position of each customer
        for customer in shop.getCustomers():

            dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)
            pos = customer.getPos()
            speed = customer.getSpeed()

            if norm(speed+dv) < v_max:
                customer.setSpeed(speed+dv)
            else:
                customer.setSpeed(((speed+dv)/norm(speed+dv))*v_max)

            customer.setPos(pos+dt*(speed+dv))

            # Movement of the customers
            if balls_list[customer.getId()] is not None:
                pos = customer.getPos()
                speed = customer.getSpeed()
                magasin.coords(balls_list[customer.getId()], pos[0]+5, pos[1]+5, pos[0]+15, pos[1]+15)
                if lines_list:
                    magasin.coords(lines_list[customer.getId()], pos[0]+10, pos[1]+10, pos[0]+5*speed[0]+10, pos[1]+5*speed[1]+10)
                customers_exit(shop, magasin, balls_list, lines_list, x_max, y_max)
            root.update()
            time.sleep(.01)
            # if i%3 == 0:
            #     magasin.postscript(file="C:\\Users\\coren\\Desktop\\Matieres\\Projet_Mouvement_Foule\\Programme_git\\images\\image{}.ps".format(i), colormode='color')
            # i += 1
        t += dt
        i += 1
    root.mainloop()


def evolution_list(shop, T, dt, lambd, d_0, F_wall0, F_stand0, F_0, v_max, F_exit, beta_customer, beta_wall):
    """"
    Function that computes the evolution of the system and returns the trajectories of the clients
    :param shop: (Shop) Shop considered
    :param T: (float) Time frame considered
    :param dt: (float) Time step
    :param lambd: (function) Function that characterises the repulsion of the walls
    :param d_0: (float) Diameter of a person
    :param F_wall0: (float) Module of the forces exerted by the walls
    :param F_stand0: (float) Module of the forces exerted by the stands
    :param F_0: (float) Coefficient applied to the social force
    :param v_max: (float) Module of the maximum speed of the customer
    :param F_exit: (float) Coefficient applied to the force linked with the exit
    :param beta_customer: (float) Coefficient in the exponential when computing the social force
    :param beta_wall: (float) Coefficient in the exponential when computing the wall force
    :return: (list) List of the positions of all the clients over time
    """

    t = 0
    syst = {}
    for customer in shop.getCustomers():
        syst[customer.getId()] = []

    while t < T:
        # Calculation of the next position of each customer
        for customer in shop.getCustomers():
            syst[customer.getId()] += [customer.getPos()[0], customer.getPos()[1]]

            dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)
            pos = customer.getPos()
            speed = customer.getSpeed()

            if norm(speed+dv) < v_max:
                customer.setSpeed(speed + dv)
            else:
                customer.setSpeed(((speed + dv)/norm(speed + dv))*v_max)
            customer.setPos(pos+dt*speed+dt*dv)
        t += dt
    return syst

def one_client(shop, experience_list, T, dt, lambd, d_0, F_wall0, F_stand0, F_0, v_max, F_exit, beta_customer, beta_wall):
    """"
    Function that computes the evolution of the system and returns the trajectories of the clients
    :param shop: (Shop) Shop considered, without clients
    :param T: (float) Time frame considered
    :param dt: (float) Time step
    :param lambd: (function) Function that characterises the repulsion of the walls
    :param d_0: (float) Diameter of a person
    :param F_wall0: (float) Module of the forces exerted by the walls
    :param F_stand0: (float) Module of the forces exerted by the stands
    :param F_0: (float) Coefficient applied to the social force
    :param v_max: (float) Module of the maximum speed of the customer
    :param F_exit: (float) Coefficient applied to the force linked with the exit
    :param beta_customer: (float) Coefficient in the exponential when computing the social force
    :param beta_wall: (float) Coefficient in the exponential when computing the wall force
    :return: (list) List of the positions of all the clients over time
    """

    t = 0
    syst = {}
    for customer in shop.getCustomers():
        syst[customer.getId()] = []

    while t < T:
        # Calculation of the next position of each customer
        for customer in shop.getCustomers():
            syst[customer.getId()] += [customer.getPos()[0], customer.getPos()[1]]

            dv = dt * exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer,
                                      beta_wall)
            pos = customer.getPos()
            speed = customer.getSpeed()

            if norm(speed + dv) < v_max:
                customer.setSpeed(speed + dv)
            else:
                customer.setSpeed(((speed + dv) / norm(speed + dv)) * v_max)
            customer.setPos(pos + dt * speed + dt * dv)
        t += dt
    return syst

if __name__ == '__main__':

    T = 150
    v_max = 4

    # Walls_test = [Wall(0, 0, 0, 200), Wall(0, 200, 300, 200), Wall(300, 200, 300, 0), Wall(300, 0, 0, 0)]
    # Entries_test = [Entry(200, 0, 245, 0, 45), Entry(150, 200, 180, 200, 45)]
    # Exits_test = [Exit(0, 100, 0, 150), Exit(150, 200, 180, 200)]
    Stands_test = [Stand(0, 0, 25, 50), Stand(150, 100, 250, 130)]
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
