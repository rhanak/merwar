import os, pygame, json, random, csv, math
from pygame.locals import *
from characters import *
from mermaid import *
from utils import *

kDataDir = 'data'
kGlobals = 'globals.json'

class CharManager():
	def __init__( self):
		self.propsfiles = []
		for character in csv.DictReader( open( os.path.join( kDataDir, 'characters.csv' ) ) ):
			self.propsfiles.append(character)
		mermaid = Mermaid(self.propsfiles[0])
		dfm = Enemy(self.propsfiles[1])
	
		self.prot = mermaid
		self.evil = pygame.sprite.Group()
		self.items = 0
		self.protg = pygame.sprite.GroupSingle( self.prot )
		self.currentdifficulty = "normal"
		self.evil.add(dfm)
		
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
		self.evil.update(self.prot.get_position())
		self.prot.update()
		return self.difficulty()
		
	def draw( self, screen ):
		self.protg.draw( screen )
		self.evil.draw( screen )
		#pygame.display.flip() 
	
	def difficulty(self):
		prot = self.prot
		changeDifficulty = False
		# Protaginist going to an easier level
		if(prot.rect.top<30):
			prot.rect.bottom = 590
			prot.rect.left = 100
			if(self.currentdifficulty=="normal"):
				changeDifficulty = True
				self.currentdifficulty = "easy"
			elif(self.currentdifficulty=="hard"):
				changeDifficulty = True
				self.currentdifficulty = "normal"
			#self = Mermaid(self.properties,self.enemies,self.enemyManager)
			return (changeDifficulty, False)
		# Nah they are up for something harder
		elif(prot.rect.bottom>600):
			prot.rect.top = 40
			prot.rect.left = 100
			if(self.currentdifficulty=="normal"):
				changeDifficulty = True
				self.currentdifficulty = "hard"
			elif(self.currentdifficulty=="easy"):
				changeDifficulty = True
				self.currentdifficulty = "normal"
			#self = Mermaid(self.properties,self.enemies,self.enemyManager)
			return (changeDifficulty,True)
		# No change in difficulty 
		return (False, False)
		
	def set_evils( self, num_enemies, type_enemies):
		evil.clear()
		'''add in type differences'''
		for x in num_enemies:
			evil.add(Shark())
		
	def set_items(self, item_num):
		self.items = createNewItems(item_num)
				
	def evil_helper(self, spriteA, spriteB):
		spriteA.interactWith(spriteB, None)