import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *
from abstractchar import AbstractCharacter

class Mermaid( AbstractCharacter ):
	def __init__( self, props):
		AbstractCharacter.__init__( self )
		self.properties = props
		self.sprite_sheet, sheet_rect = load_image_alpha( props['sprite sheet'] )
		self.frames = extract_frames_from_spritesheet( sheet_rect, int( props['sprite width'] ), int( props['sprite height'] ), int( props['num frames'] ) )
		self.velocity = [0,0]
		self.stabbing = 0
		#Dale Added These
		self.angle = 0
		self.inited = False
		self.max_speed = 15
		self.decay = 3;
		#end adds
		self._update_image( 0 )
		self.rect = self.image.get_rect()
		self.rect.top = int( props['start y'] )
		self.rect.left = int( props['start x'] )
		self.inited = True
		self.changeDifficulties = 0
		self.health = 100
		self.dead = 0

	def _update_image( self, frame_index ):
		self.image = self.sprite_sheet.subsurface( self.frames[ frame_index ] )
		self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
		if self.inited: self.rect = self.image.get_rect(center=self.rect.center)
		self.frame_index = frame_index

	def update( self):
		self._update_image( ( self.frame_index + 1 ) % len( self.frames ) )
		
		def sign( x ):
			if x < 0: return -1
			elif x > 0: return 1
			return 0
		
		ms = self.max_speed
		pressed = pygame.key.get_pressed()
		vel = self.velocity
		if not (pressed[ K_RIGHT ] or pressed[ K_LEFT ]
				or pressed[ K_DOWN ] or pressed[ K_UP ]):
				self.velocity[0] -= sign(vel[0])*self.decay
				self.velocity[1] -= sign(vel[1])*self.decay
		else:
			x_amt = y_amt = 0 
			if pressed[ K_RIGHT ]:
				x_amt += ms
			if pressed[ K_LEFT ]:
				x_amt -= ms
			if pressed[ K_DOWN ]:
				y_amt += ms
			if pressed[ K_UP ]:
				y_amt -= ms
			self.velocity = [x_amt, y_amt]
		
		self.angle = math.atan2(self.velocity[1], self.velocity[0])
		newpos = self.rect.move(self.velocity)
		self.clampx(newpos, 0, 900)
		
		self.clampy(newpos, 0, 630)
		
		self.rect = newpos

		
	def stab(self, target):
		if not self.stabbing:
			self.stabbing = 1
			deathbox = self.rect.inflate(-5,-5)
			return deathbox.colliderect(target.rect)
			
	def unstab(self):
		self.stabbing = 0
		
	def clampvelocity(self):
		'''
		Scale the velocity to be max in the correct direction, if it has exceeded
		'''
		vel = self.velocity
		angle = math.atan2(vel[1], vel[0])
		max = [self.max_speed*math.cos(angle), self.max_speed*math.sin(angle)]
		
		def magnitude(l_vector):
			return math.hypot(l_vector[0], l_vector[1])
			
		if magnitude(self.velocity)>magnitude(max):
			self.velocity = max
			
	def clampx(self, pos, left, right):
		if pos.left < left:
			pos.left = left
		elif pos.right > right:
			pos.right = right
	
	def clampy(self, pos, top, bottom):
		if pos.top < top:
			pos.top = top
		elif pos.bottom > bottom:
			pos.bottom = bottom

	def get_position(self):
		return self.rect.center

	def isDodging(self):
		return 0

	def decreaseHealth(self, attackPower):
		self.health-=attackPower
		if(self.health<=0):
			self.dead = 1
		self.notify(("health", "decreased", attackPower))
		
	def increaseHealth(self):
		self.health+=10
		if(self.health>100):
			self.health = 100
		self.notify(("health", "increased", 10))
