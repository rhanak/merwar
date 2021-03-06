from __future__ import division
import os, pygame
from pygame.locals import *
from utils import *

class HealthContainer(pygame.sprite.Sprite):
	def __init__(self, healthbar):
		pygame.sprite.Sprite.__init__(self)
		
		screen = pygame.display.get_surface()
		width = 150 
		height = 30
		
		self.healthbar = healthbar
		self.area = screen.get_rect()
		self.rect = pygame.Rect(0, self.area.bottom - height, width, height)
		self.image = pygame.Surface([width, height])
		self.image.set_alpha(50)
		self.image.fill((255,255,255))
		
		self.rect_health = pygame.Rect(5, 10, healthbar.width, healthbar.height)
		
	def update(self):
		self.healthbar.update()
		
		self.image.blit(self.healthbar.image, self.rect_health)

class MultipleHealthContainer(pygame.sprite.Sprite):
	def __init__(self, healthbars):
		pygame.sprite.Sprite.__init__(self)
		
		screen = pygame.display.get_surface()
		width = 150 
		height = 30
		
		self.healthbar = healthbar
		self.area = screen.get_rect()
		self.rect = pygame.Rect(0, self.area.bottom - height, width, height)
		self.image = pygame.Surface([width, height])
		self.image.set_alpha(50)
		self.image.fill((255,255,255))
		
		self.rect_health = pygame.Rect(5, 10, healthbar.width, healthbar.height)
		
	def update(self):
		self.healthbar.update()
		
		self.image.blit(self.healthbar.image, self.rect_health)


class HealthBar(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.width = 125 
		self.height = 15

		self.image = pygame.Surface([self.width, self.height])
		self.rect = self.image.get_rect()
		
		self.health = 1
		
	def update(self):
		health_width = self.width * self.health

		self.image.fill((0,0,0))
		self.image.fill((255,255,0), pygame.Rect(0,0, health_width, self.height))

	def inc_health(self, health):
		if(health < 0 or health > 100):
			print "Error invalid value for health: %d" % health

		healthChange = health / 100
		self.health = self.health + healthChange

	def dec_health(self, health):
		if(health < 0 or health > 100):
			print "Error invalid value for health: %d" % health

		healthChange = health / 100
		self.health = self.health - healthChange

	def event(self, event):
		grouping, action, value = event
		if(grouping == "health"):
			if(action == "increased"):
				self.inc_health(value)
			elif(action == "decreased"):
				self.dec_health(value)