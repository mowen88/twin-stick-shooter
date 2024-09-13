from settings import *
from entities import Entity, AnimatedEntity
from menus.base_menu import BaseMenu

class MainMenu(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.menu_sprites.empty()
		self.started = False
		self.title = 'Main Menu'
		self.element_list = ['Start Game','Options','Quit']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()
		self.alpha = 0

	def next_scene(self):
		if ACTIONS['OK']:
			if self.selection == 'Start Game':
				self.scene.transition.on_complete = [self.scene.next_scene]
				self.started = True
			elif self.selection == 'Options':
				from menus.options import Options
				self.scene.menu = Options(self.game, self.scene)
			else:
				self.game.quit()
			# ACTIONS['OK'] = 0
			# ACTIONS['Pause'] = 0
			for action in ACTIONS:
				ACTIONS[action] = 0
