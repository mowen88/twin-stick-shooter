from settings import *
from transitions import Fade
from entities import Entity, AnimatedEntity
from menus.menu import MainMenu

class OptionsMenu(MainMenu):
	def __init__(self, game):
		super().__init__(game)

		self.title = 'Options'
		self.element_list = ['Audio','Controls','Back']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()
		self.transition = Fade(self.game, [self.update_sprites, self.drawn_sprites], 2000)

	def next_scene(self):
		if self.selection in ['Audio','Controls']:
			#from menus.options import Options
			#self.game.stack.pop()
			#MainMenu(self.game).enter_state()
			#self.prev_state.transition.alpha = 255
			self.exit_state()
		else:
			# if quit
			self.game.quit()

	def update(self, dt):
		self.navigate()
		self.navigation_timer.update(dt)
		self.update_sprites.update(dt)

			

