import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename


def text_objects(font, text, color, text_center):
	rendered = font.render(text, True, color)
	return rendered, rendered.get_rect(center=text_center)

class Button:

	def __init__(self, pos_initial, taille, normal_color, bright_color, message):

		self.pushed = False
		self.rect = pygame.rect.Rect(pos_initial[0], pos_initial[1], taille[0], taille[1])
		self.normal_color = normal_color
		self.bright_color = bright_color
		self.message = message

	def draw(self, screen):
		BLACK = (  0,   0,   0)
		
		if not self.pushed:
			pygame.draw.rect(screen, self.normal_color, self.rect)
		else:
			pygame.draw.rect(screen, self.bright_color, self.rect)
		x = 'Sans'
		screen_rect = screen.get_rect()
		font = pygame.font.SysFont(x, 18)
		screen.blit(*text_objects(font, self.message, BLACK, (self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2)))

	def in_collision(self, event_pos):

		return self.rect.collidepoint(event_pos)

	def push(self):

		self.pushed = True

	def is_pushed(self):

		return self.pushed

	def release(self):

		self.pushed = False

	def set_message(self, message):

		self.message = message