from settings import *
from entities import Entity, AnimatedEntity
from menus.options import Options
from menus.base_menu import BaseMenu

class BindController(BaseMenu):
	def __init__(self, game, scene, index=0):
		super().__init__(game, scene)

		self.game.input.bind_mode = False
		self.game.input.new_bind[self.game.input.joystick_name] = -1
		self.instantiate_images = False
		self.title_string = self.game.input.joystick_name.replace("Wireless", "").strip().replace("Switch", "").strip().upper()
		self.title = self.title_string
		self.start_y = TILESIZE * 2.5
		self.element_list = ['Attack','Shoot','Dash','Inventory','Pause','Back']
		self.index = index
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements('midleft',218, WIDTH * 0.3)
		self.bindings = self.get_bindings('midright')
		self.button_prompts = self.get_button_prompts(['Reset Defaults','Confirm','Back'])
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.left_stick_animation = AnimatedEntity([self.menu_sprites], (WIDTH*0.25, HEIGHT*0.8), f'../assets/menu_animations/left_stick', 4, z=6)
		self.d_pad_animation = AnimatedEntity([self.menu_sprites], (WIDTH*0.35, HEIGHT*0.8), f'../assets/menu_animations/d-pad', 4, z=6)
		self.right_stick_animation = AnimatedEntity([self.menu_sprites], (WIDTH*0.8, HEIGHT*0.4), f'../assets/menu_animations/right_stick', 4, z=6)
		self.move_message = Entity([self.menu_sprites], (WIDTH*0.3, HEIGHT*0.95), self.game.font.render('Left stick or D-pad to move', False, COLOURS['white']), 6)
		self.right_stick_message = Entity([self.menu_sprites], (WIDTH*0.8, HEIGHT*0.55), self.game.font.render('Right stick to aim', False, COLOURS['white']), 6)
		self.alpha = 0
		
	def get_bindings(self, alignment='center'):

		offset = 0
		for option in self.element_list:
			if option != 'Back':
				offset += self.line_spacing
				for action, button_id in BUTTON_MAPS[self.game.input.joystick_name].items():
					if action == option:
						name = BUTTON_NAMES[self.game.input.joystick_name][button_id]
						surface = pygame.image.load(f'../assets/controller_button_icons/{self.game.input.joystick_name}/{name}.png').convert_alpha()
						#surface = self.game.font.render(name, False, COLOURS['white'])
						pos = self.panel_element.rect.right - TILESIZE * 1.5, self.start_y + offset
						element = Entity([self.menu_sprites], pos, surface, 3, alignment)


	def bind_mode(self):
	    if self.game.input.bind_mode:
	        if self.instantiate_images:
	            pos = (self.panel_element.rect.centerx, self.elements[self.index].rect.centery)
	            size = (self.panel_element.rect.width, 15)
	            message = f'Press a button for {self.element_list[self.index]}'
	            blank = Entity([self.menu_sprites], pos, pygame.Surface(size), 5)
	            blank.image.fill(COLOURS['cyan'])
	            text = Entity([self.menu_sprites], pos, self.game.font.render(message, False, COLOURS['black']), 5)
	            self.instantiate_images = False

	        if self.game.input.new_bind[self.game.input.joystick_name] != -1: # must be -1 as 0 is used for a button id, unlike the keys
	            if self.game.input.new_bind[self.game.input.joystick_name] not in [11,12,13,14]:
	            	new_button = self.game.input.new_bind[self.game.input.joystick_name]
	            	current_action = self.selection

	            	for action, button_id in BUTTON_MAPS[self.game.input.joystick_name].items(): # check for duplicate
	            		if button_id == new_button and action != current_action and action in self.element_list:
	            			BUTTON_MAPS[self.game.input.joystick_name][action] = BUTTON_MAPS[self.game.input.joystick_name][current_action]
	            			break

	            	BUTTON_MAPS[self.game.input.joystick_name][current_action] = new_button # assign new button to action
	            	self.scene.menu = BindController(self.game, self.scene, self.index)
	            	self.reset_actions()

	def reset_defaults(self):
		BUTTON_MAPS[self.game.input.joystick_name].update(DEFAULT_BUTTON_MAPS[self.game.input.joystick_name])
		self.scene.menu = BindController(self.game, self.scene, self.index)

	def next_scene(self):
		self.bind_mode()

		if ACTIONS['Confirm'] and not self.game.input.bind_mode:
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

		elif ACTIONS['Back'] and not self.game.input.bind_mode:
			if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
				from menus.pause import Pause
				self.scene.menu = Pause(self.game, self.scene)
			else:
				self.scene.menu = Options(self.game, self.scene)

			self.reset_actions()

		elif not self.game.input.joystick:
			from menus.bind_keyboard import BindKeyboard
			self.scene.menu = BindKeyboard(self.game, self.scene, self.index)

		elif ACTIONS['Reset Defaults']:
			self.reset_defaults()
			self.reset_actions()

