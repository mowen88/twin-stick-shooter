from settings import *
from entities import Entity, AnimatedEntity
from menus.main_menu import MainMenu
from menus.base_menu import BaseMenu 
from menus.pause import Pause

class Options(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.title = 'OPTIONS'
		self.element_list = ['Audio', 'Controls', 'Back']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.button_prompts = self.get_button_prompts(['Confirm','Back'])
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.alpha = 0

	def next_scene(self):
		if ACTIONS['Confirm']:
			if self.selection == 'Back':
				if hasattr(self.scene, 'paused'):
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = MainMenu(self.game, self.scene)

			elif self.selection == 'Audio':
				from menus.audio import Audio
				self.scene.menu = Audio(self.game, self.scene)

			elif self.selection == 'Controls':
				if self.game.input.joystick:
					from menus.bind_controller import BindController
					self.scene.menu = BindController(self.game, self.scene)
				else:
					from menus.bind_keyboard import BindKeyboard
					self.scene.menu = BindKeyboard(self.game, self.scene)

			self.reset_actions()

		elif ACTIONS['Back']:
			if hasattr(self.scene, 'paused'):
				self.scene.menu = Pause(self.game, self.scene)
			else:
				self.scene.menu = MainMenu(self.game, self.scene)
			self.reset_actions()


class Credits(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.title = 'CREDITS'
		self.element_list = ['']
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.cursor = self.get_mouse_cursor('menu_cursor')

	def next_scene(self):
		if ACTIONS['Confirm']:
			self.scene.menu = MainMenu(self.game, self.scene)
			self.reset_actions()




			

