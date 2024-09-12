import pygame
from settings import *
from entities import Entity

class State():
	def __init__(self, game):
		self.game = game
		self.prev_state = None
		self.update_sprites = pygame.sprite.Group()
		self.drawn_sprites = pygame.sprite.LayeredUpdates()
		self.menu_sprites = pygame.sprite.Group()
		
	def enter_state(self):
		if len(self.game.stack) > 1:
			self.prev_state = self.game.stack[-1]
		self.game.stack.append(self)

	def exit_state(self):
		self.game.stack.pop()

	def debug(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, (255,255,255), self.game.font, (0, 12 * index), 'topleft')

	def update(self, dt):
		pass

	def draw(self,screen):
		pass
