import os, pygame, json, random, csv, math, threading, time
from pygame.locals import *
from characters import *
from mermaid import *
from item import *
from utils import *
from health import *
from dalesutils import *

kDataDir = 'data'
kGlobals = 'globals.json'

class CharManager():
	def __init__( self, screen, event ):
		self.propsfiles = []
		for character in csv.DictReader( open( os.path.join( kDataDir, 'characters.csv' ) ) ):
			self.propsfiles.append(character)
		mermaid = Mermaid(self.propsfiles[0])
		dfm = Enemy(self.propsfiles[1], self)
		
		self.screen = screen
		self.eventThreading = event
		self.prot = mermaid
		self.evil = pygame.sprite.RenderPlain(dfm)
		self.items = pygame.sprite.Group()
		self.protg = pygame.sprite.GroupSingle( self.prot )
		
		self.health_setup()
	
	def health_setup(self):
		health_protagonist = HealthBar()
		self.prot.addListener(health_protagonist)
		self.prot.addListener(self)
		self.healthbars = pygame.sprite.RenderPlain((HealthContainer(health_protagonist)))
		
	# Character manager listens for events and when the players health is "gone" -- signalling GAME OVER	
	def event(self, event):
		grouping, action, value = event
		if(grouping == "health"):
			if(action == "decreased"):
				if(self.prot.health < 1):
					eventing = self.eventThreading
					def hello():
						#print "Set zero"
						eventing.set()
						time.sleep(2)
						#print "Set one"
						eventing.set()

					t = threading.Timer(0.0, hello)
					t.start()
					
	def evil_collide( self ):
		ev_copy = self.evil.copy()
		ev_sprites = ev_copy.sprites()
		for sprite in ev_sprites:
			ev_copy.remove( sprite )
			listc = pygame.sprite.spritecollide( sprite, ev_copy, dokill = False)
			for clsn in listc:
				self.evil_helper(sprite, clsn)
				
	def check_prot_attack_evil( self ):
		listc = pygame.sprite.spritecollide( self.prot, self.evil, dokill = False)
		closest = self.closest_evil( listc )
		for enemy in listc:
			if(not self.prot.combo_state.in_default_state()\
				and not self.prot.combo_state.dodging()):
				if enemy is closest:
					enemy.damageEnemy(self.prot.attackPower)
				else:
					enemy.damageEnemy(self.prot.attackPower/2)
				#print "This enemy is being attacked by prot %s" % enemy
	
	def closest_evil( self, collided_list ):
		if not collided_list: return None
		closest = collided_list[0]
		dist = math.hypot(self.prot.rect.centerx - closest.rect.centerx, \
			self.prot.rect.centery - closest.rect.centery)
		for enemy in collided_list:
			dist_d = math.hypot(self.prot.rect.centerx - enemy.rect.centerx, \
			self.prot.rect.centery - enemy.rect.centery)
			if (dist_d < dist):
				dist = dist_d
				closest = enemy
		return closest
	
	def update( self ):
		self.evil_collide()
		self.check_prot_attack_evil()
		self.evil.update(self.prot.get_position())
		self.prot.update()
		self.check_use_items()
		self.items.update()
		self.healthbars.update()
		#return self.difficulty()
		
	def draw( self, screen ):
		self.protg.draw( screen )
		self.evil.draw( screen )
		self.items.draw( screen )
		self.healthbars.draw( screen )
	
	### NEW BORDER CHECKING POSITION UPDATE FUNCTIONS
	### WHAT TO DO: 
	### 1.	Use atDiffBorder() and atPageBorder() to determine engine level changes
	### 2.	Call move_prot_by_border_checks(diff, page) from engine,
	###		where diff and page, Bools, indicate whether they should change.
	### ---Dale
	def diffUpOrDown(self):
		''' Vertical: return the rect.top value of where the mermaid should
			end up IF difficulty changes. Difficulty changes are
			tracked in the Game Engine now.
		'''
		if(self.prot.rect.top<10):
			return (630 - self.prot.rect.height - 10)
		elif(self.prot.rect.bottom>620):
			return 20
		return self.prot.rect.top
	
	def atDiffBorder(self):
		''' Vertical: return -1 if protagonist collides with top border 
						return 1 if protagonist collides with bottom border
						0 if no collision. 1 and -1 evaluate to Boolean TRUE
		'''
		if(self.prot.rect.top<10):
			return -1
		elif(self.prot.rect.bottom>620):
			return 1
		return 0
	
	def pageLeftOrRight(self):
		''' Horizontal: return the rect.left value of where the mermaid should
			end up IF difficulty changes. Difficulty changes are
			tracked in the Game Engine now.
		'''
		if(self.prot.rect.left<10):
			return (900 - self.prot.rect.width - 10)
		if(self.prot.rect.right>890):
			return 20
		return self.prot.rect.left
	
	def atPageBorder(self):
		''' Horizontal: return -1 if protagonist collides with left border 
						return 1 if protagonist collides with right border
						0 if no collision. 1 and -1 evaluate to Boolean TRUE
		'''
		if (self.prot.rect.left<10):
			return -1
		if (self.prot.rect.right>890): 
			return 1
		return 0
		
	def move_protagonist(self, (left,top)):
		self.prot.rect.left = left
		self.prot.rect.top = top
		
	def move_prot_by_border_checks(self, diff, page):
		''' Called from outside, this function will use
			Difficulty and Page background changes ONLY if
			the outside agent determines to change them by (DIFF, PAGE):Bools
		'''
		if(diff):
			self.prot.rect.top = self.diffUpOrDown()
		if(page):
			self.prot.rect.left = self.pageLeftOrRight()
		if(page or diff): 
			print "Changed!"
			
		
	####END NEW BORDER CHECKING CODE
	
	def update_page_before_changing(self, page):
		page.clear_enemies()
		enemies = dict()
		for evil in self.evil:
			if(not enemies.has_key(evil.type)):
				enemies[evil.type] = 0
			enemies[evil.type] += 1
		
		# set the num of items
		page.set_enemies(enemies.items())
		# set the amount health reups
		page.set_num_items(len(self.items))
		
	def set_assets(self, page):
		self.evil.empty()
		for enemy in page.enemies:
			num, type_ = enemy
			self.add_evils(num, type_)
			
		# Now finally set the health items	
		self.set_items(page.num_items)	
		
	def add_evils( self, num_enemies, type_enemies):
		'''add in type differences'''
		for x in range(0,num_enemies):
			self.add_evil(type_enemies)
			
	def add_evil(self, type_enemies):
		if(type_enemies=='df'):
			self.evil.add(Enemy(self.propsfiles[1], self, type='df'))
		elif(type_enemies=='dm'):
			self.evil.add(Enemy(self.propsfiles[2], self, type='dm'))
		
	def set_items(self, item_num):
		if not self.items:
			self.items = pygame.sprite.Group()
		self.items.empty()
		for x in range(item_num):
			self.items.add(Item())
			
	def check_use_items(self):
		if self.items:
			for item in pygame.sprite.spritecollide(self.prot,self.items,dokill=False):
				if self.prot.increaseHealth(item.get_value()):
					item.kill()
				
	def evil_helper(self, spriteA, spriteB):
		spriteA.joinWith(spriteB, None)
		
	def damageMermaid(self, damage):
		self.prot.decreaseHealth(damage)
	
	def checkDodgeStatus(self):
		#return true if dodging
		return self.prot.isDodging()

	def checkPositionStatus(self, enemypos):
		#return true if out of range
		loreleipos = self.prot.get_position()
		xrange = [(enemypos[0]-200),enemypos[0]]
		yrange = [(enemypos[1]-100),enemypos[1]+100]
		if(loreleipos[0]>=xrange[0] and loreleipos[0]<=xrange[1]):
			if(loreleipos[1]>=yrange[0] and loreleipos[1]<=yrange[1]):
				return 0
		return 1
		
	def resetGame(self):
		self.prot.increaseHealth(90)

