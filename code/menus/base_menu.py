import pygame
from state import State
from timer import Timer
from settings import *
from entities import Entity, AnimatedEntity

class BaseMenu(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.navigation_timer = Timer(0.15)
		self.navigation_timer.start()

	def get_cursors(self):
		cursors = []
		for cursor in ['right','left']:
			obj = AnimatedEntity([self.update_sprites, self.drawn_sprites], 18, f'../assets/particles/menu_cursor_{cursor}', z=3)
			cursors.append(obj)
		return cursors

	def get_elements(self):

		panel_surface = pygame.image.load('../assets/misc_images/menu_panel.png') 
		panel_element = Entity([self.drawn_sprites], RES/2, panel_surface, 'objects')

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

	def update(self, dt):
		self.navigate()
		self.navigation_timer.update(dt)
		self.update_sprites.update(dt)

	def draw(self, screen):
		self.drawn_sprites.draw(screen)

		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
                    str('Stack: ' + str(len(self.game.stack))),
                    None])