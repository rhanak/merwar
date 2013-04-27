import sys, os, pygame, json, random, csv, math, threading
from pygame.locals import *
from utils import *
from mermaid import *
from charmanager import *
from characters import *
from dalesutils import *
from selectscreen import *

class GameConditions():
		def __init__( self, screen, eventThreading, resetGame ):
			self.eventNumber = 0
			self.screen = screen
			self.eventThreading = eventThreading
			self.resetGame = resetGame
			
		def update(self):
			if(self.eventThreading.is_set()):
				print self.eventNumber
				if(self.eventNumber == 0):
					# Event is fired the first time and it shows the game over screen, another event will be fired to show the game menu
					s = pygame.Surface((self.screen.get_width(), self.screen.get_height()) )
					self.screen.blit(s, (0,0))
					display_text(self.screen, "GAME OVER!!!!", self.screen.get_width()/2, self.screen.get_height()/2)
					self.eventNumber = 1
					self.eventThreading.clear()
				else:
					# Event is fired a second time after so many seconds to show the game menu
					select_screen(self.screen)
					self.eventNumber = 0
					self.eventThreading.clear()

					# Need to actually rest the game
					self.resetGame()
			
		def isNormalPlay(self):
			if(self.eventNumber == 0):
				return True
			else:
				return False