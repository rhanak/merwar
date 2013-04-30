import sys, os, pygame, json, random, csv, math, threading, time
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
			self.gameWon = False
			self.gameWonTimer = None
			
		def update(self):
			# OOh did you lose? :(
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
			# Have we won the Game		
			elif(self.gameWon):
					#print "now you are cool"
					s = pygame.Surface((self.screen.get_width(), self.screen.get_height()) )
					s.fill((255,255,255))
					self.screen.blit(s, (0,0))
					display_text(self.screen, "YOU WON!!!!", self.screen.get_width()/2, self.screen.get_height()/2)
					if(not self.gameWonTimer):
						self.gameWonTimer = time.time()
					
					# timer expires you know you have won ;)
					if((time.time() - self.gameWonTimer) > 2):
						# Ok you are finishing winning now ...
						self.gameWon = False
						self.gameWonTimer = None
						# Display the main menu
						select_screen(self.screen)

						# Need to actually rest the game
						self.resetGame()
					
		def win(self):
			self.gameWon = True
		
		def isNormalPlay(self):
			if(self.eventNumber == 0 and not self.gameWon):
				return True
			else:
				return False