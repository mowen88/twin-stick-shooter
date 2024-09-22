from settings import *
from entities import Entity, AnimatedEntity
from menus.base_menu import BaseMenu

class MainMenu(BaseMenu):
	def __init__(self, game, scene):
		super().__init__(game, scene)

		self.menu_sprites.empty()
		self.title = 'Main Menu'
		self.element_list = ['Start Game','Options', 'Credits','Quit']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.key_button_prompts = self.get_key_button_prompts(['Confirm'])
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.alpha = 0

	def next_scene(self):
		if ACTIONS['Confirm']:
			if self.selection == 'Start Game':
				self.scene.transition.on_complete = [self.scene.next_scene]
			elif self.selection == 'Options':
				from menus.options import Options
				self.scene.menu = Options(self.game, self.scene)
			elif self.selection == 'Credits':
				from menus.options import Credits
				self.scene.menu = Credits(self.game, self.scene)
			else:
				self.game.quit()
			# ACTIONS['Confirm'] = 0
			# ACTIONS['Pause'] = 0
			self.reset_actions()


