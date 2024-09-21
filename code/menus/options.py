from settings import *
from entities import Entity, AnimatedEntity
from menus.main_menu import MainMenu
from menus.base_menu import BaseMenu 
from menus.pause import Pause

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
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.alpha = 0

	def next_scene(self):
		if ACTIONS['OK']:
			if self.selection == 'Back':
				if hasattr(self.scene, 'paused'):
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = MainMenu(self.game, self.scene)

			elif self.selection == 'Audio':
				self.scene.menu = Audio(self.game, self.scene)

			elif self.selection == 'Controls':
				if self.game.input.joystick:
					from menus.bind_controller import BindController
					self.scene.menu = BindController(self.game, self.scene)
				else:
					from menus.bind_keyboard import BindKeyboard
					self.scene.menu = BindKeyboard(self.game, self.scene)

			for action in ACTIONS:
				ACTIONS[action] = 0

		elif ACTIONS['Back']:
			if hasattr(self.scene, 'paused'):
				self.scene.menu = Pause(self.game, self.scene)
			else:
				self.scene.menu = MainMenu(self.game, self.scene)
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
		self.elements = self.get_elements('midleft',180)
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
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

		elif ACTIONS['Back']:
			self.scene.menu = Options(self.game, self.scene)
			for action in ACTIONS:
				ACTIONS[action] = 0



			

