from settings import *
from support import write_data
from entities import Entity, AnimatedEntity
from menus.options import Options
from menus.base_menu import BaseMenu

class BindKeyboard(BaseMenu):
	def __init__(self, game, scene, index=0):
		super().__init__(game, scene)

		self.game.input.bind_mode = False
		self.game.input.new_bind['Keyboard'] = 0
		self.instantiate_images = False
		self.title = 'KEYBOARD AND MOUSE'
		self.start_y = TILESIZE * 2
		self.element_list = ['Up','Down','Left','Right','Jump','Attack','Dash','Inventory','Pause','Reset Defaults','Back']
		self.index = index
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements('midleft',226, WIDTH * 0.3)
		self.bindings = self.get_bindings('midright')
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.mouse_animation = AnimatedEntity([self.menu_sprites], (WIDTH*0.8, HEIGHT*0.4), f'../assets/menu_animations/mouse', 10, z=6)
		self.message = Entity([self.menu_sprites], (WIDTH*0.8, HEIGHT*0.65), self.game.font.render('Move mouse to aim', False, COLOURS['white']), 5)
		self.alpha = 0
		
	def get_bindings(self, alignment='center'):

		offset = 0
	
		line_spacing = TILESIZE

		for option in self.element_list:
			if option not in ['Back','Reset Defaults']:
				offset += self.line_spacing
				for action, key in KEY_MAP.items():
					if action == option:
						name = BUTTON_NAMES['Mouse'][key[0]] if key[0] <= 7 else pygame.key.name(key[0])

						surface = self.game.font.render(name, False, COLOURS['white'])
						pos = self.panel_element.rect.right - TILESIZE * 1.5, self.start_y + offset
						element = Entity([self.menu_sprites], pos, surface, 3, alignment)


	def bind_mode(self):
	    if self.game.input.bind_mode:
	        if self.instantiate_images:
	            self.game.audio.sfx['navigate'].play()
	            pos = (self.panel_element.rect.centerx, self.elements[self.index].rect.centery)
	            size = (self.panel_element.rect.width, 15)
	            message = f'Press a key for {self.element_list[self.index]}'
	            blank = Entity([self.menu_sprites], pos, pygame.Surface(size), 5)
	            blank.image.fill(COLOURS['cyan'])
	            text = Entity([self.menu_sprites], pos, self.game.font.render(message, False, COLOURS['black']), 5)
	            self.instantiate_images = False

	        if self.game.input.new_bind['Keyboard'] != 0:
	            new_key = self.game.input.new_bind['Keyboard']
	            current_action = self.selection
  
	            for action, key in KEY_MAP.items(): # check for duplicates
	                if key[0] == new_key and action not in [current_action, 'Back','Reset Defaults'] and action in self.element_list:
	                    # Swap keys
	                    KEY_MAP[action] = KEY_MAP[current_action]
	                    break

	            KEY_MAP[current_action] = [new_key] # assign new key to the action
	            self.game.audio.sfx['confirm'].play()
	            self.scene.menu = BindKeyboard(self.game, self.scene)
	            self.reset_actions()

	def reset_defaults(self):
	    self.game.audio.sfx['reset'].play()
	    KEY_MAP.update(DEFAULT_KEY_MAP)
	    self.scene.menu = BindKeyboard(self.game, self.scene, self.index)

	def next_scene(self):
		self.bind_mode()

		if ACTIONS['Confirm'] and not self.game.input.bind_mode:
			
			if self.selection == 'Back':
				self.game.audio.sfx['back'].play()
				if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
					from menus.pause import Pause
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = Options(self.game, self.scene)

			elif self.selection == 'Reset Defaults':
				self.reset_defaults()
				self.reset_actions()

			elif not self.game.input.joystick:
				self.game.input.bind_mode = True
				self.instantiate_images = True

			self.reset_actions()

		elif ACTIONS['Back'] and not self.game.input.bind_mode:
			self.game.audio.sfx['back'].play()
			if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
				from menus.pause import Pause
				self.scene.menu = Pause(self.game, self.scene)
			else:
				self.scene.menu = Options(self.game, self.scene)
			self.reset_actions()

		elif self.game.input.joystick:
			from menus.bind_controller import BindController
			self.scene.menu = BindController(self.game, self.scene)

		elif ACTIONS['Reset Defaults']:
			self.reset_defaults()
			self.reset_actions()
			