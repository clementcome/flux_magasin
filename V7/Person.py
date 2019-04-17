import numpy as np
from Object import *
from Container import *
import random

class Agent:

	def __init__(self, info):
		'''
		-> self (self), position (numpy couple), size (numpy couple)
		<- None
		Creates an Agent in a position
		'''

		#unpack info
		self.pos = info.pos
		self.direction = info.direction

		#initialize external Agent variables
		self.rad = 0.8 + random.random()
	
		
	def get_rad(self):
		'''
		-> self (self)
		<- rad (float)
		Gets the radius of the person
		'''
		return self.rad


	def set_mode(self, mode):
		'''
		-> self (self), mode (integer)
		<- None
		Sets a mode for the person (0 is shopping, 1 is leaving)
		'''

		self.mode = mode

	def get_vel(self):
		'''
		-> self (self)
		<- vel (numpy couple)
		Returns the velocity of the person
		'''

		return self.vel

	def get_pos(self):
		'''
		-> self (self)
		<- pos (numpy couple)
		Returns the position of the person
		'''

		return self.pos

	def get_dir(self):
		'''
		-> self (self)
		<- direction (numpy couple)
		Returns the direction of the person
		'''

		return sel.direction

	def distance_to_rec(self, ob_pos, ob_size):

		'''
		-> self (self), obj_pos (numpy couple), obj_size (numpy couple)
		<- dist (float)
		Calculates the distance to a rectangle
		'''

		#unpack variables
		pos = self.pos

		#Compare all edges
		proj = ob_pos.copy()
		re_dist = np.linalg.norm(pos - ob_pos)

		aux = np.array([ob_size[0], 0.0])
		if re_dist > np.linalg.norm(pos - ob_pos - aux):
			re_dist = np.linalg.norm(pos - ob_pos - aux)
			proj = ob_pos + aux

		aux = np.array([0.0, ob_size[1]])
		if re_dist > np.linalg.norm(pos - ob_pos - aux):
			re_dist = np.linalg.norm(pos - ob_pos - aux)
			proj = ob_pos + aux

		aux = np.array([ob_size[0], ob_size[1]])
		if re_dist > np.linalg.norm(pos - ob_pos - aux):
			re_dist = np.linalg.norm(pos - ob_pos - aux)
			proj = ob_pos + aux

		#see if proyects to the side
		for i in range(2):
			if ob_pos[i] < pos[i] < ob_pos[i] + ob_size[i]:

				if re_dist > abs(pos[1 - i] - ob_pos[1 - i]):

					re_dist = abs(pos[1 - i] - ob_pos[1 - i])
					proj = pos.copy()
					proj[1 - i] = ob_pos[1 - i]

				if re_dist > abs(ob_size[1 - i] + ob_pos[1 - i] - pos[1 - i]):

					re_dist = abs(pos[1 - i] - ob_pos[1 - i] - ob_size[1 - i])
					proj = pos.copy()
					proj[1 - i] = ob_pos[1 - i] + ob_size[1 - i]

		return re_dist, proj

	def exit(self, exit):
		'''
		-> self (self), exit (Exit)
		<- exits (Bool)
		Evaluates if person goes out
		'''
		ob_pos, ob_size = exit.get_pos(), exit.get_size()
		dist, proj = self.distance_to_rec(ob_pos, ob_size)

		if dist < self.rad:
			return True
		else:
			return False

class Folower(Agent):

	def __init__(self, path):

		'''
		-> self (self), position (numpy couple), size (numpy couple)
		<- None
		Creates a person in a position
		'''

		#unpack info
		self.path = path
		self.pos = path[0].astype('float64')

		if len(path) > 0:

			if np.linalg.norm(self.path[1] - self.path[0]) > 0:
				self.direction = (self.path[1] - self.path[0]) / np.linalg.norm(self.path[1] - self.path[0])
				self.vel = self.path[1] - self.path[0]
			else:
				self.direction = np.zeros(2)
				self.vel = np.zeros(2)
		else:
			self.direction = np.zeros(2)
			self.vel = np.zeros(2)
		

		#initialize external Agent variables
		self.rad = 1.2

		#initialize internal variables
		self.path_pos = 0


	def update_pos(self):
		
		'''
		-> self (self)
		<- None
		Updates the position
		'''

		#increase position in path and unpack
		self.path_pos += 1
		path_pos = self.path_pos
		path = self.path

		#update physical position and vel
		self.pos += self.vel
		if path_pos + 1 < len(path):
			self.vel = self.path[path_pos + 1] - self.path[path_pos]
		else:
			self.vel = np.zeros(2)

class Person(Agent):

	def __init__(self, info):
		'''
		-> self (self), position (numpy couple), size (numpy couple)
		<- None
		Creates a person in a position
		'''

		#unpack info
		self.pos = info.pos
		self.direction = info.direction

		#initialize external Agent variables
		self.rad = 0.8 + random.random() * 0.3

		#initialize external Person variables
		self.lam = 1
		self.A = 0.05
		self.B = 0.0001
		self.dt = 1
		self.tau = 2
		self.des_speed = 1

		#initialize internal variables
		self.obj_force = np.zeros(2)
		self.per_force = np.zeros(2)
		self.vel = np.zeros(2)
		self.old_vel = np.zeros(2)
		self.des_vel = np.random.rand(2)#np.array([1,0]) * (random.randint(0,1) - 1)
		self.des_pos = np.random.rand(2) * 100
	

	def calculate_interaction_people(self, other):

		'''
		-> self (self), other (Person)
		<- None
		Calculates the interaction between the person and other
		'''

		#unpack variables
		lam = self.lam
		A = self.A
		B = self.B

		#unpack own variables
		pos = self.pos
		rad = self.rad
		direction = self.direction

		#unpack other's variables
		ot_pos = other.get_pos()
		ot_rad = other.get_rad()

		#define other variables
		dist = np.linalg.norm(pos - ot_pos)
		dist_direction = (pos - ot_pos)/dist

		#the repulsion has 2 components
		#angular component
		omega = lam + (1 - lam) * (1 + np.dot(direction, dist_direction))/2

		#radial component
		g = A * np.exp((rad + ot_rad - dist)/B) * dist_direction
		
		#total force
		self.per_force += omega * g

	def calculate_interaction_object(self, obj):

		'''
		-> self (self), object (Object)
		<- None
		Calculates the interaction between the person and other
		'''
		
		#unpack variables
		lam = self.lam
		A = self.A
		B = self.B

		#unpack own variables
		pos = self.pos
		rad = self.rad
		direction = self.direction

		#unpack other's variables

		#define other variables
		ob_pos = obj.get_pos()
		ob_size = obj.get_size()
		dist, ot_pos = self.distance_to_rec(ob_pos, ob_size)
		dist_direction = (pos - ot_pos)/dist

		#the repulsion has 2 components
		#angular component
		omega = lam + (1 - lam) * (1 + np.dot(direction, dist_direction))/2

		#radial component
		g = A * np.exp((rad - dist)/B) * dist_direction
		
		#total force
		self.obj_force += omega * g



	def update_vel(self, ext_dir):
		'''
		-> self (self), des_vel (numpy couple)
		<- None
		Updates the velocity
		'''

		#unpack variables
		old_vel = self.old_vel
		obj_force = self.obj_force
		per_force = self.per_force
		des_force = self.calculate_des_force(ext_dir)
		dt = self.dt

		#use update formula
		self.vel += dt * (des_force + per_force + obj_force)
		self.direction = self.vel / np.linalg.norm(self.direction)



	def calculate_des_force(self, des):
		'''
		-> self (self), des_vel (numpy couple)
		<- des_force (numpy couple)
		Calculates the force due to desire
		'''

		#unpack variables
		tau = self.tau
		vo = self.des_speed
		old_vel = self.old_vel
		des_dir = self.calculate_des_vel()

		#Return the formula of the desired force
		return (vo * des_dir - old_vel)/tau

	def calculate_des_vel(self):
		'''
		-> self (self), des_vel (numpy couple)
		<- des_force (numpy couple)
		Calculates the force due to desire
		'''

		#unpack variables
		pos = self.pos
		des_pos = self.des_pos


		if np.linalg.norm(des_pos - pos) > 0:
			return (des_pos - pos) / np.linalg.norm(des_pos - pos)
		else:
			return np.zeros(2)

	def update_pos(self):
		
		'''
		-> self (self)
		<- None
		Updates the position
		'''
		
		self.pos += self.vel * self.dt

		self.old_vel = np.copy(self.vel)
		self.int_force = np.array([0.0,0.0])
		self.soc_force = np.array([0.0,0.0])

