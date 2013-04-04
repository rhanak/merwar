import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *

class Mermaid( pygame.sprite.Sprite ):
	def __init__( self, props, enemies, manager ):
		pygame.sprite.Sprite.__init__( self )
		self.properties = props
		self.sprite_sheet, sheet_rect = load_image_alpha( props['sprite sheet'] )
		self.frames = extract_frames_from_spritesheet( sheet_rect, int( props['sprite width'] ), int( props['sprite height'] ), int( props['num frames'] ) )
		self.velocity = [0.0,0.0]
		self.stabbing = 0
		#Dale Added These
		self.angle = 0
		self.inited = False
		self.max_speed = 10.0
		self.decay = 1.0
		self.accel = 2.0;
		#end adds
		self._update_image( 0 )
		self.rect = self.image.get_rect()
		self.rect.top = int( props['start y'] )
		self.rect.left = int( props['start x'] )
		self.inited = True
		self.enemyManager = manager
		self.enemies = enemies
		self.changeDifficulties = 0

	def _update_image( self, frame_index ):
		self.image = self.sprite_sheet.subsurface( self.frames[ frame_index ] )
		self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
		if self.inited: self.rect = self.image.get_rect(center=self.rect.center)
		self.frame_index = frame_index

	def update( self):
		self._update_image( ( self.frame_index + 1 ) % len( self.frames ) )
		global difficulty
		#move mermaid to mouse position
		mouse_position= pygame.mouse.get_pos()
		'''
		velocity changes
		'''
		pressed = pygame.key.get_pressed()
		if pressed[ K_RIGHT ]:
			self.angle += math.pi * 3 / 180
		if pressed[ K_LEFT ]:
			self.angle -= math.pi * 3 / 180 #may need to tweak these two turning rates ^
		if pressed[ K_DOWN ]:
			self.velocity[0] -= self.accel * math.cos(self.angle)
			self.velocity[1] -= self.accel * math.sin(self.angle)
		if pressed[ K_UP ]:
			self.velocity[0] += self.accel * math.cos(self.angle)
			self.velocity[1] += self.accel * math.sin(self.angle)
		self.clampvelocity()
		newpos = self.rect.move(self.velocity)
		self.clampx(newpos, 0, 900)
		self.rect= newpos
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
		elif(self.rect.top<30 and difficulty=="hard"):
			self.rect.bottom = 590
			self.rect.left = 100
			difficulty = "normal"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		elif(self.rect.bottom>600 and difficulty=="normal"):
			self.rect.top = 40
			self.rect.left = 100
			difficulty = "hard"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		elif(self.rect.bottom>600 and difficulty=="easy"):
			self.rect.top = 40
			self.rect.left = 100
			difficulty = "normal"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		self.clampy(self.rect, 0, 630)
		
		#self.rect.midtop= mouse_position	
		
		return self.changeDifficulties
		
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
