import pygame
from state import State
from timer import Timer
from settings import *
from entities import Entity, AnimatedEntity

class BaseMenu:
	def __init__(self, game, scene):

		self.game = game
		self.scene = scene
		self.navigation_timer = Timer(0.2)
		self.title = 'Press any key'
		self.start_y = TILESIZE * 4
		self.line_spacing = TILESIZE
		self.element_list = ['']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.key_button_prompts = self.get_key_button_prompts(['Confirm'])
		self.cursors = self.get_cursors()
		self.menu_cursor = self.get_mouse_cursor('menu_cursor')
		self.alpha = 0

	def reset_actions(self):
		for action in ACTIONS:
			ACTIONS[action] = 0

	def get_mouse_cursor(self, cursor_type):
	   	if not self.game.input.joystick:
	   		cursor = Entity([self.menu_sprites], self.game.input.mouse_pos, pygame.image.load(f'../assets/particles/{cursor_type}.png').convert_alpha(), 7)
	   		return cursor

	def get_cursors(self):
		cursors = []
		for cursor in ['right','left']:
			obj = AnimatedEntity([self.menu_sprites], RES/2, 30, f'../assets/particles/menu_cursor_{cursor}', z=3)
			cursors.append(obj)
		return cursors

	def get_key_button_prompts(self, prompts):
		offset = 0
		for prompt in prompts:
			if self.game.input.joystick:
				offset += self.line_spacing
				surface = self.game.font.render(prompt, False, COLOURS['cyan'])
				pos = WIDTH - TILESIZE * 1.5, HEIGHT - TILESIZE/2 - (self.line_spacing * len(prompts)) + offset
				element = Entity([self.menu_sprites], pos, surface, 6, 'midright')

				icon = BUTTON_NAMES[self.game.input.joystick_name][BUTTON_MAPS[self.game.input.joystick_name][prompt]]
				action_surface = pygame.image.load(f'../assets/controller_button_icons/{self.game.input.joystick_name}/{icon}.png').convert_alpha()
				action_element = Entity([self.menu_sprites], element.rect.midright, action_surface, 6, 'midleft')

	def get_elements(self, alignment='center', panel_width=144):
 
		panel_surface = pygame.Surface((panel_width, HEIGHT))
		panel_surface.fill((COLOURS['black']))
		self.panel_element = Entity([self.menu_sprites], (WIDTH*0.5,HEIGHT*0.5), panel_surface, 3)
		self.panel_element.image.fill((0,0,0))

		title_surface = self.game.font.render(str(self.title), False, COLOURS['white'])
		title_element = Entity([self.menu_sprites], (self.panel_element.rect.centerx, self.panel_element.rect.top + TILESIZE*2), title_surface, 3)
		
		elements = []
		offset = 0
	
		
		for option in self.element_list:
			offset += self.line_spacing
			surface = self.game.font.render(option, False, COLOURS['cyan']).convert_alpha()

			special_option = option in ['Back', 'Quit', 'Quit to Menu']
			start_x = self.panel_element.rect.centerx if special_option or alignment == 'center' else self.panel_element.rect.x + self.line_spacing * 1.5
			pos = (start_x, self.start_y + offset + (TILESIZE * 0.5 if special_option else 0))

			element = Entity([self.menu_sprites], pos, surface, 3, alignment if not special_option else None)
			elements.append(element)

		return elements

	def mouse_navigation(self):

		prev_index = self.index
		for index, element in enumerate(self.elements):
			element_rect = pygame.Rect(self.panel_element.rect.x, element.rect.y - 2, self.panel_element.rect.width, element.rect.height + 4)
			if element_rect.collidepoint(self.game.input.mouse_pos):
				self.index = index
				if self.alpha == 255 and not self.game.block_input and ACTIONS['Left Click']:
					ACTIONS['Confirm'] = 1
					print(ACTIONS['Confirm'])

		if self.index != prev_index:
			for cursor in self.cursors:
				cursor.frame_index = 0

	def navigate(self):

		if self.navigation_timer.running and not (ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or abs(AXIS_PRESSED['Left Stick'][1]) > 0):
			self.navigation_timer.stop()

		if self.alpha == 255 and not self.game.block_input:
			self.next_scene()
			if not self.game.input.joystick:
				self.mouse_navigation()

			if not self.navigation_timer.running and not self.game.input.bind_mode:
				if ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or abs(AXIS_PRESSED['Left Stick'][1]) > 0:
					self.navigation_timer.start()
					for cursor in self.cursors:
						cursor.frame_index = 0

					if ACTIONS['Menu Down'] or AXIS_PRESSED['Left Stick'][1] > 0:
						self.index = (self.index + 1) % len(self.elements)			
					elif ACTIONS['Menu Up'] or AXIS_PRESSED['Left Stick'][1] < 0:
						self.index = (self.index - 1) % len(self.elements)
		else:
			ACTIONS['Confirm'] = 0
			ACTIONS['Back'] = 0
			for cursor in self.cursors:
				cursor.frame_index = 0

		self.cursors[0].rect.midleft = self.panel_element.rect.left, self.elements[self.index].rect.centery
		self.cursors[1].rect.midright = self.panel_element.rect.right, self.elements[self.index].rect.centery
		self.selection = self.element_list[self.index]


	def fade_in(self, speed):
		self.alpha += speed
		if self.alpha >= 255:
			self.alpha = 255
		for sprite in self.menu_sprites:
			if sprite == self.panel_element:
				sprite.image.set_alpha(min(self.alpha, 128))
			else:
				sprite.image.set_alpha(self.alpha)

	def next_scene(self):
		pass

	def update(self, dt):

		self.fade_in(1500 * dt)
		self.navigate()
		self.navigation_timer.update(dt)
		self.menu_sprites.update(dt)

		if self.cursor:
			self.cursor.rect.center = self.game.input.mouse_pos

	def draw(self, screen):
		sorted_sprites = sorted(self.menu_sprites, key=lambda sprite: sprite.z)
		for sprite in sorted_sprites:
			screen.blit(sprite.image, sprite.rect)


