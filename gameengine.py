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
		self.read_current_assets()

		self.health_protagonist = HealthBar()
		self.health_container = HealthContainer(self.health_protagonist)
		self.healthbars = pygame.sprite.RenderPlain((self.health_container))
		
		self.whiff_sound = load_sound('bubbles.wav')
		#self.stab_sound = load_sound('bubbleshit.wav')

	def update(self):
		background = self.backgrounds[self.curr_list_num]
		self.screen.blit(background, (0,0))
		#self.change_difficulty(
		self.char_manager.update() #)
		#self.change_page(self.char_manager.pagecheck())
		self.update_prot_with_border_checks()
		self.char_manager.draw(self.screen)
		self.healthbars.update()
		self.healthbars.draw(self.screen)
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
		assets = self.assets_list[self.curr_list_num].split('/',2)
		self.char_manager.set_evils(int(assets[0]),assets[1])
		#self.char_manager.set_items(assets[2])
		
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
		self.read_current_assets()
		return True
		
	def change_page_by_offset(self, num):
		''' Attempt to change Page by num.
			Return TRUE if new page valid, FALSE otherwise.
		'''
		if not num: return False
		new_page_num = self.page_num + num
		if((3 * new_page_num > (len(self.backgrounds)-1)) or new_page_num < 0): return False
		self.page_num = new_page_num
		self.curr_list_num += 3*num
		self.read_current_assets()
		return True
	
	### I am wondering whether I could separate the below into a new Class 	###
	### ---DALE 		[TIMER CODE FOLLOWS]								###	
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
		disp_text = font_obj.render(text, 1, (249, 35, 7))
		self.screen.blit(disp_text, (x,y))

