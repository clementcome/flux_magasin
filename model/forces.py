import numpy as np
from model.environnement import Wall,StandWall,Shop,Stand,Customer,Entry,Exit
from model.intersections import intersectPointLine, intersectionSegDroite, inside
from model.utils import norm

# def lambd(x):
#     return np.exp(-x**0.3)

def exitForce(client,exit, F_exit):
    '''
    Computes the force exerted by the exits
    :param client: (Client) The client considered
    :param exit: (Exit) The exit considered
    :param F_exit: (float) Module of the force exerted by the exits
    :return: (array) Force exerted by the exit on the client
    '''
    xForce = (exit.x1+exit.x2)/2 -client.x
    yForce = (exit.y1+exit.y2)/2 -client.y
    vecClientMur = np.array([xForce,yForce])
    vecForce = F_exit*vecClientMur/norm(vecClientMur)
    return vecForce

def angle(customer1,customer2):
    return 0

def vision_coef(customer1, customer2, lambd):
    return lambd + (1-lambd)*(np.cos(angle(customer1,customer2))+1)/2
# def exteriorForces(customer,shop,lambd,d_0,F_wall0,F_stand0,F_0, F_exit):
#     """
#     Computes the forces applied to a client
#     :param customer: (Client) The client considered
#     :param shop:  (Shop) The shop
#     :param lambd: (function) Fuction that caracterises the repultion of the walls
#     :param d_0:  (float) Diameter of a client
#     :param F_wall0: (float) Module of the force exerted by a wall
#     :param F_stand0: (float) Module of the force exerted by a stand wall
#     :param F_0: (float) Module of the social force
#     :param F_exit: (float) Module of the force exerted by the exits
#     :return: (array) Force exerted by the shop on the client
#     """
#     forces = np.zeros(2)
#     wallForces = np.zeros(2)
#     wallCoef = 1
#     exitForces = np.zeros(2)
#
#     for otherCustomer in shop.getCustomers():
#         if otherCustomer.getId() != customer.getId():
#             forces = forces + F_0 * (np.array(customer.getPos()) - np.array(otherCustomer.getPos())) / abs(norm(np.array(customer.getPos()) - np.array(otherCustomer.getPos())) ** 2 - d_0 ** 2)
#
#     for wall in shop.getWalls():
#         if intersectionSegDroite(wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3], customer.getPos()[0], customer.getPos()[1], wall.getNormal()):
#             intersect = intersectPointLine(customer.getPos()[0], customer.getPos()[1], wall.getNormal(), wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3])
#             dist = norm(intersect - np.array([customer.getPos()[0], customer.getPos()[1]]))
#             wallCoef = wallCoef * (1-lambd(dist))
#             if np.vdot(wall.getNormal(), np.array([customer.getPos()[0], customer.getPos()[1]]) - intersect) > 0:
#                 wallForces = wallForces + lambd(dist) * F_wall0 * wall.getNormal()
#             else:
#                 wallForces = wallForces - lambd(dist) * F_wall0 * wall.getNormal()
#
#     for stand in shop.getStands():
#         for standWall in stand.getStandWalls():
#             if intersectionSegDroite(standWall.getPos()[0], standWall.getPos()[1], standWall.getPos()[2], standWall.getPos()[3],
#                                      customer.getPos()[0], customer.getPos()[1], standWall.getNormal()):
#                 intersect = intersectPointLine(customer.getPos()[0], customer.getPos()[1], standWall.getNormal(), standWall.getPos()[0],
#                                                standWall.getPos()[1], standWall.getPos()[2], standWall.getPos()[3])
#                 dist = norm(intersect - np.array([customer.getPos()[0], customer.getPos()[1]]))
#                 wallCoef = wallCoef * (1 - lambd(dist))
#                 if np.vdot(standWall.getNormal(), np.array([customer.getPos()[0], customer.getPos()[1]]) - intersect) > 0:
#                     wallForces = wallForces + lambd(dist) * F_stand0 * standWall.getNormal()
#                 else:
#                     wallForces = wallForces - lambd(dist) * F_stand0 * standWall.getNormal()
#
#     for exit in shop.exits:
#         exitForces += exitForce(customer, exit, F_exit)
#     return wallCoef * (forces + exitForces) + wallForces

def exterior_forces(customer, shop, lambd, F_0, d_0, F_wall0, F_stand0 , F_exit, beta_customer, beta_wall):
    forces = np.zeros(2)
    for other_customers in shop.getCustomers():
        if other_customers.getId()!= customer.getId():
            forces = forces + F_0 * np.exp((d_0-norm(customer.getPos()-other_customers.getPos()))/beta_customer) * 1/norm(customer.getPos()-other_customers.getPos()) *(customer.getPos()-other_customers.getPos()) * vision_coef(customer, other_customers, lambd)

    for wall in shop.getWalls():
        if intersectionSegDroite(wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3], customer.getPos()[0], customer.getPos()[1], wall.getNormal()):
            intersect = intersectPointLine(customer.getPos()[0], customer.getPos()[1], wall.getNormal(), wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3])
            dist = norm(intersect - np.array([customer.getPos()[0], customer.getPos()[1]]))
            if np.vdot(wall.getNormal(), np.array([customer.getPos()[0], customer.getPos()[1]]) - intersect) > 0:
                forces = forces + F_wall0 * np.exp((d_0/2 - dist)/beta_wall) * wall.getNormal()
            else:
                forces = forces - F_wall0 * np.exp((d_0/2 - dist)/beta_wall) * wall.getNormal()

    for stand in shop.getStands():
         for stand_wall in stand.getStandWalls():
             if intersectionSegDroite(stand_wall.getPos()[0], stand_wall.getPos()[1], stand_wall.getPos()[2], stand_wall.getPos()[3], customer.getPos()[0], customer.getPos()[1], stand_wall.getNormal()):
                 intersect = intersectPointLine(customer.getPos()[0], customer.getPos()[1], stand_wall.getNormal(), stand_wall.getPos()[0],stand_wall.getPos()[1], stand_wall.getPos()[2], stand_wall.getPos()[3])
                 dist = norm(intersect - np.array([customer.getPos()[0], customer.getPos()[1]]))
                 if np.vdot(stand_wall.getNormal(), np.array([customer.getPos()[0], customer.getPos()[1]]) - intersect) > 0:
                     forces = forces + F_stand0 * np.exp((d_0 / 2 - dist) / beta_wall) * stand_wall.getNormal()
                 else:
                     forces = forces - F_stand0 * np.exp((d_0 / 2 - dist) / beta_wall) * stand_wall.getNormal()

    for exit in shop.exits:
        forces += exitForce(customer, exit, F_exit)
    return forces


def customers_exit(shop, canvas, balls_list, lines_list, x_max, y_max):
    """
    Deletes a customer if he approaches an exit
    :param shop: the shop (type : Shop)
    :param canvas: the tkinter canvas
    :param balls_list: the list of the green dots on tkinter, representing each customer
    :param lines_list: y=the list of green lines representing the speed of each customer
    :return: None
    """
    #We create polygons around each exit (for now, exits are lines)
    list_exits = []
    for exit in shop.getExits():
        normal = exit.getNormal()
        xA, yA, xB, yB = exit.getPos()
        A = [xA, yA] + 5*normal
        B = [xB, yB] + 5*normal
        C = [xB, yB] - 5*normal
        D = [xA, yA] - 5*normal
        polygon_exit = [A, B, C, D]
        list_exits.append(polygon_exit)

    for customer in shop.getCustomers():
        pos = customer.getPos()
        for exit in list_exits:
            if inside(pos[0], pos[1], exit):
                shop.removeCustomer(customer)
                canvas.coords(balls_list[customer.getId()], x_max + 100, y_max + 100, x_max + 110, y_max + 110)
                balls_list[customer.getId()] = None
                if lines_list:
                    canvas.coords(lines_list[customer.getId()], x_max + 100, y_max + 100, x_max + 110, y_max + 110)
                    lines_list[customer.getId()] = None
