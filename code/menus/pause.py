import random
from state import State
from settings import *
from entities import Entity, AnimatedEntity
from transitions import Fade
from timer import Timer
from menus.base_menu import BaseMenu

class Pause():
	def __init__(self, game, scene):

		self.game = game
		self.scene = scene

		self.navigation_timer = Timer(0.3)
		self.navigation_timer.start()
		self.title = 'Paused'
		self.element_list = ['Options','Controls','Quit to Menu']
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

	def get_elements(self):

		panel_surface = pygame.image.load('../assets/misc_images/menu_panel.png') 
		panel_element = Entity([self.menu_sprites], RES/2, panel_surface, z=3)

		title_surface = self.game.font.render(str(self.title), False, COLOURS['white'],)
		title_element = Entity([self.menu_sprites], (WIDTH * 0.5, TILESIZE * 2), title_surface, z=3)
		
		elements = []
		offset = 0
		start_x = WIDTH * 0.5
		start_y = TILESIZE * 3
		line_spacing = TILESIZE

		for option in self.element_list:
			offset += line_spacing
			surface = self.game.font.render(option, False, COLOURS['cyan'])
			pos = start_x, start_y + offset
			element = Entity([self.menu_sprites], pos, surface, z=3)
			elements.append(element)
		return elements

	def navigate(self):

		if self.navigation_timer.running and not (ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or abs(AXIS_PRESSED['Left Stick'][1]) > 0):
			self.navigation_timer.stop()

		if self.alpha == 255:
			if ACTIONS['OK'] and self.selection == 'Quit to Menu':
				self.scene.paused = not self.scene.paused
				self.scene.transition.on_complete = [self.scene.next_scene]
				# ACTIONS['OK'] = 0
				# ACTIONS['Pause'] = 0
				for action in ACTIONS:
					ACTIONS[action] = 0

			elif ACTIONS['Pause']:
				self.scene.paused = not self.scene.paused
				ACTIONS['Pause'] = 0 

			if not self.navigation_timer.running:
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

				# if ACTIONS['OK'] and self.selection == 'Options':
				# 	ACTIONS['OK'] = 0

		self.cursors[0].rect.midright = self.elements[self.index].rect.midleft
		self.cursors[1].rect.midleft = self.elements[self.index].rect.midright
		self.selection = self.element_list[self.index]

	def fade_in(self, speed):
		self.alpha += speed
		if self.alpha >= 255:
			self.alpha = 255
		for sprite in self.menu_sprites:
			sprite.image.set_alpha(self.alpha)

	def update(self, dt):
		self.fade_in(3000 * dt)
		self.navigate()
		self.navigation_timer.update(dt)
		self.menu_sprites.update(dt)

	def draw(self, screen):
		self.menu_sprites.draw(screen)



