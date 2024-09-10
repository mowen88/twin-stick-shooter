
from settings import *
from entities import Entity, AnimatedEntity
from transitions import CirclesTransition
from menus.menu import Menu

class ControllerBindings(Menu):
	def __init__(self, game, name):
		super().__init__(game)

		self.drawn_sprites.empty()
		self.update_sprites.empty()
		self.bg_colour = COLOURS['green']
		# self.bg_img = pygame.image.load('../assets/misc_images/gradient_bg.png').convert_alpha()
		# self.bg = Entity([self.drawn_sprites], RES/2, self.bg_img)
		self.title = f'{name} Bindings'
		self.name = name
		self.element_list = list(BUTTON_MAPS[self.name].keys())
		self.max_items_per_column = len(self.element_list)
		self.additional_elements = ['Reset Defaults','Back']
		self.assigned_elements = []
		self.element_list.extend(self.additional_elements)
		self.multi_column = True if len(self.element_list) > self.max_items_per_column else False
		self.elements = self.get_elements()
		self.cursor = AnimatedEntity([self.update_sprites, self.drawn_sprites], self.elements[self.index].rect.midleft, '../assets/particles/menu_cursor_right', 'player')

	def navigate(self):
		if not self.game.block_input and not self.navigation_timer.running and not self.game.input.bind_mode:
			if  MENU_ACTIONS['Down'] or AXIS_PRESSED['Left Stick'][1] > 0:
				self.index = (self.index + 1) % len(self.elements)
				self.navigation_timer.start()
				
			elif MENU_ACTIONS['Up'] or AXIS_PRESSED['Left Stick'][1] < 0:
				self.index = (self.index - 1) % len(self.elements)
				self.navigation_timer.start()

			if self.multi_column:
				if MENU_ACTIONS['Left'] or MENU_ACTIONS['Right'] or AXIS_PRESSED['Left Stick'][0]:
					self.navigation_timer.start()
					if self.index < self.max_items_per_column:
						self.index = min(self.index + self.max_items_per_column, len(self.element_list)-1)
					else:
						self.index -= self.max_items_per_column


			if MENU_ACTIONS['OK']:
				if self.selection == 'Back':
					self.transition.on_complete = [self.next_scene]
				elif self.selection == 'Reset Defaults':
					self.reset_defaults()
				elif self.game.input.control_type == self.name:
					self.game.input.bind_mode = True
				else:
					print('Use the right controller!')

				MENU_ACTIONS['OK'] = 0

			if MENU_ACTIONS['Back'] and self.title != 'Main Menu':
				self.transition.on_complete = [self.prev_scene]
				MENU_ACTIONS['Back'] = 0

			# update cursor and selection
			self.cursor.rect.midright = self.elements[self.index].rect.midleft
			self.selection = self.element_list[self.index]

	def reset_defaults(self):
		BUTTON_MAPS[self.name] = DEFAULT_BUTTON_MAPS[self.name]

	def get_assigned_elements(self, screen):

	    # Iterate over elements and options simultaneously
	    shown_elements = self.elements[:-len(self.additional_elements)]
	    shown_element_list = self.element_list[:len(shown_elements)]

	    for index, (element, option) in enumerate(zip(shown_elements, shown_element_list)):
	        button_id = BUTTON_MAPS[self.name][option]
	        if button_id is not None:
	            button_name = BUTTON_NAMES[self.name][button_id]
	            if button_name:
	            	pos = (element.rect.x + 120, element.rect.y)
	      
	            	if index == self.index and self.game.input.bind_mode and self.game.input.control_type == self.name:
		            	binding_text = '???'
		            	if self.game.input.new_bind is not None:
		            		new_bind = self.game.input.new_bind[0]
		            		BUTTON_MAPS[self.name][option] = new_bind
		            		button_name = BUTTON_NAMES[self.name][new_bind]
		            		self.game.input.bind_mode = False
	            	else:
	            		binding_text = button_name

	            	self.game.render_text(binding_text, COLOURS['white'], self.game.font, pos, 'topright')


	def bind_button(self):
		pass

	def next_scene(self):
		self.exit_state()

	def draw(self, screen):
		screen.fill(self.bg_colour)
		self.drawn_sprites.draw(screen)
		self.get_assigned_elements(screen)
		self.game.render_text(self.title, COLOURS['white'], self.game.font, (WIDTH * 0.5, HEIGHT * 0.15))

		self.transition.draw(screen)

		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
                    str('Stack: ' + str(len(self.game.stack))),
                    str(list(AXIS_PRESSED.values())),
                    None])
