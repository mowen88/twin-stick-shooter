import random
from state import State
from settings import *
from entities import Entity, AnimatedEntity
from transitions import Fade
from timer import Timer
from menus.base_menu import BaseMenu

class Pause(BaseMenu):
	def __init__(self, game):
		super().__init__(game)

		self.title = 'Paused'
		self.element_list = ['Options','Controls','Quit to Menu']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()

	def get_elements(self):

		panel_surface = pygame.image.load('../assets/misc_images/menu_panel.png') 
		panel_element = Entity([self.drawn_sprites], RES/2, panel_surface, z=2)

		title_surface = self.game.font.render(str(self.title), False, COLOURS['white'])
		title_element = Entity([self.drawn_sprites], (WIDTH * 0.5, TILESIZE * 2), title_surface, z=3)

		elements = []
		offset = 0
		start_x = WIDTH * 0.5
		start_y = TILESIZE * 3
		line_spacing = TILESIZE

		for option in self.element_list:
			offset += line_spacing
			surface = self.game.font.render(option, False, COLOURS['cyan'])
			pos = start_x, start_y + offset
			element = Entity([self.drawn_sprites], pos, surface, 'player')
			elements.append(element)
		return elements

	def navigate(self):
		if not self.game.block_input and not self.navigation_timer.running:
			if ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or abs(AXIS_PRESSED['Left Stick'][1]) > 0:
				self.navigation_timer.start()
				for cursor in self.cursors:
					cursor.frame_index = 0

				if ACTIONS['Menu Down'] or AXIS_PRESSED['Left Stick'][1] > 0:
					self.index = (self.index + 1) % len(self.elements)			
				elif ACTIONS['Menu Up'] or AXIS_PRESSED['Left Stick'][1] < 0:
					self.index = (self.index - 1) % len(self.elements)

			if ACTIONS['OK'] and self.selection == 'Options':
				from menus.options import OptionsMenu
				OptionsMenu(self.game).enter_state()

			elif ACTIONS['OK'] and self.selection == 'Quit to Menu':
				self.exit_state()
				self.prev_state.transition.on_complete = [self.prev_state.next_scene]
				ACTIONS['OK'] = 0
				ACTIONS['Pause'] = 0

			elif ACTIONS['Pause']:
				self.prev_state.paused = not self.prev_state.paused
				self.exit_state()
				ACTIONS['Pause'] = 0

				

		self.cursors[0].rect.midright = self.elements[self.index].rect.midleft
		self.cursors[1].rect.midleft = self.elements[self.index].rect.midright
		self.selection = self.element_list[self.index]

	def next_scene(self):
		if self.selection == 'Main Menu':
			self.exit_state()
			self.exit_state()		
		else:
			# if quit
			self.game.quit()

