import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *

class Shark(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect= load_image('shark.png')
		self.image = pygame.transform.flip(self.image,1,0)
		screen= pygame.display.get_surface()
		self.velocity = [8,1]
		self.area= screen.get_rect()
		self.rect.topleft = random.randrange(30,840), random.randrange(30,570)
		self.move = self.velocity
		self.dizzy = 0
		
	def update(self, position):
		if self.dizzy:
			self._spin_()
		else:
			self._walk_()
			
	def _walk_(self):
		newpos = self.rect.move(self.velocity)
		if (self.rect.left<self.area.left or self.rect.right>self.area.right):
			self.velocity[0]=-self.velocity[0]
			self.velocity[1]=self.velocity[1]*random.randrange(1,3)
			newpos=self.rect.move(self.velocity)
			self.image = pygame.transform.flip(self.image,1,0)
		if self.rect.top<self.area.top:
			self.velocity[1]=2
			newpos=self.rect.move(self.velocity)
		elif self.rect.bottom>self.area.bottom:
			self.velocity[1]=-2
			newpos=self.rect.move(self.velocity)
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
		
	def joinWith(self, other, dims):
		new_speed = other.velocity
		if new_speed[0] * self.velocity[0] < 0:
			self.image = pygame.transform.flip(self.image,1,0)
		
		
	def stabbed(self):
		if not self.dizzy:
			self.dizzy=1
			self.original= self.image;

class Enemy( pygame.sprite.Sprite ):
	def __init__( self, props ):
		pygame.sprite.Sprite.__init__( self )
		self.properties = props
		self.sprite_sheet, sheet_rect = load_image_alpha( props['sprite sheet'] )
		self.frames = extract_frames_from_spritesheet( sheet_rect, int( props['sprite width'] ), int( props['sprite height'] ), int( props['num frames'] ) )
		self.stabbing = 0
		self.velocity = [0.0,0.0]
		self._update_image( 0 )
		self.rect = self.image.get_rect()
		self.rect.top = int( props['start y'] )
		self.rect.left = int( props['start x'] )
		#Mode 0 is 'tracking mode' in which the enemy attempts to close the distance between itself and Lerelei
		#Mode 1 is 'combat mode' in which the enemy maintains distance from Lorelei attempts to attack her
		self.mode = 0
		
	def _update_image( self, frame_index ):
		self.image = self.sprite_sheet.subsurface( self.frames[ frame_index ] )
		self.frame_index = frame_index
		
	def update( self, pos):
		self._update_image( ( self.frame_index + 1 ) % len( self.frames ) )
		if(not self.mode):
			self.track(pos)
		else:
			self.combat(pos)
	
	def track(self,pos):
		if(abs(self.rect.center[0]-pos[0])<200 and abs(self.rect.center[1]-pos[1])<100):
			self.mode = 1
		elif(abs(self.rect.center[0]-pos[0])<200):
			if(self.rect.center[1]>pos[1]):
				self.velocity[1]=-2
			elif(abs(self.rect.center[1])<pos[1]):
				self.velocity[1]=2
		elif(abs(self.rect.center[1]-pos[1])<100):
			if(self.rect.center[0]>pos[0]):
				self.velocity[0]=-2
			elif(self.rect.center[0]<pos[0]):
				self.velocity[0]=2
		else:
			if(self.rect.center[0]>pos[0]):
				self.velocity[0]=-2
			elif(self.rect.center[0]<pos[0]):
				self.velocity[0]=2
			if(self.rect.center[1]>pos[1]):
				self.velocity[1]=-2
			elif(self.rect.center[1]<pos[1]):
				self.velocity[1]=2
		newpos = self.rect.move(self.velocity)
		self.rect = newpos
		
	def combat(self,pos):
		if(abs(self.rect.center[0]-pos[0])>200 or abs(self.rect.center[1]-pos[1])>100):
			self.mode = 0
		self.velocity = [0.0,0.0]
		
	def joinWith(self, other, dims):
		blah = 0