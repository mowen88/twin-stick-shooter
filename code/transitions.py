import pygame
from settings import *

class Fade(pygame.sprite.Sprite):
	def __init__(self, game, groups, speed, colour=COLOURS['white'], surf=pygame.Surface((RES)), z=5):
		super().__init__(groups)

		self.game = game
		self.z = z
		self.fade_speed = speed
		self.image = surf
		self.image.fill(colour)
		self.rect = self.image.get_rect(topleft=(0,0))
		self.alpha = 255
		self.on_complete = None
		self.transitioning = False

	def update(self, dt):

		self.game.block_input = True if self.alpha > 0 else False
		self.transitioning = True if self.on_complete is not None else False

		if self.transitioning:
			self.alpha += self.fade_speed * dt
			if self.alpha >= 255: 
				[func() for func in self.on_complete]	
				self.on_complete = None
				self.transitioning = False
		else:
			self.alpha -= self.fade_speed * dt
			if self.alpha <= 0:
				self.alpha = 0
				
		self.image.set_alpha(self.alpha)


class CirclesTransition(Fade):
	def __init__(self, game, colour=COLOURS['red']):
		super().__init__(game)

		self.game = game
		self.surface = pygame.Surface(RES)
		self.margin = 8
		self.cols = int(WIDTH/self.margin)
		self.rows = int(HEIGHT/self.margin)
		self.counter = 16
		self.limit = self.counter
		self.fade_speed = 60#20
		self.on_complete = None
		self.transitioning = False

	def draw_shapes(self, screen):
		for x in range(self.rows):
			for y in range(self.cols):
				pos_x = y * self.margin * 2
				pos_y = x * self.margin * 2
				pygame.draw.circle(screen, COLOURS['black'], (pos_x, pos_y), int(self.counter))

	def draw(self, screen):
		self.draw_shapes(screen)