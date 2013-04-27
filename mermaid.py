import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *
from abstractchar import AbstractCharacter
from combostate import *

COMBO_BTNS = {K_LALT:"/", K_LCTRL:"^", K_SPACE:"_"}

class Mermaid( AbstractCharacter ):
	def __init__( self, props ):
		AbstractCharacter.__init__( self )
		self.properties = props
	
		#combo_map stores combo states. pass it a combo string with values from
		#the COMBO_BTNS strings above. You can add more control keys/string equivs
		#to the dictionary (COMBO_BTNS) if you like. Make sure the strings are one char long.
		
		#Recommend combo_map be loaded from a CSV file at some point.
		combo_map = [("^^^", "darkfemalemermaid.png", (180,180,4)),\
			("^^/^", "darkfemalemermaid.png", (180,180,4)),\
			("^_^", "darkfemalemermaid.png", (180,180,4))]
		self.combo_state = ComboMachine(( props['sprite sheet'], (int(props['sprite width']),\
			int( props['sprite height']), int( props['num frames'])) ), combo_map ) 
		self.velocity = [0,0]
		self.stabbing = 0
		#Dale Added These
		self.angle = 0
		self.inited = False
		self.max_speed = 15
		self.decay = 3;
		#end adds
		self._update_image()
		self.rect = self.image.get_rect()
		self.rect.top = int( props['start y'] )
		self.rect.left = int( props['start x'] )
		self.inited = True
		self.changeDifficulties = 0
		self.health = 100
		self.dead = 0
		#tempvars
		self.dodgeStatus = False

	def _update_image( self ):
		self.image = self.combo_state.get_cur_frame()
		self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
		if self.inited: self.rect = self.image.get_rect(center=self.rect.center)
		#self.frame_index = frame_index

	def update( self):
		
		combo_str = ""
		
		ignore_flag = False	
		push_exit = None
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				push_exit = event
			if ignore_flag: continue
			if event.type == KEYUP:
				if event.key in COMBO_BTNS.keys():
					ignore_flag = True
					combo_str+=COMBO_BTNS[event.key]
		if push_exit: pygame.event.post(push_exit)
		
		self.combo_state.combo_check_and_update(combo_str)
			
		def sign( x ):
			if x < 0: return -1
			elif x > 0: return 1
			return 0
		
		
		ms = self.max_speed
		pressed = pygame.key.get_pressed()
		vel = self.velocity
		## TODO mermaid stays facing left once she looks left until right is pressed
		if not (pressed[ K_RIGHT ] or pressed[ K_LEFT ]
				or pressed[ K_DOWN ] or pressed[ K_UP ]):
				self.velocity[0] -= sign(vel[0])*self.decay
				self.velocity[1] -= sign(vel[1])*self.decay
				if abs(self.velocity[0])<self.decay: self.velocity[0]=0
				if abs(self.velocity[1])<self.decay: self.velocity[1]=0
		else:
			self.combo_state.interrupt()
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
					
			
		if (pressed[ K_RSHIFT ] or pressed[ K_LSHIFT ]):
			self.dodgeStatus = True
		else:
			self.dodgeStatus = False
		
		self.angle = math.atan2(self.velocity[1], self.velocity[0])
		newpos = self.rect.move(self.velocity)
		self.clampx(newpos, 0, 900)
		
		self.clampy(newpos, 0, 630)
		
		self.rect = newpos
		self._update_image( ) #( self.frame_index + 1 ) % len( self.frames )#
		
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
		return self.dodgeStatus

	def decreaseHealth(self, attackPower):
		if not self.dodgeStatus:
			self.combo_state.interrupt()
			self.health-=attackPower
			if(self.health<=0):
				self.dead = 1
			self.notify(("health", "decreased", attackPower))
		
	def increaseHealth(self, value):
		self.health+=value
		if(self.health>100):
			self.health = 100
		self.notify(("health", "increased", value))
