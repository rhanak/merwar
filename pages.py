import os, pygame, json, random, csv
from pygame.locals import *
from utils import *

class PageManager():
	def __init__(self):
		self.difficulty = "normal"
		self.curr_num_enemies = 0
		self.curr_type_enemies = "none"

	def load_backgrounds(self):
		e1 = pygame.image.load(path_rejoin('data/backgrounds/undertheseaeasy.png')).convert()
		n1 = pygame.image.load(path_rejoin('data/backgrounds/underthesea.png')).convert()
		h1 = pygame.image.load(path_rejoin('data/backgrounds/undertheseahard.png')).convert()
		background_list = [e1,n1,h1]
		return background_list