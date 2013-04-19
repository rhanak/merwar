import sys, os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *
from mermaid import *
from charmanager import *
from characters import *
from health import *

kDataDir = 'data'
kGlobals = 'globals.json'

class GameEngine():
	def __init__(self, screen, clock=pygame.time.Clock()):
		###### USED FOR TIMERS
		self.clock = clock	#Currently using a constructed one. Maybe use outside one?
		self.times = [0.0, 0.0, 0.0] #accumulator Easy, Med, Hard times
		self.timer_index = 1	#start on Medium timer
		###### END TIMER STUFF
		self.page_num = 0
		self.curr_list_num = 1
		self.curr_num_enemies = 0
		self.curr_type_enemies = "none"
		self.screen = screen
		self.backgrounds = self.load_backgrounds()
		self.assets_list = self.load_enemy_parameters()
		self.char_manager = CharManager()
		self.health_protagonist = HealthBar()
		self.health_container = HealthContainer(self.health_protagonist)
		self.healthbars = pygame.sprite.RenderPlain((self.health_container))
		
		self.whiff_sound = load_sound('bubbles.wav')
		#self.stab_sound = load_sound('bubbleshit.wav')

	def update(self):
		background = self.backgrounds[self.curr_list_num]
		self.screen.blit(background, (0,0))
		diff = self.char_manager.update()
		self.change_page(self.char_manager.pagecheck())
		self.change_difficulty(diff)
		self.char_manager.draw(self.screen)
		self.healthbars.update()
		self.healthbars.draw(self.screen)
		self.update_timers()

		# Just showing how you can test the health bar for the protagonist
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit("Quit.") 
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit("Quit.") 
			elif event.type == MOUSEBUTTONDOWN:
				self.whiff_sound.play()
			elif event.type is MOUSEBUTTONUP:
				self.health_protagonist.dec_health()
		

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
		'''upOrDown is a boolean value. 0 denotes up; 1 denotes down.'''
		change, upOrDown = diff
		char_m = self.char_manager
		if (change):
			print "Up? ", upOrDown, "; curr_list_num: ", self.curr_list_num
			if (not upOrDown) and ((self.curr_list_num % 3) > 0):
				self.curr_list_num-=1
				char_m.push_new_rect()
			elif upOrDown and ((self.curr_list_num % 3) < 2):
				self.curr_list_num+=1
				char_m.push_new_rect()

			self.screen.blit(self.backgrounds[self.curr_list_num], (0,0))
			pygame.display.flip()
		
	def change_page(self, leftOrRight):
		'''leftOrRight is "left" or "right". If NoneType, do nothing.'''
		if not leftOrRight: return
		print leftOrRight
		if(leftOrRight == "left" and self.page_num > 0):
			self.page_num -= 1
			self.curr_list_num-=3
		elif(leftOrRight == "right" and self.page_num < len(self.backgrounds)/3 - 1):
			self.page_num += 1
			self.curr_list_num += 3
		#self.char_manager.push_new_rect()
		self.screen.blit(self.backgrounds[self.curr_list_num], (0,0))
		pygame.display.flip()
	
	### I am wondering whether I could separate this into a new Class 	###
	### ---DALE 		[TIMER CODE FOLLOWS]							###	
	def update_timers(self):
		''' Called from the main update function, this will update and display 
			the	timer for the currently active difficulty level '''
		self.timer_index = self.curr_list_num % 3
		self.times[self.timer_index] += self.clock.tick()
		self.display_text("Level " + str(self.timer_index + 1) + ":" + 
		"{:10.2f}".format(self.times[self.timer_index]/1000.0) +"s", 20, 20)
		
	def display_text(self, text, x, y):
		''' Display the passed text at the coordinates (x,y) in 
			a sufficiently visible font '''
		font_obj = pygame.font.SysFont("arial", 20, bold=True)
		disp_text = font_obj.render(text, 1, (204, 102, 0))
		self.screen.blit(disp_text, (x,y))
		pygame.display.flip()

