
from settings import *
from menus.base_menu import BaseMenu

class Pause(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.title = 'Paused'
		self.element_list = ['Continue','Audio','Controls','Quit to Menu']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.key_button_prompts = self.get_key_button_prompts(['Confirm','Back'])
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.alpha = 0

	def next_scene(self):
		
		if ACTIONS['Confirm'] and self.selection == 'Quit to Menu':
			self.scene.paused = not self.scene.paused
			self.scene.transition.on_complete = [self.scene.next_scene]
			for action in ACTIONS:
				ACTIONS[action] = 0

		elif ACTIONS['Confirm'] and self.selection == 'Audio':
			from menus.options import Audio
			self.scene.menu = Audio(self.game, self.scene)
			for action in ACTIONS:
				ACTIONS[action] = 0

		elif ACTIONS['Confirm'] and self.selection == 'Controls':
			if self.game.input.joystick:
				from menus.bind_controller import BindController
				self.scene.menu = BindController(self.game, self.scene)
			else:
				from menus.bind_keyboard import BindKeyboard
				self.scene.menu = BindKeyboard(self.game, self.scene)
				
			for action in ACTIONS:
				ACTIONS[action] = 0

		elif ACTIONS['Confirm'] or ACTIONS['Pause'] or ACTIONS['Back']:
			self.scene.paused = not self.scene.paused
			ACTIONS['Pause'] = 0
			ACTIONS['Confirm'] = 0
			ACTIONS['Back'] = 0


		



