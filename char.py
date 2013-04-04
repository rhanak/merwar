#coded by Tanya Presnetsova

import os, pygame, json, random, csv, thread
from pygame.locals import *
from utils import *
from modes import ModeManager, GameMode, SimpleMode

kDataDir = 'data'
kGlobals = 'globals.json'

class CharacterManager():
	def __init__( self, protagonist, evils):
		self.prot = protagonist
		self.evil = evils
		
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
		self.evil.update()
		return self.prot.update()
		
	def set_evils( self, evils):
		self.evil = evils
				
	def evil_helper(self, spriteA, spriteB):
		spriteA.joinWith(spriteB, None)

class Fighter ( pygame.sprite.Sprite ):
	def __init__( self, props ):
		pygame.sprite.Sprite.__init__( self )
		self.properties = props
		self.sprite_sheet, sheet_rect = load_image_alpha( props['sprite sheet'] )
		self.frames = extract_frames_from_spritesheet( sheet_rect, int( props['sprite width'] ), int( props['sprite height'] ), int( props['num frames'] ) )
		self.stabbing = 0
		self._update_image( 0 )
		self.rect = self.image.get_rect()
		self.rect.top = int( props['start y'] )
		self.rect.left = int( props['start x'] )
		
	def _update_image( self, frame_index ):
		self.image = self.sprite_sheet.subsurface( self.frames[ frame_index ] )
		self.frame_index = frame_index
		
	def update( self):
		self._update_image( ( self.frame_index + 1 ) % len( self.frames ) )
		
	def attack(self, key):
		pass
		
class ProtagonistMermaid( Fighter ):
	def __init__( self, props ):
		Fighter.__init__( self, props)
		self.speed = [0,0]
	
	def update(self):
		Fighter.update(self)
		pressed = pygame.key.get_pressed()
		if pressed[ K_RIGHT ]:
			self.angle += math.pi * 3 / 180
		if pressed[ K_LEFT ]:
			self.angle -= math.pi * 3 / 180 #may need to tweak these two turning rates ^
		if pressed[ K_DOWN ]:
			self.speed[0] -= self.accel * math.cos(self.angle)
			self.speed[1] -= self.accel * math.sin(self.angle)
		if pressed[ K_UP ]:
			self.speed[0] += self.accel * math.cos(self.angle)
			self.speed[1] += self.accel * math.sin(self.angle)
	
	def attack(self):
		pass
	def defend(self):
		pass
class DarkFemaleMermaid( Fighter ):
	def __init__(self):
		pass
	def update(self):
		pass
	def trackProtagonist(self):
		pass
	def dazed(self):
		pass		
	def attack(self):
		pass
	def defend(self):
		pass
class DarkMaleMermaid( Fighter ):
	def __init__(self):
		pass
	def update(self):
		pass
	def trackProtagonist(self):
		pass
	def dazed(self):
		pass
	def attack(self):
		pass
	def defend(self):
		pass
