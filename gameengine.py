import sys, os, pygame, json, random, csv, math, threading
from pygame.locals import *
from utils import *
from mermaid import *
from charmanager import *
from characters import *
from dalesutils import *
from selectscreen import *
from gameconditions import *
from page import *

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
		
		self.screen = screen
		self.backgrounds = self.load_backgrounds()
		self.pages = self.load_enemy_parameters()
		
		# A thread inside Character manager uses this to communicate with the main thread
		self.eventThreading = threading.Event()
		self.char_manager = CharManager(screen, self.eventThreading)
		self.gameConditions = GameConditions(screen, self.eventThreading, self.resetGame, self.times)
		
		self.move_to_first_page()
		
		self.set_current_assets()
		
		self.whiff_sound = load_sound('bubbles.wav')
		#self.stab_sound = load_sound('bubbleshit.wav')
		

	def update(self):
		self.gameConditions.update()
		
		if(self.page_num == 8 and not self.char_manager.evil):
			self.gameConditions.win()
			#print "You won!"
		
		if(self.gameConditions.isNormalPlay()):
			if(self.curr_list_num < len(self.backgrounds)):
				background = self.backgrounds[self.curr_list_num]
				self.screen.blit(background, (0,0))
			#self.change_difficulty(
			self.char_manager.update() #)
			#self.change_page(self.char_manager.pagecheck())
			self.update_prot_with_border_checks()
			self.char_manager.draw(self.screen)
			self.update_timers()
		
		pygame.display.flip()
		
		
		
		# Just showing how you can test the health bar for the protagonist
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit("Quit.") 
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit("Quit.") 
			elif event.type == MOUSEBUTTONDOWN:
				self.whiff_sound.play()
	
	def resetGame(self):
		self.char_manager.resetGame()
		
		# Reset the timers
		for i in range(0,len(self.times)):
			self.times[i] = 0.0
		
		# Reload the enemies
		self.set_current_assets()
		
		# Move the protoganist to the first page
		self.char_manager.move_protagonist((100, 300))
		self.move_to_first_page()
				
	def load_backgrounds(self):
		#0
		e0 = pygame.image.load(path_rejoin('data/backgrounds/e0.png')).convert()
		n0 = pygame.image.load(path_rejoin('data/backgrounds/n0.png')).convert()
		h0 = pygame.image.load(path_rejoin('data/backgrounds/h0.png')).convert()
		#1
		e1 = pygame.image.load(path_rejoin('data/backgrounds/e1.png')).convert()
		n1 = pygame.image.load(path_rejoin('data/backgrounds/n1.png')).convert()
		h1 = pygame.image.load(path_rejoin('data/backgrounds/h1.png')).convert()
		#2
		e2 = pygame.image.load(path_rejoin('data/backgrounds/e2.png')).convert()
		n2 = pygame.image.load(path_rejoin('data/backgrounds/n2.png')).convert()
		h2 = pygame.image.load(path_rejoin('data/backgrounds/h2.png')).convert()
		#3
		e3 = pygame.image.load(path_rejoin('data/backgrounds/e3.png')).convert()
		n3 = pygame.image.load(path_rejoin('data/backgrounds/n3.png')).convert()
		h3 = pygame.image.load(path_rejoin('data/backgrounds/h3.png')).convert()
		#4
		e4 = pygame.image.load(path_rejoin('data/backgrounds/e4.png')).convert()
		n4 = pygame.image.load(path_rejoin('data/backgrounds/n4.png')).convert()
		h4 = pygame.image.load(path_rejoin('data/backgrounds/h4.png')).convert()
		#5
		e5 = pygame.image.load(path_rejoin('data/backgrounds/e5.png')).convert()
		n5 = pygame.image.load(path_rejoin('data/backgrounds/n5.png')).convert()
		h5 = pygame.image.load(path_rejoin('data/backgrounds/h5.png')).convert()
		#6
		e6 = pygame.image.load(path_rejoin('data/backgrounds/e6.png')).convert()
		n6 = pygame.image.load(path_rejoin('data/backgrounds/n6.png')).convert()
		h6 = pygame.image.load(path_rejoin('data/backgrounds/h6.png')).convert()
		#7
		e7 = pygame.image.load(path_rejoin('data/backgrounds/e7.png')).convert()
		n7 = pygame.image.load(path_rejoin('data/backgrounds/n7.png')).convert()
		h7 = pygame.image.load(path_rejoin('data/backgrounds/h7.png')).convert()
		#8
		e8 = pygame.image.load(path_rejoin('data/backgrounds/e8.png')).convert()
		n8 = pygame.image.load(path_rejoin('data/backgrounds/n8.png')).convert()
		h8 = pygame.image.load(path_rejoin('data/backgrounds/h8.png')).convert()
		background_list = [e0,n0,h0,e1,n1,h1,e2,n2,h2,e3,n3,h3,e4,n4,h4,e5,n5,h5,e6,n6,h6,e7,n7,h7,e8,n8,h8]
		return background_list
		
	def get_opening_screen(self):
		return self.backgrounds[1]
		
	def create_page(self, pageParts):
		# Iterate over the different enemy types for this page
		print "Creating page"
		page = Page()
		for enemy in pageParts.split(';', -1):
			print enemy
			parts = enemy.split('/',3)
			# If len is 2 we don't have number of health items 
			if(len(parts) == 2):
				page.add_enemy(int(parts[0]), parts[1])
			elif(len(parts) == 3):
				page.add_enemy(int(parts[0]), parts[1])
				page.set_num_items(int(parts[2]))
		print page
		return page
		
	def load_enemy_parameters(self):
		crap = ['page 0', 'page 1', 'page 2', 'page 3', 'page 4','page 5','page 6', 'page 7', 'page 8']
		pages = []
		for dudu in crap: 
			for difficulty in csv.DictReader( open( os.path.join( 'data/screens.csv' ) ) ):
				page = self.create_page(difficulty[dudu])
				pages.append(page)
		return pages
		
	def set_current_assets(self): 
		print self.current_page
		self.char_manager.set_assets(self.current_page)
		
	def update_prot_with_border_checks(self):
		''' Use more modular functions from charmanager to check borders
			and update the protagonist appropriately '''
		char_m = self.char_manager
		#### atDiffBorder/atPageBorder will give 0 if none needed, so won't add/subtract
		diff_change = self.change_diff_by_offset(char_m.atDiffBorder())
		page_change = self.change_page_by_offset(char_m.atPageBorder())
		####
		char_m.move_prot_by_border_checks(diff_change, page_change)
		
	def change_diff_by_offset(self, num):
		''' Attempt to change Difficulty by num.
			Return TRUE if new difficulty valid, FALSE otherwise.
		'''
		if not num: return False
		diff = self.curr_list_num % 3
		if((diff == 0 and num < 0) or (diff==2 and num > 0)): 
			return False
		self.curr_list_num += num
		#print "Difficulty list val: ", self.curr_list_num
		self.set_current_assets()
		return True
	
	def move_to_first_page(self): 
		self.current_page = self.pages[0]
		self.change_page(0)
	
	def change_page(self, page_num):
		self.page_num = page_num
		self.curr_list_num = 3*page_num
		
		# Update the current page with the enemies and items before changing pages
		self.update_before_page_change()
	
	def change_page_by_offset(self, num):
		''' Attempt to change Page by num.
			Return TRUE if new page valid, FALSE otherwise.
		'''
		if not num: return False
		new_page_num = self.page_num + num
		if((3 * new_page_num > (len(self.backgrounds)-1)) or new_page_num < 0): return False
		self.page_num = new_page_num
		self.curr_list_num += 3*num
		
		# Update the current page with the enemies and items before changing pages
		self.update_before_page_change()
	
		return True
		
	def update_before_page_change(self):
		self.current_page = self.pages[self.curr_list_num]
		
		# Update the current page with the enemies and items before changing pages
		#BIG TODO
		#self.char_manager.update_page_before_changing(self.current_page)
		
		# Set the assets for the current page
		self.set_current_assets()
	
	### I am wondering whether I could separate the below into a new Class	###
	### ---DALE			[TIMER CODE FOLLOWS]								### 
	def update_timers(self):
		''' Called from the main update function, this will update and display 
			the timer for the currently active difficulty level '''
		self.timer_index = self.curr_list_num % 3
		self.times[self.timer_index] += self.clock.tick()
		display_text(self.screen, "Level " + str(self.timer_index + 1) + ":" + 
		"{:10.2f}".format(self.times[self.timer_index]/1000.0) +"s", 20, 20)
		

