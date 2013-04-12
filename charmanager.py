import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *

class CharManager():
	def __init__( self, protagonist, evils):
		self.prot = protagonist
		self.evil = evils
		self.protg = pygame.sprite.GroupSingle( self.prot )
		
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
		self.prot.update()
		return self.difficulty()
		
	def draw( self, screen ):
		self.protg.draw( screen )
		self.evil.draw( screen )
		#pygame.display.flip() 
	
	def difficulty(self):
		prot = self.prot
		# Protaginist going to an easier level
		if(prot.rect.top<30):
			prot.rect.bottom = 590
			prot.rect.left = 100
			if(self.currentdifficulty=="normal"):
				self.currentdifficulty = "easy"
			elif(self.currentdifficulty=="hard"):
				self.currentdifficulty = "normal"
			#self = Mermaid(self.properties,self.enemies,self.enemyManager)
			return (True, False)
		# Nah they are up for something harder
		elif(prot.rect.bottom>600):
			prot.rect.top = 40
			prot.rect.left = 100
			if(self.currentdifficulty=="normal"):
				self.currentdifficulty = "hard"
			elif(self.currentdifficulty=="easy"):
				self.currentdifficulty = "normal"
			#self = Mermaid(self.properties,self.enemies,self.enemyManager)
			return (True,True)
		# No change in difficulty 
		return (False, False)
		
	def set_evils( self, evils):
		self.evil = evils
				
	def evil_helper(self, spriteA, spriteB):
		spriteA.interactWith(spriteB, None)