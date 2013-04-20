import pygame

class AbstractCharacter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		subscribers = []

	def addListener(subscriber):
		subscribers.append(subscriber)

	def delListener():
		# TODO
		print "del"
		
	def notify(event):
		for subscriber in subscribers:
			 subscriber(event)