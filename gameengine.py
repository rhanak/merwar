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
		self.assets_list = self.load_enemy_parameters()
		self.char_manager = CharManager()
		
	def update(self):
		background = self.backgrounds[self.curr_list_num]
		self.screen.blit(background, (0,0))
		diff = self.char_manager.update()
		self.change_difficulty(diff)
		self.char_manager.draw(self.screen)

	def load_backgrounds(self):
		e0 = pygame.image.load(path_rejoin('data/backgrounds/e0.png')).convert()
		n0 = pygame.image.load(path_rejoin('data/backgrounds/n0.png')).convert()
		h0 = pygame.image.load(path_rejoin('data/backgrounds/h0.png')).convert()
		e1 = pygame.image.load(path_rejoin('data/backgrounds/e1.png')).convert()
		n1 = pygame.image.load(path_rejoin('data/backgrounds/n1.png')).convert()
		h1 = pygame.image.load(path_rejoin('data/backgrounds/h1.png')).convert()
		background_list = [e0,n0,h0,e1,n1,h1]
		return background_list
		
	def get_opening_screen(self):
		return self.backgrounds[1]
		
	def load_enemy_parameters(self):
		assets_list = []
		for difficulty in csv.DictReader( open( os.path.join( 'data/screens.csv' ) ) ):
			assets_list.append(difficulty['page 1'])
		for difficulty in csv.DictReader( open( os.path.join( 'data/screens.csv' ) ) ):
			assets_list.append(difficulty['page 2'])
		for difficulty in csv.DictReader( open( os.path.join( 'data/screens.csv' ) ) ):
			assets_list.append(difficulty['page 3'])
		return assets_list
		
	def read_current_assets(self):	
		assets = self.assets_list.split('/',2)
		self.char_manager.set_evils(assets[0],assets[1])
		self.char_manager.set_items(assets[2])
		
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