import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *
from abstractchar import AbstractCharacter
from combostate import *

class Enemy( AbstractCharacter ):
	def __init__( self, props, charmanager, type="df" ):
		AbstractCharacter.__init__( self )
		self.manager = charmanager
		self.properties = props
		self.sprite_sheet, sheet_rect = load_image_alpha( props['sprite sheet'] )
		width, height = int(props['sprite width']), int(props['sprite height'])
		num_frames = int( props['num frames'] )
		###BEGIN CLUNKY IF STATEMENTS CHECKING ENEMY TYPE###
		if type == "df":
			combo_map = [("pullback", "dfpullback.png", (width-1, height-1, 2)),\
							("attack", "dfattack.png",(width-1, height-1, 3))]
		elif type == "dm":
			combo_map = [("pullback", "dmpullback.png", (width, height, 2)),\
							("attack", "dmattack.png", (width, height, 4))]
		else:
			combo_map = None
		###END CLUNKY IF STATEMENTS###
		self.combo_state = ComboMachine( (props['sprite sheet'], (width, height, num_frames)),\
					combo_map)
		#self.frames = extract_frames_from_spritesheet( sheet_rect, int( props['sprite width'] ), int( props['sprite height'] ), int( props['num frames'] ) )
		self.attackPower = int( props['attack power'] )
		self.defenseBoost = int( props['defense boost'] )
		self.stabbing = 0
		self.maxVelocity = int( props['velocity'] )
		self.velocity = [0.0,0.0]
		self._update_image( random.randrange(self.combo_state.get_num_frames()) )
		self.rect = self.image.get_rect()
		self.rect.topleft = random.randrange(700,840), random.randrange(400,570)
		self.maxBefore = int( props['max before'] )
		self.maxBetween = int( props['max between'] )
		self.health = 100
		
		#Mode 0 is 'tracking mode' in which the enemy attempts to close the distance between itself and Lerelei
		#Mode 1 is 'combat mode' in which the enemy maintains distance from Lorelei attempts to attack her
		self.mode = 0
		self.recovering = 1
		self.recoverytimer = random.randrange(0,self.maxBefore)
		self.preparedToAttack = 0
		self.continueAttack = True
		# This changes when the health of this Enemy goes down to nothing
		# They then float up the screen and "kill()" themself off screen
		self.dying = False
		
	def _update_image( self, frame_index=-1 ):
		#print "Frame is %d" % frame_index
		#print "and length in %d" % len(self.frames)
		self.image = self.combo_state.get_cur_frame(frame_index)
		
	def _update_health(self):
		self.image.fill((0,0,0), pygame.Rect(50,0, 100, 10))
		self.image.fill((255,255,255), pygame.Rect(50,0, self.health, 10))
		
		if(self.health < 1):
			self.i_am_dead()
		
	def update( self, pos):
		
		if(self.dying):
			self.dying_update()
		else:
			self.combo_state.combo_check_and_update()
			self._update_image()
			
			if(not self.recovering):
				if(not self.mode):
					self.track(pos)
				else:
					self.combat(pos)
			else:
				self.recoverytimer += 1
			
				if(self.recoverytimer>random.randrange(self.maxBetween-10,self.maxBetween)):
					self.recovering = 0
					self.recoverytimer = 0
					self.preparedToAttack = 0
		
			# Finally update the health
			self._update_health()
			
			
	def i_am_dead(self):
		self.image = pygame.transform.flip(self.image, 0, 1)
		self.dying = True
	
	def dying_update(self):
		self.rect.move_ip(0, -5)
		
		# Once the enemy moves off screen remove it from all groups
		if(self.rect.y < 0):
			self.kill()
	
	def faceProtagonist(self):
		self.image = pygame.transform.flip(self.image, 1, 0)
		
	def track(self,pos):
		oldVelocity = self.velocity[0]
		maxVelocity, negVelocity = self.maxVelocity, (-1*self.maxVelocity)
		if(abs(self.rect.center[0]-pos[0])<200 and abs(self.rect.center[1]-pos[1])<100):
			self.mode = 1
		elif(abs(self.rect.center[0]-pos[0])<200):
			if(self.rect.center[1]>pos[1]):
				self.velocity[1]=negVelocity
			elif(abs(self.rect.center[1])<pos[1]):
				self.velocity[1]=maxVelocity
		elif(abs(self.rect.center[1]-pos[1])<100):
			if(self.rect.center[0]>pos[0]):
				self.velocity[0]=negVelocity
			elif(self.rect.center[0]<pos[0]):
				self.velocity[0]=maxVelocity
		else:
			if(self.rect.center[0]>pos[0]):
				self.velocity[0]=negVelocity
			elif(self.rect.center[0]<pos[0]):
				self.velocity[0]=maxVelocity
			if(self.rect.center[1]>pos[1]):
				self.velocity[1]=negVelocity
				
			elif(self.rect.center[1]<pos[1]):
				self.velocity[1]=maxVelocity
				
		if(self.velocity[0] == maxVelocity):
			self.faceProtagonist()
		elif(oldVelocity > self.velocity[0]):
			self.faceProtagonist()
		newpos = self.rect.move(self.velocity)
		self.rect = newpos
		
	def combat(self,pos):
		if(abs(self.rect.center[0]-pos[0])>200 or abs(self.rect.center[1]-pos[1])>100):
			self.mode = 0
		self.velocity = [0.0,0.0]
		if(self.preparedToAttack==0):
			self.prepareToAttack()
		if(self.preparedToAttack>10):
			self.attack()
			self.preparedToAttack = 0
		else:
			self.preparedToAttack += 1
			if self.manager.checkDodgeStatus():
				self.continueAttack = False
				
	def damageEnemy(self, attackPower):
		self.health -= attackPower
		
	def prepareToAttack(self):
		self.combo_state.enter_combo_str("pullback")
		pull_back = load_sound('enemypullback.wav')
		pull_back.play()
		#animate pull back
	
	def attack(self):
		miss = load_sound('bubbles.wav')
		hit = load_sound('bubbleshit.wav')
		self.combo_state.enter_combo_str("attack")
		if self.manager.checkPositionStatus(self.rect.center):
			self.continueAttack = False
			self.combo_state.interrupt()
		if(self.continueAttack):
			#animate attack
			#print "attackPower %d" % self.attackPower
			self.manager.damageMermaid(self.attackPower)
			# Just testing damaging the enemy, REMOVE THIS
			#self.damageEnemy(self.attackPower)
			hit.play()
		else:
			self.combo_state.interrupt()
			miss.play()
		self.recovering = 1
		self.continueAttack = True
		
	def joinWith(self, other, dims):
		blah = 0
