import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *
from mermaid import *
from charmanager import *

kDataDir = 'data'
kGlobals = 'globals.json'

class GameEngine():
	def __init__(self,screen):
		self.page_num = 0
		self.curr_list_num = 1
		self.curr_num_enemies = 0
		self.curr_type_enemies = "none"
		self.screen = screen
		self.backgrounds = self.load_backgrounds()
		self.enemy_list = self.load_enemy_parameters()
		
		for character in csv.DictReader( open( os.path.join( kDataDir, 'maze_characters.csv' ) ) ):
			mermaid = Mermaid(character)
		mermaidg = pygame.sprite.Group( ( mermaid ) )
		
		self.char_manager = CharManager(mermaid, pygame.sprite.Group())
		
	def update(self):
		background = self.backgrounds[self.curr_list_num]
		self.screen.blit(background, (0,0))
		diff = self.char_manager.update()
		self.change_difficulty(diff)
		pygame.display.flip()

	def load_backgrounds(self):
		e0 = pygame.image.load(path_rejoin('data/backgrounds/undertheseaeasy.png')).convert()
		n0 = pygame.image.load(path_rejoin('data/backgrounds/underthesea.png')).convert()
		h0 = pygame.image.load(path_rejoin('data/backgrounds/undertheseahard.png')).convert()
		e1 = pygame.image.load(path_rejoin('data/backgrounds/e1.png')).convert()
		n1 = pygame.image.load(path_rejoin('data/backgrounds/n1.png')).convert()
		h1 = pygame.image.load(path_rejoin('data/backgrounds/h1.png')).convert()
		background_list = [e1,n1,h1]
		return background_list
		
	def load_enemy_parameters(self):
		enemies_list = []
		for difficulty in csv.DictReader( open( os.path.join( 'data/screens.csv' ) ) ):
			enemies_list.append(difficulty['page 1'])
		return enemies_list
		
	def change_difficulty(self, diff):
		'''upOrDown is a boolean value. 1 denotes up; 0 denotes down.'''
		change, upOrDown = diff
		if (change):
			if(upOrDown):
				self.curr_list_num+=1
			else:
				self.curr_list_num-=1
			
		self.screen.blit(self.backgrounds[self.curr_list_num], (0,0))
		pygame.display.flip()
		
	def change_page(self, leftOrRight):
		'''leftOrRight is a boolean value. 0 denotes left; 1 denotes right.'''
		if(not leftOrRight):
			self.page_num -= 1
			self.curr_list_num-=3
		elif(leftOrRight):
			self.page_num -= 1
			self.curr_list_num+=3
		self.screen.blit(self.backgrounds[self.curr_list_num], (0,0))
		pygame.display.flip()