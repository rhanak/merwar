import pygame 

def display_text(screen, text, x, y, size = 20):
	''' Display the passed text at the coordinates (x,y) in 
		a sufficiently visible font '''
	font_obj = pygame.font.SysFont("arial", size, bold=True)
	disp_text = font_obj.render(text, 1, (249, 35, 7))
	screen.blit(disp_text, (x,y))