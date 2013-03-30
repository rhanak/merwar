#coded by Tanya Presnetsova

import os, pygame, json, random, csv
from pygame.locals import *
from utils import *
from modes import ModeManager, GameMode, SimpleMode

kDataDir = 'data'
kGlobals = 'globals.json'

class Fighter (pygame.sprite.Sprite)
	def __init__(self, props):
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
		
	def _update_image( self, frame_index ):
		self.image = self.sprite_sheet.subsurface( self.frames[ frame_index ] )
		self.frame_index = frame_index
		
	def update( self):
		self._update_image( ( self.frame_index + 1 ) % len( self.frames ) )
		
	def attack(self, key)
	
		
class ProtagonistMermaid( pygame.sprite.Sprite ):
	def __init__( self, props ):
	
	def update(self)
	
	def attack(self)
	
	def defend(self)

class DarkFemaleMermaid(pygame.sprite.Sprite):
	def __init__(self):
		
	def update(self):
			
	def trackProtagonist(self):

	def dazed(self):
		
	def attack(self):
	
	def defend(self):

class DarkMaleMermaid(pygame.sprite.Sprite):
	def __init__(self):
		
	def update(self):
			
	def trackProtagonist(self):

	def dazed(self):
		
	def attack(self):
	
	def defend(self):