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
from selectscreen import *

kDataDir = 'data'
kGlobals = 'globals.json'

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

	while 1:
		clock.tick(15)
				
		game_engine.update()
		pygame.display.flip()

if __name__== '__main__': main()
      


