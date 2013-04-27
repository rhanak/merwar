import pygame
class Shark(AbstractCharacter):
	def __init__(self):
		AbstractCharacter.__init__(self)
		self.image, self.rect= load_image('shark.png')
		self.image = pygame.transform.flip(self.image,1,0)
		screen= pygame.display.get_surface()
		self.velocity = [8,1]
		self.area= screen.get_rect()
		self.rect.topleft = random.randrange(30,840), random.randrange(30,570)
		self.move = self.velocity
		self.dizzy = 0
		
	def update(self, position):
		if self.dizzy:
			self._spin_()
		else:
			self._walk_()
			
	def _walk_(self):
		newpos = self.rect.move(self.velocity)
		if (self.rect.left<self.area.left or self.rect.right>self.area.right):
			self.velocity[0]=-self.velocity[0]
			self.velocity[1]=self.velocity[1]*random.randrange(1,3)
			newpos=self.rect.move(self.velocity)
			
			# TODO Make the shark flip without actually flipping too many times
			
			#self.image = pygame.transform.flip(self.image,1,0)
		if self.rect.top<self.area.top:
			self.velocity[1]=2
			newpos=self.rect.move(self.velocity)
		elif self.rect.bottom>self.area.bottom:
			self.velocity[1]=-2
			newpos=self.rect.move(self.velocity)
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
		
	def joinWith(self, other, dims):
		new_speed = other.velocity
		
		# TODO need to actual make the sharks join together and follow each other
		
		#if new_speed[0] * self.velocity[0] < 0:
			#self.image = pygame.transform.flip(self.image,1,0)
		
		
	def stabbed(self):
		if not self.dizzy:
			self.dizzy=1
			self.original= self.image;