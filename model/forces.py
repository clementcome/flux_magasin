import numpy as np
from model.environnement import Wall,StandWall,Shop,Stand,Client,Entry,Exit
from model.intersections import intersectPointLine, intersectionSegDroite, inside
from model.utils import norm

# def lambd(x):
#     return np.exp(-x**0.3)


def exitForce(client, exit, F_exit):
    xForce = (exit.x1+exit.x2)/2 - client.x
    yForce = (exit.y1+exit.y2)/2 - client.y
    vecClientMur = np.array([xForce, yForce])
    vecForce = F_exit*vecClientMur/norm(vecClientMur)
    return vecForce


def exteriorForces(customer, shop, lambd, d_0, F_wall0, F_stand0, F_0, F_exit):
    forces = np.zeros(2)
    wallForces = np.zeros(2)
    wallCoef = 1
    exitForces = np.zeros(2)

    for otherCustomer in shop.getCustomers():
        if otherCustomer.getId() != customer.getId():
            forces = forces + F_0 * (np.array(customer.getPos()) - np.array(otherCustomer.getPos())) / abs(norm(np.array(customer.getPos()) - np.array(otherCustomer.getPos())) ** 2 - d_0 ** 2)

    for wall in shop.getWalls():
        if intersectionSegDroite(wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3], customer.getPos()[0], customer.getPos()[1], wall.getNormal()):
            intersect = intersectPointLine(customer.getPos()[0], customer.getPos()[1], wall.getNormal(), wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3])
            dist = norm(intersect - np.array([customer.getPos()[0], customer.getPos()[1]]))
            wallCoef = wallCoef * (1-lambd(dist))
            if np.vdot(wall.getNormal(), np.array([customer.getPos()[0], customer.getPos()[1]]) - intersect) > 0:
                wallForces = wallForces + lambd(dist) * F_wall0 * wall.getNormal()
            else:
                wallForces = wallForces - lambd(dist) * F_wall0 * wall.getNormal()

    for stand in shop.getStands():
        for standWall in stand.getStandWalls():
            if intersectionSegDroite(standWall.getPos()[0], standWall.getPos()[1], standWall.getPos()[2], standWall.getPos()[3],
                                     customer.getPos()[0], customer.getPos()[1], standWall.getNormal()):
                intersect = intersectPointLine(customer.getPos()[0], customer.getPos()[1], standWall.getNormal(), standWall.getPos()[0],
                                               standWall.getPos()[1], standWall.getPos()[2], standWall.getPos()[3])
                dist = norm(intersect - np.array([customer.getPos()[0], customer.getPos()[1]]))
                wallCoef = wallCoef * (1 - lambd(dist))
                if np.vdot(standWall.getNormal(), np.array([customer.getPos()[0], customer.getPos()[1]]) - intersect) > 0:
                    wallForces = wallForces + lambd(dist) * F_stand0 * standWall.getNormal()
                else:
                    wallForces = wallForces - lambd(dist) * F_stand0 * standWall.getNormal()

    for exit in shop.exits:
        exitForces += exitForce(customer, exit, F_exit)
    return wallCoef * (forces + exitForces) + wallForces


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
                canvas.coords(lines_list[customer.getId()], x_max + 100, y_max + 100, x_max + 110, y_max + 110)
