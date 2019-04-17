import numpy as np
import random
import pygame
from Container import *

class Object:


	normal_color = [0,0,0]
	bright_color = [50,50,50]

	scale = 5
	drag = False

	#null
	def __init__(self, position, size):
		
		#(x, y) numpy array
		self.position = np.array((position[0], position[1])) // self.scale
		
		#(length, heigth) numpy array
		self.size = np.array((size[0], size[1])) // self.scale

		#initialize variables
		self.offset_y = self.offset_x = 0
		self.touched = 0
		self.seen = 0

	def draw(self, screen, margin):

		y, x = self.position * self.scale + margin
		dy, dx = self.size * self.scale

		if not self.drag:
			pygame.draw.rect(screen, self.normal_color, pygame.Rect(x, y, dx, dy))
		else:
			pygame.draw.rect(screen, self.bright_color, pygame.Rect(x, y, dx, dy))

	def in_collision(self, event_pos):

		#unpack variables
		y, x = self.position * self.scale
		dy, dx = self.size * self.scale

		collide = (x <= event_pos[0] <= x + dx)
		collide = collide and (y <= event_pos[1] <= y + dy)

		return collide

	#null
	def __init__(self):
		pass

	#(length, heigth)
	def get_size(self):

		return self.size

	#(pos_x, pos_y)
	def get_pos(self):

		return self.position

	#null
	def scale_size(self, scale):

		self.size = np.array((max(1, self.size[1] // scale), max(1, self.size[0] // scale)))

	#null
	def scale_position(self, scale):

		self.position = np.array((self.position[1] // scale, self.position[0] // scale))

	#null
	def start_drag(self, event_pos):
		self.drag = True
		event_x, event_y = event_pos
		y, x = self.position * self.scale
		self.offset_x = x - event_x
		self.offset_y = y - event_y

	#null
	def end_drag(self):
		self.drag = False


	#null
	def offset_pos(self, event_pos, left, right, upper, lower):
		if self.drag:
			event_x, event_y = event_pos
			dy, dx = self.size * self.scale


			if event_x + self.offset_x + dx > right:
				x = right - dx
				
			elif event_x + self.offset_x < left:
				x = left
			else:
				x = event_x + self.offset_x

			if event_y + self.offset_y + dy > upper:
				y = upper - dy
			elif event_y + self.offset_y < lower:
				y = lower
			else:
				y = event_y + self.offset_y

			self.position = np.array((y, x)) // self.scale

	def get_center_of_mass(self):
		'''
		-> self (self)
		<- pos_mass (numpy couple)
		Return geometrical center of object
		'''

		return self.position + self.size / 2

	def touch(self):
		'''
		-> self (self)
		<- None
		updates touch counter of obj
		'''

		self.touched += 1

	def see(self):
		'''
		-> self (self)
		<- None
		updates sight counter of obj
		'''

		self.touched += 1

	#maybe useless
	def get_value(self):

		return self.value

	def set_index(self, i):

		self.index = i


	def get_index(self):

		return self.index

	
class Obstacle(Object):
	def __init__(self, position, size):
		#(x, y) numpy array
		self.position = position
		
		#(length, heigth) numpy array
		self.size = size

		#initialize variables
		self.offset_y = self.offset_x = 1
		self.touched = 0
		self.seen = 0
		self.value = 1

class Entry(Object):

	def __init__(self, position, size):
		
		'''
		-> self (self), position (numpy couple), size (numpy couple)
		<- None
		Creates a person in a position
		'''

		#(x, y) numpy array
		self.position = position
		
		#(length, heigth) numpy array
		self.size = size

		#initialize variables
		self.offset_y = self.offset_x = 0
		self.touched = 0
		self.seen = 0
		self.value = 0.3

		#Mode 0 is shopping mode
		self.mode = 0
		self.produced = 0

	def new_person(self):

		'''
		-> self (self)
		<- new (Boolean), info (Container)
		Creates a person in a position
		'''
		
		r = random.random()
		if r > 0.98:
			
			position = self.get_free_position().astype('float64')
			direction = self.get_direction().copy()

			info = Info(position, direction)
			
			'''
			if self.produced > 3:
				return False, Info(np.array([0,0]), np.array([0,0]))
			self.produced += 1
			'''
			return  True, info

		else:

			return False, Info(np.array([0,0]), np.array([0,0]))

	def get_free_position(self):


		return self.position + self.size * np.random.rand(2)

	def get_direction(self):

		return np.array([1,0])

class Exit(Object):

	normal_color = [255,0,0]
	bright_color = [200,0,0]

	def __init__(self, position, size):
		
		'''
		-> self (self), position (numpy couple), size (numpy couple)
		<- None
		Creates a person in a position
		'''

		#(x, y) numpy array
		self.position = position
		
		#(length, heigth) numpy array
		self.size = size

		#initialize variables
		self.offset_y = self.offset_x = 0
		self.touched = 0
		self.seen = 0
		self.value = 0
		
		#Mode 0 is shopping mode
		self.mode = 0