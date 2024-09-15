import pygame
from state import State
from timer import Timer
from settings import *
from entities import Entity, AnimatedEntity

class BaseMenu:
	def __init__(self, game, scene):

		self.game = game
		self.scene = scene
		self.navigation_timer = Timer(0.3)
		self.title = 'Press any key'
		self.element_list = ['Press any key']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()
		self.alpha = 0

	def get_cursors(self):
		cursors = []
		for cursor in ['right','left']:
			obj = AnimatedEntity([self.menu_sprites], RES/2, 30, f'../assets/particles/menu_cursor_{cursor}', z=3)
			cursors.append(obj)
		return cursors

	def get_elements(self, alignment='center', panel_width=144):

		# panel_surface = pygame.image.load('../assets/misc_images/menu_panel.png') 
		panel_surface = pygame.Surface((panel_width, HEIGHT))
		panel_surface.fill((COLOURS['black']))
		self.panel_element = Entity([self.menu_sprites], (WIDTH*0.5,HEIGHT*0.5), panel_surface, 3)

		title_surface = self.game.font.render(str(self.title), False, COLOURS['white'])
		title_element = Entity([self.menu_sprites], (self.panel_element.rect.centerx, self.panel_element.rect.top + TILESIZE*2), title_surface, 3)
		
		elements = []
		offset = 0
	
		start_y = TILESIZE * 4
		line_spacing = TILESIZE

		for option in self.element_list:
			offset += line_spacing
			surface = self.game.font.render(option, False, COLOURS['cyan'])

			special_option = option in ['Back', 'Quit', 'Quit to Menu']
			start_x = self.panel_element.rect.centerx if special_option or alignment == 'center' else self.panel_element.rect.x + TILESIZE * 1.5
			pos = (start_x, start_y + offset + (TILESIZE * 0.5 if special_option else 0))

			element = Entity([self.menu_sprites], pos, surface, 3, alignment if not special_option else None)
			elements.append(element)

		return elements

	def navigate(self):

		if self.navigation_timer.running and not (ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or abs(AXIS_PRESSED['Left Stick'][1]) > 0):
			self.navigation_timer.stop()

		if self.alpha == 255 and not self.game.block_input:
			self.next_scene()	

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
			ACTIONS['OK'] = 0
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
				sprite.image.set_alpha(min(self.alpha, 220))
			else:
				sprite.image.set_alpha(self.alpha)

	def next_scene(self):
		pass

	def update(self, dt):
		self.fade_in(1500 * dt)
		self.navigate()
		self.navigation_timer.update(dt)
		self.menu_sprites.update(dt)


	def draw(self, screen):
		self.menu_sprites.draw(screen)