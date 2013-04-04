import os, pygame, json, random, csv
from pygame.locals import *
from utils import *

class PageManager():
	def __init__(self,screen):
		self.difficulty = "normal"
		self.page_num = 0
		self.curr_list_num = 1
		self.curr_num_enemies = 0
		self.curr_type_enemies = "none"
		self.screen = screen
		self.backgrounds = self.load_backgrounds()
		self.enemy_list = self.load_enemy_parameters()
		
	def update(self):
		background = self.backgrounds[self.curr_list_num]
		self.screen.blit(background, (0,0))
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
		
	def change_difficulty(self, upOrDown):
		'''upOrDown is a boolean value. 0 denotes up; 1 denotes down.'''
		if((self.difficulty=="easy" and not upOrDown) or (self.difficulty=="hard" and upOrDown)):
			return
		if(self.difficulty=="easy" and upOrDown):
			self.difficulty = "normal"
			self.curr_list_num+=1
		elif(self.difficulty=="hard" and not upOrDown):
			self.difficulty = "normal"
			self.curr_list_num-=1
		elif(self.difficulty=="normal" and upOrDown):
			self.difficulty = "hard"
			self.curr_list_num+=1
		elif(self.difficulty=="normal" and not upOrDown):
			self.difficulty = "easy"
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
		