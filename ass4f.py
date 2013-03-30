#coded by Tanya Presnetsova, Assignment 2, due 2/13/13 @10pm

import os, pygame, json, random, csv
from pygame.locals import *
if not pygame.mixer: print 'Warning: sound disabled'
from utils import *
from modes import ModeManager, GameMode, SimpleMode

kDataDir = 'data'
kGlobals = 'globals.json'
'''screen = pygame.display.set_mode((900,630))
background = pygame.image.load(path_rejoin('data/underthesea.png')).convert()'''
difficulty = "normal"

def load_image(name):
	'''given a filename, returns a pygame.Surface'''
	filename= os.path.join('data', name)
	try:
		image= pygame.image.load(filename)
	except pygame.error, message:
		print 'Cannot noad image:', filename
		raise SystemExit, message
	image= image.convert_alpha()
	return image, image.get_rect()

def load_sound(name):
	class NoneSound:
		def play(self):pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	filename= os.path.join('data',name)
	try:
		sound= pygame.mixer.Sound(filename)
	except pygame.error, message:
		print 'Cannot load sound:', fullname
		raise SystemExit, message
	return sound
	
def path_rejoin(path):
	return os.path.join(*path.split('/'))

class Mermaid( pygame.sprite.Sprite ):
	def __init__( self, props, enemies, manager ):
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
		self.enemyManager = manager
		self.enemies = enemies
		self.changeDifficulties = 0

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
		self.changeDifficulties = 0
		if(self.rect.top<30 and difficulty=="normal"):
			self.rect.bottom = 590
			self.rect.left = 100
			difficulty = "easy"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		if(self.rect.top<30 and difficulty=="hard"):
			self.rect.bottom = 590
			self.rect.left = 100
			difficulty = "normal"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		if(self.rect.bottom>600 and difficulty=="normal"):
			self.rect.top = 40
			self.rect.left = 100
			difficulty = "hard"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		if(self.rect.bottom>600 and difficulty=="easy"):
			self.rect.top = 40
			self.rect.left = 100
			difficulty = "normal"
			self = Mermaid(self.properties,self.enemies,self.enemyManager)
			self.changeDifficulties = 1
		#self.rect.midtop= mouse_position	
		self.rect= newpos
		return self.changeDifficulties
		
	def stab(self, target):
		if not self.stabbing:
			self.stabbing = 1
			deathbox = self.rect.inflate(-5,-5)
			return deathbox.colliderect(target.rect)
			
	def unstab(self):
		self.stabbing = 0

class SharkManager():
	def __init__(self):
		self.numSharks = 3
		
	def returnSharks(self):
		global difficulty
		if(difficulty=="easy"):
			self.numSharks = 1
		if(difficulty=="normal"):
			self.numSharks = 3
		if(difficulty=="hard"):
			self.numSharks = 6
			
		sharks = []
		for i in range(self.numSharks):
			sharks.append(Shark())
		return sharks
		
class Shark(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect= load_image('shark.png')
		self.image = pygame.transform.flip(self.image,1,0)
		screen= pygame.display.get_surface()
		self.speed = [8,1]
		self.area= screen.get_rect()
		self.rect.topleft = random.randrange(30,840), random.randrange(30,570)
		self.move = self.speed
		self.dizzy = 0
		
	def update(self):
		if self.dizzy:
			self._spin_()
		else:
			self._walk_()
			
	def _walk_(self):
		newpos = self.rect.move(self.speed)
		if (self.rect.left<self.area.left or self.rect.right>self.area.right):
			self.speed[0]=-self.speed[0]
			self.speed[1]=self.speed[1]*random.randrange(1,3)
			newpos=self.rect.move(self.speed)
			self.image = pygame.transform.flip(self.image,1,0)
		if self.rect.top<self.area.top:
			self.speed[1]=2
			newpos=self.rect.move(self.speed)
		elif self.rect.bottom>self.area.bottom:
			self.speed[1]=-2
			newpos=self.rect.move(self.speed)
		self.rect = newpos

	def _spin_(self):
		center= self.rect.center
		self.dizzy= self.dizzy+30
		if self.dizzy >= 360:
			self.dizzy = 0
			self.image = self.original
		else:
			rotate = pygame.transform.rotate
			self.image = rotate(self.original, self.dizzy)
		self.rect = self.image.get_rect(center=center)
		
	def stabbed(self):
		if not self.dizzy:
			self.dizzy=1
			self.original= self.image;
		
def main():
	pygame.init()
	screen = pygame.display.set_mode((900,630))
	pygame.display.set_caption('Shark Tag')
	pygame.mouse.set_visible(0)
	
	unselected = 1
	splashScreen = pygame.image.load(path_rejoin('data/select_screen.png')).convert()
	quit_rect = pygame.Rect( 25, 100, 140, 160 )
	start_rect = pygame.Rect( 25, 25, 145, 90 )
	mouse_down_pos = (-1,-1)
	pygame.mouse.set_visible( 1 )
	
	while unselected:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				mouse_down_pos = event.pos
			elif event.type is MOUSEBUTTONUP:
				def collides_down_and_up( r ):
					return r.collidepoint( mouse_down_pos ) and r.collidepoint( event.pos )
				if collides_down_and_up( quit_rect ):
					print 'quitting'
					return   
				if collides_down_and_up( start_rect ):
					print 'play!'
					unselected = 0
					break
		screen.blit(splashScreen, (0,0))
		pygame.display.flip()
	
	
	'''background = pygame.image.load(path_rejoin('data/underthesea.png')).convert()'''
	backgroundEasy = pygame.image.load(path_rejoin('data/undertheseaeasy.png')).convert()
	backgroundNormal = pygame.image.load(path_rejoin('data/underthesea.png')).convert()
	backgroundHard = pygame.image.load(path_rejoin('data/undertheseahard.png')).convert()
	screen.blit(backgroundNormal,(0,0))
	pygame.display.flip()
	
	clock = pygame.time.Clock()
	whiff_sound = load_sound('bubbles.wav')
	stab_sound = load_sound('bubbleshit.wav')
	sharkManager = SharkManager()
	sharkgroup = pygame.sprite.Group( sharkManager.returnSharks() )
	for character in csv.DictReader( open( os.path.join( kDataDir, 'maze_characters.csv' ) ) ):
		mermaid = Mermaid(character, sharkgroup, sharkManager)
	mermaidg = pygame.sprite.Group( ( mermaid ) )
	
	while 1:
		clock.tick(15)
		pygame.mouse.set_visible( 0 )
		
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			elif event.type == MOUSEBUTTONDOWN:
				killed = pygame.sprite.spritecollide(mermaid, sharkgroup, True )
				if len( killed ) > 0:
					stab_sound.play()
				else:
					whiff_sound.play()
			elif event.type is MOUSEBUTTONUP:
				mermaid.unstab()
				
		changeInDifficulty=mermaid.update()
		if (changeInDifficulty):
			sharkgroup.empty()
			sharkgroup = pygame.sprite.Group( sharkManager.returnSharks() )
		sharkgroup.update()
		
		if(difficulty=="easy"):
			screen.blit(backgroundEasy, (0,0))
		elif(difficulty=="normal"):
			screen.blit(backgroundNormal, (0,0))
		elif(difficulty=="hard"):
			screen.blit(backgroundHard, (0,0))
		sharkgroup.draw(screen)
		mermaidg.draw(screen)
		pygame.display.flip()
		
if __name__== '__main__': main()
			















