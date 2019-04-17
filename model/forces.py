import numpy as np
from environnement import Wall,StandWall,Shop,Stand,Client,Entry,Exit
from intersections import intersectPointLine
from utils import norm

F_0 = 1
F_wall0 = 10
d_0 = 1
F_exit = 1


def lambd(x):
    return np.exp(-x**0.4)

def exitForce(client,exit):
    xForce = (exit.x1+exit.x2)/2 -client.x
    yForce = (exit.y1+exit.y2)/2 -client.y
    vecClientMur = np.array([xForce,yForce])
    vecForce = F_exit*vecClientMur/norm(vecClientMur)
    return vecForce

def exteriorForces(client,shop):
    forces = np.zeros(2)
    wallForces = np.zeros(2)
    wallCoef = 1
    exitForces = np.zeros(2)

    for otherClient in shop.getClients():
        if otherClient.getId()!= client.getId():
            forces = forces + F_0 * (np.array(client.getPos())-np.array(otherClient.getPos()))/abs(norm(np.array(client.getPos())-np.array(otherClient.getPos()))**2-d_0**2)

    for wall in shop.getWalls():
        intersect = intersectPointLine(client.getPos()[0],client.getPos()[1], wall.getNormal(), wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3])
        dist = norm(intersect-np.array([client.getPos()[0],client.getPos()[1]]))
        wallCoef = wallCoef*(1-lambd(dist))
        if np.vdot(wall.getNormal(),np.array([client.getPos()[0],client.getPos()[1]])-intersect)>0:
            wallForces = wallForces + lambd(dist)*F_wall0*wall.getNormal()
        else:
            wallForces = wallForces - lambd(dist)*F_wall0*wall.getNormal()

    for stand in shop.getStands():
        for standWall in stand.getStandWalls():
            intersect = intersectPointLine(client.getPos()[0], client.getPos()[1], standWall.getNormal(), standWall.getPos()[0],
                                           standWall.getPos()[1], standWall.getPos()[2], standWall.getPos()[3])
            dist = norm(intersect - np.array([client.getPos()[0], client.getPos()[1]]))
            wallCoef = wallCoef * (1 - lambd(dist))
            if np.vdot(standWall.getNormal(), np.array([client.getPos()[0], client.getPos()[1]]) - intersect) > 0:
                wallForces = wallForces + lambd(dist) * F_wall0 * standWall.getNormal()/4
            else:
                wallForces = wallForces - lambd(dist) * F_wall0 * standWall.getNormal()/4

    for exit in shop.exits:
        exitForces += exitForce(client,exit)
    return wallCoef*forces + wallForces + exitForces
