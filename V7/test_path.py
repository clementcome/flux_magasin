import numpy as np
import random as rd
from Person import *
from Object import *
from Container import *
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
from Operator import *
from Path_Outils import *
from Instance import *
from Silent_Instance import *
from Person import *
from Object import *
from Container import *
from In_Terface import *
from time import time

size, margin, objects, people = np.array([100, 100]), 5, [], []

#objects = [Entry(np.array([3.0,3.0]), np.array([4,4])), Obstacle(np.array([30.0,10.0]), np.array([20, 20])), Obstacle(np.array([60.0,60.0]), np.array([10, 20])), Obstacle(np.array([0.0,0.0]), np.array([2, 100])), Obstacle(np.array([0.0,0.0]), np.array([100, 2])), Obstacle(np.array([98.0,0.0]), np.array([2, 100])), Obstacle(np.array([0.0, 98.0]), np.array([100, 2])), Exit(np.array([96.0, 96.0]), np.array([2, 2]))]


in_terface = In_Terface()
#in_terface.initialize_interface()
in_terface.initialize_silent_interface()

saved_state = in_terface.get_state()
size = saved_state.screen_size // 5
objects = saved_state.objects

'''
size = np.array([80,80])
margin, people = 5, []


objects = [Entry(np.array([5.0,5.0]), np.array([4,4])), Obstacle(np.array([20.0,10.0]), np.array([10, 5])), Obstacle(np.array([60.0,60.0]), np.array([10, 10])), Obstacle(np.array([0.0,0.0]), np.array([2, 80])), Obstacle(np.array([0.0,0.0]), np.array([80, 2])), Obstacle(np.array([78.0,0.0]), np.array([2, 80])), Obstacle(np.array([0.0, 78.0]), np.array([80, 2])), Exit(np.array([76.0, 76.0]), np.array([2, 2]))]
objects.append(Obstacle(np.array([50.0,25.0]), np.array([20, 5])))
objects.append(Exit(np.array([75.0,3.0]), np.array([2, 3])))
objects.append(Entry(np.array([5.0,70.0]), np.array([4,4])))
objects.append(Entry(np.array([35.0,70.0]), np.array([4,4])))
objects.append(Obstacle(np.array([50.0,50.0]), np.array([10, 20])))
objects.append(Obstacle(np.array([20.0,25.0]), np.array([3, 18])))
objects.append(Obstacle(np.array([50.0,25.0]), np.array([5, 24])))
'''
path = load_path("paths1.txt")
F = Folower(path)

setup = Setup(size, margin, objects, people)

for A in [1, 0.1, 0.01]:
	
	for lam in [1, 0.5, 0.2]:
		instance = Silent_Instance(setup, A, 0.5, lam)
		instance.agents.append(F)


		instance.people[0].pos = np.copy(F.pos)
		instance.people[0].des_pos = np.copy(path[-1])
		instance.people[0].direction = np.copy(F.direction)
		instance.people[0].vel = np.copy(F.vel)
		instance.people[0].rad = np.copy(F.rad)


		instance.init_show()
