import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from scipy import signal
import heapq
import math

#Master class for all operators
class Operator:
	'''
	null
	'''
	def __init__(self):
		pass

class Fast_march_calculator(Operator):

	'''
	It runs the fast march algorythm to solve eikonal ecuations
	'''

	#null
	def __init__(self, U, h):
		'''
		-> U (numpy matrix), h (real)
		U is the matrix with the initial configuration and h the step
		The positions with initial value 1 start as 100000, the initial value 0 is 0
		'''

		#store variables
		self.U = U.copy()
		self.h = h
		self.der = Derivator()
		self.grad_U = np.zeros([U.shape[0], U.shape[1], 2])


	#real
	def calculate_eikonal_formula(self, grad_i, grad_j):

		'''
		-> grad_i (real), grad_j(real)
		<- ans (real)
		Runs the update formula for a specific step in the fast march algorythm
		'''

		#unpack variables
		h = self.h
		length, height = self.U.shape

		if abs(grad_i - grad_j) > h:

			ans = min(grad_i, grad_j) + h

		else:

			grad_sum = grad_i + grad_j
			grad_norm = grad_i**2 + grad_j**2

			root = 0.5 * math.sqrt(grad_sum**2 - 2*(grad_norm - h**2))

			ans = grad_sum/2.0 + root

		return ans

	#real
	def calculate_aproximate_gradient(self, i, j):
		'''
		-> i (int), j (int)
		<- ans (real)
		Calculates the gradient given the coordinates in the matrix
		'''


		#Unpack variables
		U = self.U
		length, height = U.shape

		#Calculate aproximate gradient
		grad_i = math.inf

		#Handling border cases
		if i + 1 < length:
			grad_i = min(U[i + 1][j], grad_i)
		if i - 1 >= 0:
			grad_i = min(U[i - 1][j], grad_i)
			
		grad_j = math.inf
		if j + 1 < height:
			grad_j = min(U[i][j + 1], grad_j)
		if j - 1 >= 0:
			grad_j = min(U[i][j - 1], grad_j)

		#Call the eikonal update formula
		return self.calculate_eikonal_formula(grad_i, grad_j)

	#null
	def calculate_U(self):
		'''
		-> None
		<- None
		It calculates the solution to the Eikonal equation as a potential U
		'''


		#unpack variables
		U = self.U
		length, height = U.shape

		#define variables
		priority_queue = []
		state = np.zeros([length, height])


		#initialize queue with neighboars of frontier
		for i in range(length):
			for j in range(height):
				ko = 1e9
				#undesirable places
				if U[i][j] == 1:

					U[i][j] = ko
					state[i][j] = -1					

				#desirable places
				elif U[i][j] == 0:
					state[i][j] = 2

				#other places
				else:

					U[i][j] = ko

		for i in range(length):
			for j in range(height):
				
				if state[i][j] == 0:
					new_U = self.calculate_aproximate_gradient(i, j)

					if new_U < U[i][j]:
						U[i][j] = new_U
						heapq.heappush(priority_queue, (new_U,i,j))
						state[i][j] = 1


		
		#find smallest value of U and update
		while len(priority_queue) > 0:

			dist, i, j = heapq.heappop(priority_queue)
			if state[i][j] == 2 or state[i][j] == -1 or state[i][j] == 0:
				continue
			state[i][j] = 2

			#update neighbors
			for di,dj in [(0,1), (1,0), (-1,0), (0,-1)]:

				if 0 <= di + i < length and 0 <= dj + j < height:
					
					if state[i+di][j+dj] == -1:
						
						continue

					elif state[i+di][j+dj] < 2:
						
						new_U = self.calculate_aproximate_gradient(i+di, j+dj)
						state[i+di][j+dj] = 1
						
						#if better solution is found, add to queue
						if new_U < U[i+di][j+dj]:
							U[i+di][j+dj] = new_U
							heapq.heappush(priority_queue, (new_U,i+di,j+dj))
	

	#velocity matrix
	def calculate_velocity_field(self):

		self.calculate_U()
		grad_U = self.der.calculate_derivative(self.U)
		norm = np.sqrt(np.square(grad_U[:,:,0]) + np.square(grad_U[:,:,1]))
		norm[norm == 0] = 1
		grad_U[:,:,0] /= norm
		grad_U[:,:,1] /= norm
		self.grad_U = grad_U
		
		return grad_U


	#2d matrix
	def get_U(self):
		return self.U

	def get_grad_U(self):
		return self.grad_U


class Velociy_calculator(Operator):

	#null
	def __init__(self):
		pass
class Reward_calculator(Operator):

	#null
	def __init__(self):
		pass

class Derivator(Operator):

	#null
	def __init__(self):
		pass

	#2d matrix
	def calculate_derivative(self, M):

		#conv_x = 0.5 * np.array([[0,-1,0],[0,0,0],[0,1,0]])
		conv_x = 1.0/8.0 * np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
		conv_y = np.transpose(conv_x)

		grad = np.zeros([M.shape[0], M.shape[1], 2])

		grad[:,:,0] = signal.convolve2d(M, conv_x, boundary='symm', mode='same')
		grad[:,:,1] = signal.convolve2d(M, conv_y, boundary='symm', mode='same')
		
		return grad