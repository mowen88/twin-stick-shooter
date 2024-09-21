from settings import *
from entities import Entity, AnimatedEntity
from menus.options import Options
from menus.base_menu import BaseMenu

class BindController(BaseMenu):
	def __init__(self, game, scene, index=0):
		super().__init__(game, scene)

		self.joystick_name = self.game.input.joystick_name
		self.game.input.bind_mode = False
		self.game.input.new_bind[self.game.input.joystick_name] = -1
		self.instantiate_images = False
		self.title = f'{self.game.input.joystick_name}'
		self.element_list = ['Attack', 'Dash', 'Inventory', 'Pause', 'Back']
		self.index = index
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements('midleft',220)
		self.bindings = self.get_bindings('midright')
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.alpha = 0
		
	def get_bindings(self, alignment='center'):

		elements = []
		offset = 0
	
		start_y = TILESIZE * 4
		line_spacing = TILESIZE

		for option in self.element_list:
			if option != 'Back':
				offset += line_spacing
				for action, button_id in BUTTON_MAPS[self.joystick_name].items():
					if action == option:
						name = BUTTON_NAMES[self.joystick_name][button_id]

						surface = self.game.font.render(name, False, COLOURS['white'])
						pos = self.panel_element.rect.right - TILESIZE * 1.5, start_y + offset
						element = Entity([self.menu_sprites], pos, surface, 3, alignment)
						elements.append(element)

		return elements

	def bind_mode(self):
	    if self.game.input.bind_mode:
	        if self.instantiate_images:
	            pos = (self.panel_element.rect.centerx, self.bindings[self.index].rect.centery)
	            size = (self.panel_element.rect.width, 12)
	            message = f'Press a key for {self.element_list[self.index]}'
	            blank = Entity([self.menu_sprites], pos, pygame.Surface(size), 5)
	            blank.image.fill(COLOURS['cyan'])
	            text = Entity([self.menu_sprites], pos, self.game.font.render(message, False, COLOURS['black']), 5)
	            self.instantiate_images = False

	        if self.game.input.new_bind[self.joystick_name] != -1: # must be -1 as 0 is used for a button id, unlike the keys
	            new_button = self.game.input.new_bind[self.joystick_name]
	            current_action = self.selection
	            print(new_button)
	            
	            for action, button_id in BUTTON_MAPS[self.joystick_name].items(): # check for duplicates
	                if button_id == new_button and action != current_action and action not in ['OK','Back']:
	                    BUTTON_MAPS[self.joystick_name][action] = BUTTON_MAPS[self.joystick_name][current_action]
	                    break

	            BUTTON_MAPS[self.joystick_name][current_action] = new_button # assign new button to action

	            self.reset_actions()

	            self.scene.menu = BindController(self.game, self.scene, self.index)

	def next_scene(self):
		self.bind_mode()

		if ACTIONS['OK'] and not self.game.input.bind_mode:
			if self.selection == 'Back':
				if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
					from menus.pause import Pause
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = Options(self.game, self.scene)
					
			elif self.game.input.joystick:
				self.game.input.bind_mode = True
				self.instantiate_images = True

			self.reset_actions()

		elif ACTIONS['Back'] and not self.game.input.bind_mode or not self.game.input.joystick:
			if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
				from menus.pause import Pause
				self.scene.menu = Pause(self.game, self.scene)
			else:
				self.scene.menu = Options(self.game, self.scene)

			self.reset_actions()
