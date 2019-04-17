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

class Silent_Instance:

	def __init__(self, setup, A, B, lam):
		
		'''
		-> self (self), setup (setup)
		<- None
		Create an instance, meaning a given configuratiion of a magazin
		'''

		self.setup = setup

		#unpack variables
		self.size = setup.size
		self.margin = setup.margin
		self.objects = setup.objects
		self.people = setup.people
		self.agents = []
		self.entry = []
		self.obstacle = []
		self.exit = []
		self.copying = (0,0)
		self.A = A
		self.B = B
		self.lam = lam

		#initialize variables
		self.track = np.zeros(self.size)
		self.way_to = np.zeros([len(self.objects), self.size[0], self.size[1], 2]) + 0.3
		self.way_to_exit = np.zeros([self.size[0], self.size[1], 2]) + 0.3
		self.state = np.zeros(self.size) + 0.3
		self.initialize_state()

	def initialize_state(self):

		'''
		-> self (self)
		<- None
		Place the initial conditions of the magazine
		'''

		#unpack variables
		size = self.size
		margin = self.margin

		#place objects
		self.place_objects()
		
		#place people
		n_pe = 14
		people = self.people
		for i in range(n_pe):


			position = (self.size - 19) * np.random.rand(2) + 10
			r = random.random() * 2 * np.pi
			direction = np.array([np.sin(r), np.cos(r)])

			info = Info(position, direction)
			people.append(Person(info))
			people[-1].A = self.A
			people[-1].B = self.B
			people[-1].lam = self.lam
			
		self.calculate_way_to_exit()

	def place_objects(self):

		'''
		-> self (self)
		<- None
		Initializes the positions of objects and 
		'''

		n_ob = len(self.objects)
		objects = self.objects
		for i in range(n_ob):
			
			#Assign index
			objects[i].set_index(i)

			#Place in map
			x, y = objects[i].get_pos()
			x, y = int(x), int(y)
			dx, dy = objects[i].get_size()

			val = objects[i].get_value()

			if val == 0.3:

				self.entry.append(i)

			if val == 1:

				self.obstacle.append(i)

			if val == 0:
				
				self.exit.append(i)
				self.state[x:(x + dx), y:(y + dy)] = 0.3
			
			else:
			
				self.state[x:(x + dx), y:(y + dy)] = objects[i].get_value()


		
		for i in range(n_ob):

			self.calculate_way_to(i)
		
		
	def update_state(self):

		'''
		-> self (self)
		<-
		'''

		#unpack variables
		size = self.size
		margin = self.margin
		people = self.people
		agents = self.agents
		n_ag = len(agents)
		n_ob = len(self.objects)
		objects = self.objects

		#activate objects
		for i in self.entry:
			new, info = objects[i].new_person()
			if new:
				people.append(Person(info))

		#calculate velocities
		n_pe = len(self.people)
		people = self.people

		#initialize container
		kill = []

		#calculate interaction forces
		for i in range(n_pe):

			for j in range(n_pe):
				if i != j:
					people[i].calculate_interaction_people(people[j])
			
			for j in range(n_ag):
				if (i,j) != self.copying:
					people[i].calculate_interaction_people(agents[j])

			for j in self.obstacle:
				people[i].calculate_interaction_object(objects[j])
			
			for j in self.exit:
				if people[i].exit(objects[j]):
					kill.append(people[i])

		for person in kill:
			people.remove(person)
			n_pe -= 1

		#calculate desired velocities
		for i in range(n_pe):

			pos = people[i].get_pos()
			people[i].update_vel(np.array([0,0]))

		#update positions
		for i in range(n_pe):

			people[i].update_pos()

		for i in range(n_ag):

			agents[i].update_pos()

	def calculate_way_to(self, i):

		'''
		-> self (self), i (int)
		<- None
		Use the operator module to solve the eikonal equation
		and calculate the velocity field to reach object i
		'''

		obj = self.objects[i]

		x, y = obj.get_pos()
		x, y = int(x), int(y)
		dx, dy = obj.get_size()
		
		aux = self.state[x][y]
		self.state[x:(x + dx), y:(y + dy)] = 0

		self.operator = Fast_march_calculator(self.state, 1)
		self.way_to[i] = self.operator.calculate_velocity_field()

		self.state[x:(x + dx), y:(y + dy)] = aux

	def calculate_way_to_exit(self):

		'''
		-> self (self), i (int)
		<- None
		Use the operator module to solve the eikonal equation
		and calculate the velocity field to reach object i
		'''
		n_ob = len(self.objects)
		state = self.state.copy()

		for i in range(n_ob):

			obj = self.objects[i]

			x, y = obj.get_pos()
			x, y = int(x), int(y)
			dx, dy = obj.get_size()
			
			state[x:(x + dx), y:(y + dy)] = self.objects[i].get_value()
		
		self.operator = Fast_march_calculator(state, 1)
		self.way_to_exit = self.operator.calculate_velocity_field()

	
	def update_track(self, pos):

		self.track[int(pos[0])][int(pos[1])] += 1


	def get_geometric_vel(self, pos, target):
		'''
		'''

		if target is None:

			return self.way_to_exit[int(pos[0])][int(pos[1])]

		else:

			return self.way_to[target][int(pos[0])][int(pos[1])]

	def init_show(self):
		
		'''
		'''

		fig = plt.figure()
		fig.set_dpi(100)
		fig.set_size_inches(7, 6.5)

		ax = plt.axes(xlim=(-10, self.size[0] + 10), ylim=(-10, self.size[1] + 10))
		self.ax = ax

		self.circ = []
		self.rect = []


		self.title = self.ax.text(self.margin, self.size[1], str(len(self.people)) + " people")
		
		objects = self.objects
		n_ob = len(objects)
		for i in range(n_ob):
			pos = objects[i].get_pos()
			size = objects[i].get_size()
			if i == len(self.rect):

				if isinstance(objects[i], Entry):
					self.rect.append(patches.Rectangle(pos, size[0], size[1], color = 'y', alpha = 0.5))
				elif isinstance(objects[i], Exit):
					self.rect.append(patches.Rectangle(pos, size[0], size[1], color = 'r'))
				else:
					self.rect.append(patches.Rectangle(pos, size[0], size[1]))
				

				self.ax.add_patch(self.rect[i])

		self.error = 0
		N = 300
		for i in range(N):
			self.update_show()
		print(self.error)


	def show_velocities(self, vel_field):

		'''
		'''
		for i in range(len(vel_field)):
			for j in range(len(vel_field)):
				n = np.linalg.norm(vel_field[i][j])
				if n != 0:
					ar = patches.Arrow(i, j, vel_field[i][j][0] / n, vel_field[i][j][1] / n, color = 'g')
					self.ax.add_patch(ar)

	def update_show(self):

		'''
		'''
		'''
		if iter == 300:

			save_path(self.path, "paths1.txt")
			print(self.path)
			print(len(self.path))
		'''
		self.update_state()
		cop = self.copying
		self.error += np.linalg.norm(self.people[cop[0]].pos - self.agents[cop[1]].pos)**2

