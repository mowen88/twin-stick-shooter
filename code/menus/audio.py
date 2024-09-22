from settings import *
from entities import Entity, AnimatedEntity
from menus.base_menu import BaseMenu 
from menus.options import Options
from menus.pause import Pause

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
		if ACTIONS['Confirm']:
			if self.selection == 'Back':
				if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = Options(self.game, self.scene)

			self.reset_actions()

		elif ACTIONS['Back']:
			self.scene.menu = Options(self.game, self.scene)
			self.reset_actions()