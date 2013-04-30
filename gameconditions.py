import sys, os, pygame, json, random, csv, math, threading, time
from pygame.locals import *
from utils import *
from mermaid import *
from charmanager import *
from characters import *
from dalesutils import *
from selectscreen import *

class GameConditions():
		def __init__( self, screen, eventThreading, resetGame, times ):
			self.eventNumber = 0
			self.screen = screen
			self.eventThreading = eventThreading
			self.resetGame = resetGame
			self.gameWon = False
			self.gameWonTimer = None
			self.times = times
			
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
					background = pygame.image.load(path_rejoin('data/splash_screen.png')).convert()
					s.blit(background, (0,0))
					self.screen.blit(s, (0,0))
					display_rage_text(self.screen, "Time spent Easy: %d seconds" % (self.times[0]/1000), self.screen.get_width()/2 - 20, self.screen.get_height()/2 - 240)
					display_rage_text(self.screen, "Time spent Medium: %d seconds" % (self.times[1]/1000), self.screen.get_width()/2 - 20, self.screen.get_height()/2 - 210)
					display_rage_text(self.screen, "Time spent Hard: %d seconds" % (self.times[2]/1000), self.screen.get_width()/2 - 20, self.screen.get_height()/2 - 180)
					
					# Just weighted addition of scores in the different levels
					score = self.times[0] * .1 + self.times[1] * .3 + self.times[2] * .6
					
					display_rage_text(self.screen, "New Score: %d" % score, self.screen.get_width()/2 - 20, self.screen.get_height()/2 - 50)
					#display_rage_text(self.screen, "YOU WON!!!!", self.screen.get_width()/2 - 20, self.screen.get_height()/2)
					if(not self.gameWonTimer):
						self.gameWonTimer = time.time()
					
					# timer expires you know you have won ;)
					if((time.time() - self.gameWonTimer) > 10):
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