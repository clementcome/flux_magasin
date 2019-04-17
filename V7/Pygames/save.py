import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from Obstacle import *

# Saving
def save_state(rect_ob):

	saveable = [0] * len(rect_ob)

	for i in range(len(rect_ob)):
		saveable[i] = rect_ob[i].get_savestate()

	with open("savegame.txt", "wb") as f:
		pickle.dump(saveable, f)


def load_state():
	with open("savegame.txt", "rb") as f:
		return pickle.load(f)
