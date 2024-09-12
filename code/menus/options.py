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
		self.transition = Fade(self.game, [self.update_sprites, self.drawn_sprites], 1000)

	def next_scene(self):
		if self.selection in ['Audio','Controls','Back']:
			self.prev_state.transition.alpha = 255
			for cursor in self.prev_state.cursors:
				cursor.frame_index = 0
			self.exit_state()
		# else:
		# 	# if quit
		# 	self.game.quit()


			

