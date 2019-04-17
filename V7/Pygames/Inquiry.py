import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import numpy as np



choices = { 'Meuble', 'Article'}

# Add objects
class Inquiry():
		
	#Returns None
	#Calls None
	def __init__(self):

		self.root = tk.Tk()
		self.makeform()

		button = tk.Button(self.root, text = 'Enter', command=self.quit)
		button.pack()

		self.root.mainloop()

	#Returns tk.Frame (mainframe)
	#Calls None
	def setup_mainframe(self):

		mainframe = tk.Frame(self.root)
		mainframe.grid(column=0,row=0 )
		mainframe.columnconfigure(0, weight = 1)
		mainframe.rowconfigure(0, weight = 1)
		mainframe.pack(pady = 100, padx = 100)

		return mainframe


class Object_Inquiry(Inquiry):

	#Returns None
	#Calls None
	def quit(self):

		self.type = self.type_entry.get()

		for i in range(len(self.labels)):
			self.answer[i] = int(self.entry[i].get())

		self.root.destroy()
		
	#Returns None
	#Calls None
	def makeform(self):
		#Set window parameters
		mainframe = self.setup_mainframe()

		#if window is closed
		self.type = 'Error'

		#Add pull down menu
		choices = { 'Obstacle', 'People', 'Entry', 'Exit', 'Product'}
		self.type_entry = tk.StringVar(self.root)
		self.type_entry.set('Obstacle')
		popupMenu = tk.OptionMenu(mainframe, self.type_entry, *choices)
		tk.Label(mainframe, text="Type").grid(row = 1, column = 0)
		popupMenu.grid(row = 1, column = 1)

		#Add numerical entries
		self.labels = ["Length", "Heigth"]
		self.answer = [0] * len(self.labels)
		self.entry = [0] * len(self.labels)
		for i in range(len(self.labels)):

			tk.Label(mainframe, text=self.labels[i]).grid(row = i + 2, column = 0)
			self.entry[i] = tk.Entry(mainframe)
			self.entry[i].grid(row=i + 2, column=1)

	#Returns string (type), list (answer)
	#Calls None 
	def get(self):

		return self.type, np.array(self.answer)


class Window_Inquiry(Inquiry):

	def quit(self):

		for i in range(len(self.labels)):
			self.answer[i] = int(self.entry[i].get())

		self.root.destroy()

	def makeform(self):

		#Set window parameters
		mainframe = self.setup_mainframe()
		self.answer = [0,0]

		#Add numerical entries
		self.labels = ["Screen length", "Screen heigth"]
		self.entry = [0] * len(self.labels)

		for i in range(len(self.labels)):

			tk.Label(mainframe, text=self.labels[i]).grid(row = i + 1, column = 0)
			self.entry[i] = tk.Entry(mainframe)
			self.entry[i].grid(row= i + 1, column=1)

	
	#Returns list (answer)
	#Calls None 
	def get(self):

		return np.array(self.answer)

'''
pending

class File_Inquiry(Inquiry):

	def quit(self):

	def makeform(self):

	def get(self):
'''