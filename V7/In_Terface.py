import numpy as np
import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
import sys
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from Pygames.Inquiry import *
from Pygames.Button import *
from Pygames.Saved_State import Saved_State
from Object import *
import copy

#Class that controls the pygame window has two main modes
#Setup mode for the customer to place objects
#Show mode to show the simulations

class In_Terface:

	#null
	def __init__(self):

		#Frames per second
		self.FPS = 20

		#C'est les marges de la partie interative de l'ecran
		self.screen_x_min = 100
		self.screen_y_min = 10
		

	#null
	def initialize_interface(self):
		'''
		Initiliaze tout et ouvre la fenêtre du client
		'''


		self.setup_buttons()
		
		self.load_objects()
		self.calculate_screen_limits()
		
		self.initialize_window()
		self.main_loop()

		self.quit()

	#null
	def initialize_silent_interface(self):
		'''
		Initialize l'interface mais n'ouvre pas la fênetre client, 
		c'est pour aller plus vite en developpement
		'''

		self.setup_buttons()
		
		self.load_objects()
		self.calculate_screen_limits()

	#null
	def setup_buttons(self):
		'''
		BIENTOT VA CHANGER!

		Mets en place les boutons
		'''

		save_pos = (10, 12)
		add_pos = (10, 40)
		quit_pos = (10, 68)

		button_dimensions = (70, 20)

		save_message = "Garder"
		add_message = "Rajouter"
		quit_message = "Simuler"

		green = (0, 200, 0)
		brigth_green = (0, 255, 0)

		self.save_button = Button(save_pos, button_dimensions, green, brigth_green, save_message)
		self.add_button = Button(add_pos, button_dimensions, green, brigth_green, add_message)
		self.quit_button = Button(quit_pos, button_dimensions, green, brigth_green, quit_message)

	#null
	def load_objects(self):
		'''
		Charge l'état sauvgardé, en cas où il n'y a pas elle crée un nouveu fichier vide
		pour le moment elle toujours cherche le fichier 'saved_state.txt'
		Le fichier est sauvgarde avec Pickle
		'''

		config = Path('saved_state.txt')

		#if existing saved state
		if config.is_file():

			with open("saved_state.txt", "rb") as f:
				self.saved_state = pickle.load(f)
			
			objects = self.saved_state.objects

			number_obj = len(objects)

			self.objects = objects

			self.screen_size = self.saved_state.get_screen_size()
		

		#if not ask user for details
		else:

			self.objects = []
			self.screen_size = self.perform_window_inquiry()
			self.saved_state = Saved_State(self.screen_size, self.objects)

	#null
	def main_loop(self):
		'''
		C'est le loop principal du mode interactive / mode client
		BIENTOT les boutons serions streamlined
		'''

		#unpack variables
		number_obj = len(self.objects)
		screen = self.screen
		save_button = self.save_button
		add_button = self.add_button
		quit_button = self.quit_button

		#define variables
		running = True
		white = (255, 255, 255)
		clock = pygame.time.Clock()

		while running:
	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					sys.exit("Error")


				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:

						event_pos = self.adjust_by_margin(event.pos)			
						
						#Remember layers
						for i in range(number_obj):

							if self.objects[i].in_collision(event_pos):

								self.objects[i].start_drag(event_pos)
				
					#change into vector of buttons
						if save_button.in_collision(event.pos):

							save_button.push()

						if add_button.in_collision(event.pos):

							add_button.push()

						if quit_button.in_collision(event.pos):

							quit_button.push()

				elif event.type == pygame.MOUSEBUTTONUP:

						event_pos = self.adjust_by_margin(event.pos)	
						
						if event.button == 1:			

							for i in range(number_obj):

								self.objects[i].end_drag()

							if save_button.is_pushed():

								save_button.release()
								if save_button.in_collision(event.pos):
									
									self.update_saved_state()
									self.save_current_state()

							if add_button.is_pushed():

								add_button.release()
								if add_button.in_collision(event.pos):

									self.add_object()

							if quit_button.is_pushed():

								quit_button.release()
								if quit_button.in_collision(event.pos):
									
									running = False
									
				elif event.type == pygame.MOUSEMOTION:
					event_pos = self.adjust_by_margin(event.pos)	
					#traspass the within limits function to the object class giving the limits
					for i in range(number_obj):
						
						left = 0
						right = self.screen_x_max - self.screen_x_min
						upper = self.screen_y_max - self.screen_y_min
						lower = 0
						self.objects[i].offset_pos(event_pos, left, right, upper, lower)


			screen.fill(white)

			#Remember order of layers, products before obstacles and clicked before all
			margin = np.array([self.screen_y_min, self.screen_x_min])
			for i in range(number_obj):
				self.objects[i].draw(screen, margin)

			#Change into vector of buttons
			save_button.draw(screen)
			add_button.draw(screen)
			quit_button.draw(screen)

			pygame.display.flip()
			clock.tick(self.FPS)
			
			#adjust variables
			number_obj = len(self.objects)


		# - end -

	
	def calculate_screen_limits(self):
		'''
		Definit les marges de la partie interactive
		'''

		screen_size = self.screen_size
		left = 100
		right = 10
		upper = 10
		lower = 10

		self.show_screen_size = np.array((screen_size[0] + left + right, max(screen_size[1] + upper + lower, 100)))
		self.screen_x_max = screen_size[0] + left
		self.screen_x_min = left
		self.screen_y_max = screen_size[1] + lower
		self.screen_y_min = lower


	#pos
	def adjust_by_margin(self, pos):
		'''
		Change la position d'un object pour l'adjuster aux marges
		'''

		return np.array((pos[0] - self.screen_x_min, pos[1] - self.screen_y_min))


	#null
	def add_object(self):
		'''
		Resultat d'apuyer sur le boutton "add object"
		Laisse la choix de taille et type d'object a l'utilissateur
		'''

		type_obj, size= self.perform_object_inquiry()
		pos = np.array((0,0))
		#pos = self.adjust_by_margin(pos)

		if type_obj == "Error":
			return
		elif type_obj == "Obstacle":
			self.objects.append(Obstacle(pos, size))
		elif type_obj == 'People':
			self.objects.append(Initial_Value(pos, size))
		elif type_obj == 'Entry':
			self.objects.append(Entry(pos, size))
		elif type_obj == 'Exit':
			self.objects.append(Exit(pos, size))
		elif type_obj == 'Product':
			self.objects.append(Product(pos, size))

	#type, size
	def perform_object_inquiry(self):
		'''
		Appelle le module inquiry pour faire une demande a l'utilisateur
		Elle demande type d'objet et taille
		'''


		inquiry = Object_Inquiry()
		return inquiry.get()

	#screen_size
	def perform_window_inquiry(self):
		'''
		Appelle le module inquiry pour faire une demande a l'utilisateur
		Elle demande les dimension de l'ecran
		'''
		inquiry = Window_Inquiry()
		return inquiry.get()		

	#null
	def update_saved_state(self):
		'''
		C'est un update de l'état à sauvgarder interne, ceci n'est pas le sauvegarde en soit
		'''


		self.saved_state.screen_size = self.screen_size
		margin_x = self.screen_x_min
		margin_y = self.screen_y_min

		number_obj = len(self.objects)
		self.saved_state.objects = copy.deepcopy(self.objects)

		for i in range(number_obj):

			size = self.saved_state.objects[i].get_size()
			pos = self.saved_state.objects[i].get_pos()
			pos = np.array((pos[0], pos[1])).copy()

			self.saved_state.objects[i].position = pos

	#null
	def save_current_state(self):
		'''
		Ceci c'est le sauvgarde proprement
		Utilise le module Pickle pour garder en "saved_state.txt"
		'''


		with open("saved_state.txt", "wb") as f:
			pickle.dump(self.saved_state, f)

	#null
	def initialize_window(self):
		'''
		Cree la fenêtre pygame aux dimentions indiquées
		'''


		title = "Display Magazin"
		pygame.init()
		self.screen = pygame.display.set_mode(self.show_screen_size)
		pygame.display.set_caption(title)

	#null
	def quit(self):
		'''
		La fonction quit, elle ne fais pas quit par l'instant car la simulation se fais dans la même fenêtre
		'''

		#pass
		pygame.quit()

	def get_state(self):
		'''
		Retourne l'état actuel, pour accomplir cela il met à jour l'état à sauvgarder
		'''

		self.update_saved_state()
		return self.saved_state