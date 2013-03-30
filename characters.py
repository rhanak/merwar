import os, pygame, json, random, csv
from pygame.locals import *
from utils import *

difficulty = "normal"

class SharkManager():
  def __init__(self):
    self.numSharks = 3

  def returnSharks(self):
    global difficulty
    if(difficulty=="easy"):
      self.numSharks = 1
    if(difficulty=="normal"):
      self.numSharks = 3
    if(difficulty=="hard"):
      self.numSharks = 6

    sharks = []
    for i in range(self.numSharks):
      sharks.append(Shark())
    return sharks

class Mermaid( pygame.sprite.Sprite ):
	def __init__( self, props, enemies, manager ):
		pygame.sprite.Sprite.__init__( self )
		self.properties = props
		self.sprite_sheet, sheet_rect = load_image_alpha( props['sprite sheet'] )
		self.frames = extract_frames_from_spritesheet( sheet_rect, int( props['sprite width'] ), int( props['sprite height'] ), int( props['num frames'] ) )
		self.speed = [0,0]
		self.stabbing = 0
		self._update_image( 0 )
		self.rect = self.image.get_rect()
		self.rect.top = int( props['start y'] )
		self.rect.left = int( props['start x'] )
		self.enemyManager = manager
		self.enemies = enemies
		self.changeDifficulties = 0

	def _update_image( self, frame_index ):
		self.image = self.sprite_sheet.subsurface( self.frames[ frame_index ] )
		self.frame_index = frame_index

	def update( self):
		self._update_image( ( self.frame_index + 1 ) % len( self.frames ) )
		global difficulty
		#move mermaid to mouse position
		mouse_position= pygame.mouse.get_pos()
		'''
		speed changes
		'''
		if(self.rect.left>mouse_position[0]):
			self.speed[0]=-4
			newpos=self.rect.move(self.speed)
		elif(self.rect.right<mouse_position[0]):
			self.speed[0]=4
			newpos=self.rect.move(self.speed)
		else:
			self.speed[0]=0
			newpos=self.rect.move(self.speed)
		if(self.rect.top>mouse_position[1]):
			self.speed[1]=-4
			newpos=self.rect.move(self.speed)
		elif(self.rect.bottom<mouse_position[1]):
			self.speed[1]=4
			newpos=self.rect.move(self.speed)
		else:
			self.speed[1]=0
			newpos=self.rect.move(self.speed)
		'''
		difficulty changes
		'''
		self.changeDifficulties = 0
		if(self.rect.top<30 and difficulty=="normal"):
			self.rect.bottom = 590
			self.rect.left = 100
			difficulty = "easy"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		if(self.rect.top<30 and difficulty=="hard"):
			self.rect.bottom = 590
			self.rect.left = 100
			difficulty = "normal"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		if(self.rect.bottom>600 and difficulty=="normal"):
			self.rect.top = 40
			self.rect.left = 100
			difficulty = "hard"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		if(self.rect.bottom>600 and difficulty=="easy"):
			self.rect.top = 40
			self.rect.left = 100
			difficulty = "normal"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		#self.rect.midtop= mouse_position	
		self.rect= newpos
		return self.changeDifficulties
		
	def stab(self, target):
		if not self.stabbing:
			self.stabbing = 1
			deathbox = self.rect.inflate(-5,-5)
			return deathbox.colliderect(target.rect)
			
	def unstab(self):
		self.stabbing = 0
		
class Shark(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect= load_image('shark.png')
		self.image = pygame.transform.flip(self.image,1,0)
		screen= pygame.display.get_surface()
		self.speed = [8,1]
		self.area= screen.get_rect()
		self.rect.topleft = random.randrange(30,840), random.randrange(30,570)
		self.move = self.speed
		self.dizzy = 0
		
	def update(self):
		if self.dizzy:
			self._spin_()
		else:
			self._walk_()
			
	def _walk_(self):
		newpos = self.rect.move(self.speed)
		if (self.rect.left<self.area.left or self.rect.right>self.area.right):
			self.speed[0]=-self.speed[0]
			self.speed[1]=self.speed[1]*random.randrange(1,3)
			newpos=self.rect.move(self.speed)
			self.image = pygame.transform.flip(self.image,1,0)
		if self.rect.top<self.area.top:
			self.speed[1]=2
			newpos=self.rect.move(self.speed)
		elif self.rect.bottom>self.area.bottom:
			self.speed[1]=-2
			newpos=self.rect.move(self.speed)
		self.rect = newpos

	def _spin_(self):
		center= self.rect.center
		self.dizzy= self.dizzy+30
		if self.dizzy >= 360:
			self.dizzy = 0
			self.image = self.original
		else:
			rotate = pygame.transform.rotate
			self.image = rotate(self.original, self.dizzy)
		self.rect = self.image.get_rect(center=center)
		
	def stabbed(self):
		if not self.dizzy:
			self.dizzy=1
			self.original= self.image;