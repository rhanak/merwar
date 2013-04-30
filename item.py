import sys, os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *

class Item(pygame.sprite.Sprite):
	def __init__(self, range_x=(0,900), range_y=(0,630)):
		pygame.sprite.Sprite.__init__(self)
		#self.clock = clock
		#self.time_since_last_rot = 0
		self.degrees = 0
		self.image, self.rect = load_image_alpha("item.png")
		self.base_image, b = load_image_alpha("item.png")
		self.rect.left = random.randrange(range_x[0], range_x[1] - self.rect.width)
		self.rect.top = random.randrange(range_y[0], range_y[1] - self.rect.height)
		self.value = 25
		
	def update(self):
		#self.time_since_last_rot += self.clock.tick()
		#if(self.time_since_last_rot>=250):
		#self.time_since_last_rot = 0
		self.degrees += 5
		#print "Rotated: ", self.degrees
		self.degrees = self.degrees % 360
		self.image = pygame.transform.rotate(self.base_image, -self.degrees)
		self.rect = self.image.get_rect(center=self.rect.center)
		
	def get_value(self):
		return self.value