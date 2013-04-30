import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *
from abstractchar import AbstractCharacter

class Enemy( AbstractCharacter ):
	def __init__( self, props, charmanager ):
		AbstractCharacter.__init__( self )
		self.manager = charmanager
		self.properties = props
		self.sprite_sheet, sheet_rect = load_image_alpha( props['sprite sheet'] )
		self.frames = extract_frames_from_spritesheet( sheet_rect, int( props['sprite width'] ), int( props['sprite height'] ), int( props['num frames'] ) )
		self.attackPower = int( props['attack power'] )
		self.defenseBoost = int( props['defense boost'] )
		self.stabbing = 0
		self.maxVelocity = int( props['velocity'] )
		self.velocity = [0.0,0.0]
		self._update_image( random.randrange(len(self.frames)))
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
		
	def _update_image( self, frame_index ):
		#print "Frame is %d" % frame_index
		#print "and length in %d" % len(self.frames)
		self.image = self.sprite_sheet.subsurface( self.frames[ frame_index ] )
		self.frame_index = frame_index
		
	def _update_health(self):
		self.image.fill((0,0,0), pygame.Rect(50,0, 100, 10))
		self.image.fill((255,255,255), pygame.Rect(50,0, self.health, 10))
		
		if(self.health < 1):
			self.kill()
		
	def update( self, pos):
		self._update_image( ( self.frame_index + 1 ) % len( self.frames ) )
		
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
		pull_back = load_sound('enemypullback.wav')
		pull_back.play()
		#animate pull back
	
	def attack(self):
		miss = load_sound('bubbles.wav')
		hit = load_sound('bubbleshit.wav')
		if self.manager.checkPositionStatus(self.rect.center):
			self.continueAttack = False
		if(self.continueAttack):
			#animate attack
			#print "attackPower %d" % self.attackPower
			self.manager.damageMermaid(self.attackPower)
			# Just testing damaging the enemy, REMOVE THIS
			#self.damageEnemy(self.attackPower)
			hit.play()
		else:
			#animate attack
			miss.play()
		self.recovering = 1
		self.continueAttack = True
		
	def joinWith(self, other, dims):
		blah = 0
