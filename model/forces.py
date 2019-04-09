import numpy as np
from flux_magasin.model.environnement import *
from flux_magasin.model.intersections import intersectPointLine

F_0 = 1
F_wall = 1
d_0 = 1

def lambd(x):
    return np.exp(-x**2)

def norm(vect):
    return np.sqrt(vect[0]**2+vect[1]**2)

def exteriorForces(client,shop):
    forces = np.zeros(2)
    wallForces = np.zeros(2)
    wallCoef = 1

    for otherClient in shop.getClients():
        if otherClient.getId()!= client.getId():
            forces = forces + F_0 * (np.array(client.getPos())-np.array(otherClient.getPos()))/abs(norm(np.array(client.getPos())-np.array(otherClient.getPos()))**2-d_0**2)

    for wall in shop.getWalls():
        intersect = intersectPointLine(client.getPos()[0],client.getPos()[1], wall.getNormal(), wall.getPos()[0], wall.getPos()[1], wall.getPos()[2], wall.getPos()[3])
        dist = norm(intersect-np.array([client.getPos()[0],client.getPos()[1]]))
        wallCoef = wallCoef*(1-lambd(dist))
        if np.vdot(wall.getNormal(),np.array([client.getPos()[0],client.getPos()[1]])-intersect)>0:
            wallForces = wallForces + lambd(dist)*F_wall*wall.getNormal()
        else:
            wallForces = wallForces - lambd(dist)*F_wall*wall.getNormal()

    for stand in shop.getStands():
        for standWall in stand.getStandWalls():
            intersect = intersectPointLine(client.getPos()[0], client.getPos()[1], standWall.getNormal(), standWall.getPos()[0],
                                           standWall.getPos()[1], standWall.getPos()[2], standWall.getPos()[3])
            dist = norm(intersect - np.array([client.getPos()[0], client.getPos()[1]]))
            wallCoef = wallCoef * (1 - lambd(dist))
            if np.vdot(standWall.getNormal(), np.array([client.getPos()[0], client.getPos()[1]]) - intersect) > 0:
                wallForces = wallForces + lambd(dist) * F_wall * standWall.getNormal()
            else:
                wallForces = wallForces - lambd(dist) * F_wall * standWall.getNormal()
    return wallCoef*forces + wallForces
