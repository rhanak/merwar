#coded by Dale Gartman, Randy Hanak, Tanya Presnetsova
#cs325 spring 2012

import os, pygame, json, random, csv, sys
from pygame.locals import *
if not pygame.mixer: print 'Warning: sound disabled'
from utils import *
from modes import ModeManager, GameMode, SimpleMode
from characters import *
'''from char import *'''
from pages import *

kDataDir = 'data'
kGlobals = 'globals.json'

def select_screen(screen):
	unselected=1
	splashScreen = pygame.image.load(path_rejoin('data/select_screen.png')).convert()
	quit_rect = pygame.Rect( 25, 100, 140, 160 )
	start_rect = pygame.Rect( 25, 25, 145, 90 )
	mouse_down_pos = (-1,-1)
	pygame.mouse.set_visible( 1 )
	screen.blit(splashScreen, (0,0))
	pygame.display.flip()

	while unselected:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				mouse_down_pos = event.pos
			elif event.type is MOUSEBUTTONUP:
				def collides_down_and_up( r ):
					return r.collidepoint( mouse_down_pos ) and r.collidepoint( event.pos )
				if collides_down_and_up( quit_rect ):
					sys.exit("Quit.") 
				if collides_down_and_up( start_rect ):
					print "Play!"
					unselected = 0
					break
	screen.blit(splashScreen, (0,0))
	pygame.mouse.set_visible( 0 )
	pygame.display.flip()

class Mermaid( pygame.sprite.Sprite ):
	def __init__( self, props, page_manager):
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
		self.changeDifficulties = 0
		self.page_manager = page_manager

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
		if(self.rect.top<30):
			self.page_manager.change_difficulty(0)
			self.rect.bottom = 590
			self.rect.left = 100
			self = Mermaid(self.properties,self.page_manager)
		if(self.rect.bottom>600):
			self.page_manager.change_difficulty(1)
			self.rect.top = 40
			self.rect.left = 100
			self = Mermaid(self.properties,self.page_manager)
		if(self.rect.right>870):
			self.page_manager.change_difficulty(1)
			self.rect.top = 300
			self.rect.left = 40
			self = Mermaid(self.properties,self.page_manager)
		self.rect= newpos
		return self.changeDifficulties
		
	def stab(self, target):
		if not self.stabbing:
			self.stabbing = 1
			deathbox = self.rect.inflate(-5,-5)
			return deathbox.colliderect(target.rect)
			
	def unstab(self):
		self.stabbing = 0	
	
def main():
	pygame.init()
	screen = pygame.display.set_mode((900,630))
	pygame.display.set_caption('MerWar')

	select_screen(screen)

	page_manager = PageManager(screen)
	backgrounds = page_manager.load_backgrounds()
	screen.blit(backgrounds[1],(0,0))
	pygame.display.flip()

	clock = pygame.time.Clock()
	whiff_sound = load_sound('bubbles.wav')
	stab_sound = load_sound('bubbleshit.wav')

	for character in csv.DictReader( open( os.path.join( kDataDir, 'maze_characters.csv' ) ) ):
		mermaid = Mermaid(character,page_manager)
	mermaidg = pygame.sprite.Group( ( mermaid ) )

	while 1:
		clock.tick(15)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit("Quit.") 
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit("Quit.") 
			elif event.type == MOUSEBUTTONDOWN:
				whiff_sound.play()
			elif event.type is MOUSEBUTTONUP:
				mermaid.unstab()
				
		page_manager.update()
		mermaid.update()
		mermaidg.draw(screen)
		pygame.display.flip()

if __name__== '__main__': main()
      


