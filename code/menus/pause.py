
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
		self.cursors = self.get_cursors()
		self.alpha = 0

	def next_scene(self):
		
		if ACTIONS['OK'] and self.selection == 'Quit to Menu':
			self.scene.paused = not self.scene.paused
			self.scene.transition.on_complete = [self.scene.next_scene]
			for action in ACTIONS:
				ACTIONS[action] = 0

		elif ACTIONS['OK'] and self.selection == 'Audio':
			from menus.options import Audio
			self.scene.menu = Audio(self.game, self.scene)
			for action in ACTIONS:
				ACTIONS[action] = 0

		elif ACTIONS['OK'] and self.selection == 'Controls':
			from menus.options import Controls
			self.scene.menu = Controls(self.game, self.scene)
			for action in ACTIONS:
				ACTIONS[action] = 0

		elif ACTIONS['OK'] or ACTIONS['Pause'] or ACTIONS['Back']:
			self.scene.paused = not self.scene.paused
			ACTIONS['Pause'] = 0
			ACTIONS['OK'] = 0
			ACTIONS['Back'] = 0


		



