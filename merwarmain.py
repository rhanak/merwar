#coded by Dale Gartman, Randy Hanak, Tanya Presnetsova
#cs325 spring 2012

import os, pygame, json, random, csv, sys
from pygame.locals import *
if not pygame.mixer: print 'Warning: sound disabled'
from utils import *
from modes import ModeManager, GameMode, SimpleMode
from characters import *
'''from char import *'''
from gameengine import *

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

def main():
	pygame.init()
	screen = pygame.display.set_mode((900,630))
	pygame.display.set_caption('MerWar')

	select_screen(screen)

	game_engine = GameEngine(screen)
	background = game_engine.get_opening_screen()
	screen.blit(background,(0,0))
	pygame.display.flip()

	clock = pygame.time.Clock()
	whiff_sound = load_sound('bubbles.wav')
	stab_sound = load_sound('bubbleshit.wav')

	while 1:
		clock.tick(15)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit("Quit.") 
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit("Quit.") 
			elif event.type == MOUSEBUTTONDOWN:
				whiff_sound.play()
			#elif event.type is MOUSEBUTTONUP:
			#	mermaid.unstab()
				
		game_engine.update()
		pygame.display.flip()

if __name__== '__main__': main()
      


