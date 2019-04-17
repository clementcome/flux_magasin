import pygame
import smtplib, ssl
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

# Saving
def save_path(paths, file = "paths.txt"):

	with open(file, "wb") as f:
		pickle.dump(paths, f)


def load_path(file = "paths.txt"):
	with open(file, "rb") as f:
		return pickle.load(f)

def distance_path(path1, path2):

	return ((path2 - path1)**2).mean()
