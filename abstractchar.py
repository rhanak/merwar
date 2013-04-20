import pygame

class AbstractCharacter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.subscribers = []

	def addListener(self, subscriber):
		self.subscribers.append(subscriber)

	def delListener(self, subscriber):
		# TODO
		print "del"
		
	def notify(self, event):
		for subscriber in self.subscribers:
			 subscriber.event(event)