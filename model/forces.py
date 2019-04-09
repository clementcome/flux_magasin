import numpy as np
from flux_magasin.model.environnement import *

F_0 = 1
F_wall = 1
d_0 = 1

def lambd(x):
    return np.exp(1/x)-1

def nom(vect):
    return np.sqrt(vect[0]**2+vect[1]**2)

def exteriorForces(client,shop):
    forces = np.zeros(2)
    wallForces = np.zeros(2)
    wallCoef = 1

    for otherClient in shop.getClients():
        if otherClient.getId()!= client.getId():
            forces += F_0 * (np.array(client.getPos())-np.array(otherClient.getPos))/abs(norm(np.array(client.getPos())-np.array(otherClient.getPos))**2-d_0**2)

print(np.zeros(2))