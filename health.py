import os, pygame
from pygame.locals import *
from utils import *

class HealthProtagonist(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		screen = pygame.display.get_surface()
		width = 150 
		height = 30
		self.area = screen.get_rect()
		self.rect = pygame.Rect(0, self.area.bottom - height, width, height)

		self.image = pygame.Surface([width, height])
		self.image.set_alpha(50)
		self.image.fill((255,255,255))

		self.health_bar_width = width - 25
		self.health_bar_height = height/2

		self.health_rect_max = pygame.Rect(5, 10, self.health_bar_width, self.health_bar_height)
		self.health_max_image = pygame.Surface([self.health_bar_width, self.health_bar_height])
		

		self.health = .9
		
	def update(self):
		health_width = self.health_bar_width * self.health

		self.health_max_image.fill((0,0,0))
		self.health_max_image.fill((255,255,0), pygame.Rect(0,0, health_width, self.health_bar_height))
		self.image.blit(self.health_max_image, self.health_rect_max)

	def set_health(self, health):
		if(health < 0 or health > 100):
			print "Error invalid value for health: %d" % health

		self.health = health / 100

	def dec_health(self, ):
		self.set_health((self.health - .05) * 100)