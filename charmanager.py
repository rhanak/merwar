import os, pygame, json, random, csv, math
from pygame.locals import *
from characters import *
from mermaid import *
from utils import *
from health import *

kDataDir = 'data'
kGlobals = 'globals.json'

class CharManager():
	def __init__( self ):
		self.propsfiles = []
		for character in csv.DictReader( open( os.path.join( kDataDir, 'characters.csv' ) ) ):
			self.propsfiles.append(character)
		mermaid = Mermaid(self.propsfiles[0])
		dfm = Enemy(self.propsfiles[1], self)
		
		self.prot = mermaid
		self.evil = pygame.sprite.RenderPlain(dfm)
		self.items = 0
		self.protg = pygame.sprite.GroupSingle( self.prot )
		
		self.health_setup()
	
	def health_setup(self):
		health_protagonist = HealthBar()
		self.prot.addListener(health_protagonist)
		self.healthbars = pygame.sprite.RenderPlain((HealthContainer(health_protagonist)))
		
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
		self.healthbars.update()
		#return self.difficulty()
		
	def draw( self, screen ):
		self.protg.draw( screen )
		self.evil.draw( screen )
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
		
	def set_evils( self, num_enemies, type_enemies):
		self.evil.empty()
		'''add in type differences'''
		for x in range(0,num_enemies):
			if(type_enemies=='df'):
				self.evil.add(Enemy(self.propsfiles[1], self))
			elif(type_enemies=='dm'):
				self.evil.add(Enemy(self.propsfiles[2], self))
		
	def set_items(self, item_num):
		self.items = createNewItems(item_num)
				
	def evil_helper(self, spriteA, spriteB):
		spriteA.joinWith(spriteB, None)
		
	def damageMermaid(self, damage):
		self.prot.decreaseHealth(damage)
		print 'lalala'
	
	def checkDodgeStatus(self):
		#return true if dodging
		return self.prot.isDodging()

	def checkPositionStatus(self, enemypos):
		#return true if out of range
		loreleipos = self.prot.get_position()
		xrange = [(enemypos[0]-200),enemypos[0]]
		yrange = [(enemypos[1]-100),enemypos[1]+100]
		if(loreleipos[0]>=xrange[0] and poreleipos[0]<=xrange[1]):
			if(loreleipos[1]>=yrange[0] and poreleipos[1]<=yrange[1]):
				return 0
		return 1
