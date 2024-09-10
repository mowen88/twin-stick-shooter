
from settings import *
from entities import Entity, AnimatedEntity
from transitions import CirclesTransition
from menus.menu import Menu
from menus.bindings import ControllerBindings

class Controllers(Menu):
	def __init__(self, game):
		super().__init__(game)

		self.drawn_sprites.empty()
		self.update_sprites.empty()
		self.bg_colour = COLOURS['green']
		# self.bg_img = pygame.image.load('../assets/misc_images/gradient_bg.png').convert_alpha()
		# self.bg = Entity([self.drawn_sprites], RES/2, self.bg_img)
		self.title = 'Select Controller'
		self.element_list = self.get_controllers()
		self.multi_column = True if len(self.element_list) > self.max_items_per_column else False
		self.elements = self.get_elements()
		self.cursor = AnimatedEntity([self.update_sprites, self.drawn_sprites], self.elements[self.index].rect.midleft, '../assets/particles/menu_cursor_right', 'player')

	def get_controllers(self):
		joysticks = ['Keyboard and Mouse']
		for joy in self.game.input.joysticks:
			joysticks.append(joy.get_name())
		joysticks.append('Refresh')
		return joysticks

	def next_scene(self):

		if self.selection in self.game.input.compatible_joysticks:
			ControllerBindings(self.game, self.selection).enter_state()

		elif self.selection == 'Refresh':
			# reinstantiate the controllers menu and populate list with any newly connected controllers
			self.game.stack.pop()
			Controllers(self.game).enter_state()
		else:
			# if back
			self.exit_state()

