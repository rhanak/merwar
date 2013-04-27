import os, pygame, sys
from utils import *

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
			if event.type == QUIT:
				sys.exit("Quit.") 
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit("Quit.")
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