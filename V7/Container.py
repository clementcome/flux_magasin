import numpy as np
import random as rd

class Container:

	def __init__(self, size, margin, objects, people = []):

		pass

class Setup(Container):

	def __init__(self, size, margin, objects, people = []):

		self.size = size
		self.margin = margin
		self.objects = objects
		self.people = people

class Info(Container):

	def __init__(self, pos, direction):

		self.pos = pos
		self.direction = direction