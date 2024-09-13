from settings import *
from entities import Entity, AnimatedEntity
from menus.main_menu import MainMenu
from menus.base_menu import BaseMenu

class Options(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.title = 'Options'
		self.element_list = ['Audio', 'Controls', 'Back']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()
		self.alpha = 0

	def next_scene(self):
		if ACTIONS['OK']:
			if self.selection == 'Back':
				if hasattr(self.scene, 'paused'):
					from menus.pause import Pause
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = MainMenu(self.game, self.scene)

			elif self.selection == 'Audio':
				self.scene.menu = Audio(self.game, self.scene)

			elif self.selection == 'Controls':
				self.scene.menu = Controls(self.game, self.scene)

			for action in ACTIONS:
				ACTIONS[action] = 0

class Audio(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.title = 'Controls'
		self.element_list = ['Music Volume', 'Sound Volume', 'Master Volume', 'Back']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()
		self.alpha = 0

	def next_scene(self):
		if ACTIONS['OK']:
			if self.selection == 'Back':
				if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
					from menus.pause import Pause
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = Options(self.game, self.scene)

			for action in ACTIONS:
				ACTIONS[action] = 0

class Controls(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.title = 'Controls'
		self.element_list = ['Controller', 'Keyboard', 'Back']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()
		self.alpha = 0

	def next_scene(self):
		if ACTIONS['OK']:
			if self.selection == 'Back':
				if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
					from menus.pause import Pause
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = Options(self.game, self.scene)

			for action in ACTIONS:
				ACTIONS[action] = 0



			

