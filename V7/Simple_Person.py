import numpy as np
from Object import *
from Container import *
import random

class Person:

	
	def __init__(self, info):
		'''
		-> self (self), position (numpy couple), size (numpy couple)
		<- None
		Creates a person in a position
		'''

		#unpack info
		self.pos = info.pos
		self.direction = info.direction

		#initialize variables
		self.offset_y = self.offset_x = 0
		self.target = None
		self.vel = np.array([0,0])
		self.min_sin = 0.6
		self.max_sin = -0.6
		self.proximity_constant = 10
		self.avoid_constant = 1
		self.adquisition_value = 0.2
		self.spont_replacement_value = 0.9999
		self.real_replacement_value = 0.99

		self.max_speed = 0.5
		#int_vel, geo_vel, soc_vel
		self.w = np.array([[0.33, 0.33, 0.33]])
		self.nor_speed = 0.8
		self.personal_radius = 2
		self.buy_radius = 1.5 * self.personal_radius
		self.int_vel = np.array([0.0,0.0])
		self.soc_vel = np.array([0.0,0.0])
		self.vel = np.array([0.0,0.0])
		self.browse_speed = 0.2
		self.spont_abandon = 0.999
		self.buy_chance = 0.99
		self.seen = 0
		self.theo_vel = np.zeros(2)
		self.dir_pen = 1

		#Mode 0 is shopping mode
		self.set_mode(0)

	def set_target(self, target):
		'''
		-> self (self), target (Object)
		<- None
		Sets a target for the person
		'''

		self.target = target

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

	def get_target(self):

		if self.target is None:
			return None

		return self.target.get_index()

	def calculate_interaction_people(self, other):

		'''
		-> self (self), other (Person)
		<- None
		Calculates the interaction between the person and other
		'''


		#unpack variables
		pos = self.pos
		ot_pos = other.get_pos()	
		dist = np.linalg.norm(pos - ot_pos)
		#if very close it feels repulsion
		if dist < self.personal_radius:

			c = self.proximity_constant

			self.int_vel += c * (pos - ot_pos) / (np.linalg.norm(pos - ot_pos) ** 3.0)

		'''
		#if in field of vision also feels repulsion
		direction = self.direction
		ot_adj_pos = ot_pos - pos
		dist_adj = np.linalg.norm(ot_adj_pos) * np.linalg.norm(direction)

		if abs(np.cross(ot_adj_pos, direction) / dist_adj) > self.max_sin:

			k = self.avoid_constant
			self.soc_vel += k * (pos - ot_pos) / np.linalg.norm(pos - ot_pos) ** 4
		'''
	def calculate_interaction_object(self, obj):

		'''
		-> self (self), object (Object)
		<- None
		Calculates the interaction between the person and other
		'''
		
		if not isinstance(obj, Obstacle):

			return

		#Unpack variables
		pos = self.pos
		ob_pos = obj.get_pos()
		ob_size = obj.get_size()


		#Posibility of locking eyes if in field of vision
		#CHANGE
		#check if within fov
		'''
		if self.can_see(ob_pos, ob_size):
			#Track how many times objects has been seen
			obj.see()
		'''

		#if close by, try to avoid it
		dist, proj = self.distance_to_rec(ob_pos, ob_size)
		self.proj = proj
		if dist < self.personal_radius:

			c = self.proximity_constant
			self.int_vel += c * (pos - proj) / np.linalg.norm(dist) ** 3

			#track how many times object is touched
			obj.touch()




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
	

	def can_see(self, ob_pos, ob_size):
		'''
		-> self (self), obj_pos (numpy couple), obj_size (numpy couple)
		<- can_see (bool)
		Determines if person can see object
		'''

		pos = self.pos
		direction = self.direction

		vec = [ob_pos, ob_pos +  np.array([ob_size[0], 0]), ob_pos +  np.array([0, ob_size[1]]), ob_pos + ob_size]

		for ob_pos in vec:
			cros = np.cross(ob_pos - pos, direction)
			adj_dist = np.linalg.norm(ob_pos - pos) * np.linalg.norm(direction)

			if abs(cros / adj_dist) > self.max_sin:
				return True

		
		return False


	def update_vel(self, geo_vel):
		'''
		-> self (self), geo_vel (numpy couple)
		<- None
		Updates the velocity
		'''

		#unpack variables
		max_speed = self.max_speed
		w = self.w
		mode = self.mode

		#normalize
		if np.linalg.norm(self.int_vel) > 0:

			self.int_vel = self.max_speed * self.int_vel / np.linalg.norm(self.int_vel)
		
		#prepare velocities for ponderation
		#int_vel, geo_vel, soc_vel
		vel_vec = np.array([self.int_vel, geo_vel, self.soc_vel])
		
		#in different modes they different ponderations
		self.anc_vel = self.vel.copy()
		self.vel = w[mode].dot(vel_vec)
		self.direction = self.vel / np.linalg.norm(self.vel)
		self.vel = self.direction * self.max_speed

	def update_pos(self):
		
		'''
		-> self (self)
		<- None
		Updates the position
		'''
		
		self.pos += self.vel

		self.anc_vel = self.int_vel
		self.anc_soc_vel = self.soc_vel
		self.int_vel = np.array([0.0,0.0])
		self.soc_vel = np.array([0.0,0.0])

	def evaluate_mode(self):
		
		'''
		-> self (self)
		<- None
		Evaluates if person should change state
		'''

		return

	def exit(self, exit):
		'''
		-> self (self), exit (Exit)
		<- exits (Bool)
		Evaluates if person goes out
		'''
		ob_pos, ob_size = exit.get_pos(), exit.get_size()
		dist, proj = self.distance_to_rec(ob_pos, ob_size)
		print(proj)

		if dist < self.personal_radius:
			return True
		else:
			return False










