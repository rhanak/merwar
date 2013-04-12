import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *

class CharManager():
	def __init__( self, protagonist, evils):
		self.prot = protagonist
		self.evil = evils
		
	def evil_collide( self ):
		ev_copy = self.evil.copy()
		ev_sprites = ev_copy.sprites()
		for sprite in ev_sprites:
			ev_copy.remove( sprite )
			listc = pygame.sprite.spritecollide( sprite, ev_copy, dokill = False)
			for clsn in listc:
				self.evil_helper(sprite, clsn)
	
	def update( self ):
		self.evil_collide()
		self.evil.update()
		return self.prot.update()
		
	def set_evils( self, evils):
		self.evil = evils
				
	def evil_helper(self, spriteA, spriteB):
		spriteA.interactWith(spriteB, None)