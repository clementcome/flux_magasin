from model.environnement import Wall,StandWall,Shop,Stand,Customer,Entry,Exit
from model.static_graphic_display import store_display, customers_display
from model.utils import norm
from model.forces import exterior_forces, customers_exit
from model import builder, matrix_representation_for_fast_marching
from tkinter import Tk, Canvas
import time
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import skfmm


COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2']


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
    F_wall0 = 200
    d_0 = 1
    F_stand0 = F_wall0/4
    F_exit = 10
    v_max = 4
    lambd = 1/2
    beta_customer = 10
    beta_wall = 10

    nb_exit_wall = 0
    nb_exit_legal = 0
    nb_enter = 0
    flow = shop.getEntries()[0].getFlow()

    # Windows creation
    root = Tk()
    root.title('Magasin')

    murs = shop.getWalls()

    shop.calculate_x_y_max()
    x_max = shop.get_x_max()
    y_max = shop.get_y_max()

    magasin = Canvas(root, width=x_max+15, height=y_max+15)
    magasin.pack()

    # Display the shop
    store_display(shop, magasin)

    # Display the customers' starting point and retrieves the list of clients
    balls_list, lines_list = customers_display(shop, magasin, False)
    nb_enter += len(balls_list)

    # Fast marching algorithm
    Exits = shop.getExits()
    phi = matrix_representation_for_fast_marching(shop)
    for exit in Exits:
        directions = fast_marching_to_exit(phi, exit, shop)

    new_directions = np.zeros((len(directions[0]), len(directions), 2))
    for i in range(len(directions)):
        for j in range(len(directions[0])):
            new_directions[j,i] = directions[i,j]
    directions = new_directions

    i = 0
    while t < T:

        # New customers entering
        if i % flow == 0 and i != 0:
            for entry in shop.getEntries():
                entry_pos = entry.getPos()
                x = rd.uniform(entry_pos[0], entry_pos[2])
                y = rd.uniform(entry_pos[1], entry_pos[3])
                v_x = rd.uniform(-4, 4)
                v_y = rd.uniform(-4, 4)
                shop.addCustomer(Customer(x, y, v_x, v_y))
                nb_enter += 1
                balls_list.append(magasin.create_oval(x + 5, y + 5, x + 15, y + 15, fill=rd.choice(COLORS)))

        # Calculation of the next position of each customer
        for customer in shop.getCustomers():

            pos = customer.getPos()
            if 0 < pos[0] and pos[0] < x_max and 0 < pos[1] and pos[1] < y_max:
                dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)+.5*directions[int(pos[0]), int(pos[1])]
            else:
                dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)
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
                    magasin.coords(lines_list[customer.getId()], pos[0]+10, pos[1]+10, pos[0]+5*speed[0]+10, pos[1]+10*speed[1]+10)
                nb_exit_wall, nb_exit_legal = customers_exit(shop, balls_list, lines_list, x_max, y_max, nb_exit_wall, nb_exit_legal, magasin)
            root.update()
            # if i%3 == 0:
            #     magasin.postscript(file="C:\\Users\\coren\\Desktop\\Matieres\\Projet_Mouvement_Foule\\Programme_git\\images\\image{}.ps".format(i), colormode='color')
            # i += 1
        t += dt
        i += 1
    root.mainloop()
    print(nb_exit_wall, 'people escaped through a wall.')
    print(nb_exit_legal, 'people exited legally.')
    print(nb_enter, 'people entered.')


def evolution_list(shop, T, dt, lambd, d_0, F_wall0, F_stand0, F_0, v_max, F_exit, beta_customer, beta_wall, coef_fast_marching):
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
    :param coef_fast_marching: (float) Coefficient applied to the wanted speed calculated with the fast marching algorithm
    :return: (list) List of the positions of all the clients over time
    """

    nb_exit_wall = 0
    nb_exit_legal = 0
    nb_enter = 0

    x_max = shop.get_x_max()
    y_max = shop.get_y_max()

    # Fast marching algorithm
    Exits = shop.getExits()
    phi = matrix_representation_for_fast_marching(shop)
    for exit in Exits:
        directions = fast_marching_to_exit(phi, exit, shop)

    new_directions = np.zeros((len(directions[0]), len(directions), 2))
    for i in range(len(directions)):
        for j in range(len(directions[0])):
            new_directions[j,i] = directions[i,j]
    directions = new_directions

    t = 0
    syst = {}
    for customer in shop.getCustomers():
        nb_enter += 1
        syst[customer.getId()] = []

    while t < T:
        # Calculation of the next position of each customer
        for customer in shop.getCustomers():
            syst[customer.getId()] += [[customer.getPos()[0], customer.getPos()[1]]]
            pos = customer.getPos()

            if 0 < pos[0] and pos[0] < x_max and 0 < pos[1] and pos[1] < y_max:
                dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)+coef_fast_marching*directions[int(pos[0]), int(pos[1])]
            else:
                dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)
            pos = customer.getPos()
            speed = customer.getSpeed()

            if norm(speed+dv) < v_max:
                customer.setSpeed(speed + dv)
            else:
                customer.setSpeed(((speed + dv)/norm(speed + dv))*v_max)
            customer.setPos(pos+dt*speed+dt*dv)
        nb_exit_wall, nb_exit_legal = customers_exit(shop, [], [], x_max, y_max, nb_exit_wall, nb_exit_legal)
        t += dt
    print(nb_exit_wall, 'people escaped through a wall.')
    print(nb_exit_legal, 'people exited legally.')
    print(nb_enter, 'people entered.')
    return syst


def one_client(shop, experience_list, dt, lambd, d_0, F_wall0, F_stand0, F_0, F_exit, beta_customer, beta_wall, coef_fast_marching):
    """"
    Function that computes the evolution of the system and returns the trajectories of the clients. Only the movement of the first client is modeled by our algorithm, the movement of the other clients is modeled by data
    :param shop: (Shop) Shop considered, without clients
    :param experience_list: (list) List returned by the experience, with the coordinates of all the clients at all the times. The first client is the one that will be modeled by our model
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
    :param coef_fast_marching: (float) Coefficient applied to the wanted speed calculated with the fast marching algorithm
    :return: (list) List of the positions of all the clients over time
    """
    #Removing the clients in the shop if there are any
    if len(shop.getCustomers())!=0:
        customers = shop.getCustomers()
        for customer in customers:
            shop.removeCustomer(customer)
    #Adding the clients
    id_list = []

    customer_test = Customer(experience_list[0][0][0],experience_list[0][0][1],(experience_list[1][0][0]-experience_list[0][0][0])/dt,(experience_list[1][0][1]-experience_list[0][0][1])/dt)
    shop.addCustomer(customer_test)
    id_list.append(customer_test.getId())
    ind_client_considered = 0

    for i in range(1,len(experience_list[0])):
        customer = Customer(experience_list[0][i][0],experience_list[0][i][1],(experience_list[1][i][0]-experience_list[0][i][0])/dt,(experience_list[1][i][1]-experience_list[0][i][1])/dt)
        shop.addCustomer(customer)
        id_list.append(customer.getId())

    # Fast marching algorithm
    Exits = shop.getExits()
    phi = matrix_representation_for_fast_marching(shop)
    for exit in Exits:
        directions = fast_marching_to_exit(phi, exit, shop)

    new_directions = np.zeros((len(directions[0]), len(directions), 2))
    for i in range(len(directions)):
        for j in range(len(directions[0])):
            new_directions[j,i] = directions[i,j]
    directions = new_directions

    t = 0
    ind = 1
    syst = {}
    for customer in shop.getCustomers():
        syst[customer.getId()] = []

    x_max = int(shop.get_x_max())
    y_max = int(shop.get_y_max())

    while ind < len(experience_list[0])-1:
        # Calculation of the next position of each customer
        for i in range(id_list):
            customer = shop.getCustomerById(id_list[i])
            syst[customer.getId()] += [customer.getPos()[0], customer.getPos()[1]]

            if id_list[i] == customer_test.getId():
                pos = customer.getPos()
                speed = customer.getSpeed()
                if 0 < pos[0] and pos[0] < x_max and 0 < pos[1] and pos[1] < y_max:
                    dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)+coef_fast_marching*directions[int(pos[0]), int(pos[1])]
                else:
                    dv = dt*exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0, F_exit, beta_customer, beta_wall)

                if norm(speed + dv) < v_max:
                    customer.setSpeed(speed + dv)
                else:
                    customer.setSpeed(((speed + dv) / norm(speed + dv)) * v_max)
                customer.setPos(pos + dt * speed + dt * dv)
            else:
                customer.setPos(experience_list[ind][i][0],experience_list[ind][i][1])
                customer.setSpeed((experience_list[ind+1][i][0]-experience_list[ind][i][0])/dt,(experience_list[ind+1][i][1]-experience_list[ind][i][1])/dt)

        ind += 1
    RMS = 0
    for i in range(len(syst[customer_test.getId()])):
        RMS += (norm([experience_list[i][ind_client_considered][0]-syst[customer_test.getId()][i][0],experience_list[i][ind_client_considered][1]-syst[customer_test.getId()][i][1]]))**2
    return np.sqrt((1/len(syst[customer_test.getId()]))*RMS)

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



def fast_marching_to_exit(phi, exit, shop):
    x1, y1, x2, y2 = exit.getPos()
    x_max = shop.get_x_max()
    y_max = shop.get_y_max()
    x_min = shop.get_x_min()
    y_min = shop.get_y_min()

    X, Y = np.meshgrid(np.linspace(0, x_max-x_min, x_max-x_min+1), np.linspace(0, y_max-y_min, y_max-y_min+1))

    phi[np.logical_and(np.logical_and(x1-3 < X, X < x2+3), np.logical_and(y1-3 < Y, Y < y2+3))] = 1

    d = skfmm.distance(phi, dx=1e-4)
    s = 0
    directions = np.zeros((y_max-y_min+1, x_max-x_min+1, 2))
    for i in range(1, len(d)-1):
        for j in range(1, len(d[0])-1):
            distance_min = d[i, j]
            grad = [0, 0]
            for k, l in [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i, j+1], [i+1, j], [i+1, j-1], [i+1, j+1]]:
                if d[k, l] <= distance_min:
                    grad = [k-i,j-l]
                    distance_min = d[k,l]
            directions[i, j] = grad

    return directions


def fast_marching_to_exit_with_display(phi, exit, shop):
    x1, y1, x2, y2 = exit.getPos()
    x_max = shop.get_x_max()
    y_max = shop.get_y_max()
    X, Y = np.meshgrid(np.linspace(0, x_max, x_max+1), np.linspace(0, y_max, y_max+1))

    phi[np.logical_and(np.logical_and(x1-3 < X, X < x2+3), np.logical_and(y1-3 < Y, Y < y2+3))] = 1

    d = skfmm.distance(phi, dx=1e-4)
    s = 0
    directions = np.zeros((y_max+1, x_max+1, 2))
    for i in range(1, len(d)-1):
        for j in range(1, len(d[0])-1):
            distance_min = d[i, j]
            grad = [0, 0]
            for k, l in [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i, j+1], [i+1, j], [i+1, j-1], [i+1, j+1]]:
                if d[k, l] <= distance_min:
                    grad = [k-i,j-l]
                    distance_min = d[k,l]
            directions[i, j] = grad

    plt.figure()
    for i in range(1, len(d)-2):
        if i % 10 == 1:
            for j in range(1, len(d[0])-2):
                if j % 10 == 1:
                    plt.quiver(j, i, directions[i, j, 1], directions[i, j, 0])
                    print(i, j, directions[i,j])

    plt.imshow(d, cmap='Pastel1')
    plt.show()

    return directions
