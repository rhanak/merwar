import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *
import threading

difficulty = "normal"

class SharkManager():
  def __init__(self):
    self.numSharks = 3
    self.sharks = None
    self.difficulty = difficulty
    def collided(x): x.speed[0] = 0
    
    self.b = BadGuyCollider(collided)
    self.b.setGroup(self.sharkGroup())
    self.b.daemon = True
    self.b.start()

  def sharkGroup(self):
    global difficulty
    if(difficulty=="easy"):
      self.numSharks = 1
    if(difficulty=="normal"):
      self.numSharks = 3
    if(difficulty=="hard"):
      self.numSharks = 6
    
    if(self.sharks is None or self.difficulty != difficulty):
      self.sharks = pygame.sprite.Group()
      for i in range(self.numSharks):
       self.sharks.add(Shark())
      self.b.setGroup(self.sharks)
    return self.sharks 
  
class BadGuyCollider(threading.Thread):
  def __init__(self, collided):
    threading.Thread.__init__(self)
    self.collided = collided
  
  def setGroup(self, group):
    self.group = group.copy()
  
  def run(self):
    while True:
      sprites = self.group.sprites()
      for sprite in sprites:
        self.group.remove(sprite)
        sprite_hit_list = pygame.sprite.spritecollide(sprite, self.group, False)
        
        # Check the list of colliding sprites, and add one to the score for each one
        for sprite_collided in sprite_hit_list:
          self.collided(sprite_collided)
            
        # Add the sprite back so we can test for it again next go round
        self.group.add(sprite)       
                    
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
		
	def update(self):
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