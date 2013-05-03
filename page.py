import pygame
#from string import *

class Page():
	def __init__(self):
		self.enemies = []
		self.num_items = 0
		
	def set_enemies(self, enemies):
		self.enemies = enemies	
		
	def add_enemy(self, num, type_):
		self.enemies.append((num, type_))
		
	def clear_enemies(self):
		self.enemies = []
		
	def set_num_items(self, num):
		self.num_items = num
		
	def  __str__(self):
		s = "enemies " + ', '.join(map(str, self.enemies))
		s += "items %d" % self.num_items
		return s
		