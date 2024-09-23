from settings import *
from pygame.math import Vector2 as vec2
from support import get_images
from entities import Entity, AnimatedEntity
from menus.base_menu import BaseMenu 
from menus.options import Options
from menus.pause import Pause

class Audio(BaseMenu):
	def __init__(self, game, scene, index=0):
		super().__init__(game, scene)

		self.title = 'AUDIO'
		self.element_list = ['Music Volume', 'Sound Volume', 'Master Volume', 'Reset Defaults', 'Back']
		self.index = index
		self.selection = self.element_list[self.index]
		self.menu_sprites = pygame.sprite.Group()
		self.panel_alignment = WIDTH*0.4 if self.game.input.joystick else WIDTH*0.5
		self.elements = self.get_elements('midleft',180, self.panel_alignment)
		self.button_prompts = self.get_button_prompts(['Reset Defaults','Confirm','Back'])
		self.cursors = self.get_cursors()
		self.cursor = self.get_mouse_cursor('menu_cursor')
		self.alpha = 0
		self.volume_images = get_images('../assets/menu_animations/volume')
		self.volume_sliders = self.get_volume_sliders()

	def get_volume_sliders(self):
		elements = []
		offset = 0
		for index, element in enumerate(self.element_list):
			if element not in ['Reset Defaults','Back']:
				offset += self.line_spacing
				surface = self.volume_images[round(VOLUME[element] * 10)]
				pos = self.panel_element.rect.right - TILESIZE, self.elements[index].rect.bottom
				element = Entity([self.menu_sprites], pos, surface, 6, 'bottomright')
				elements.append(element)
		return elements

	def navigate(self):

		if self.navigation_timer.running and not (ACTIONS['Menu Left'] or ACTIONS['Menu Right']\
		or ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or vec2(AXIS_PRESSED['Left Stick']).magnitude() > 0):
			self.navigation_timer.stop()

		if self.alpha == 255 and not self.game.block_input:
			self.next_scene()
			if not self.game.input.joystick:
				self.mouse_navigation()

			if not self.navigation_timer.running and not self.game.input.bind_mode:

				if ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or abs(AXIS_PRESSED['Left Stick'][1]) > 0:
					self.navigation_timer.start()

					if ACTIONS['Menu Down'] or AXIS_PRESSED['Left Stick'][1] > 0:
						self.navigate_sound_cursor_reset()
						self.index = (self.index + 1) % len(self.elements)
							
					elif ACTIONS['Menu Up'] or AXIS_PRESSED['Left Stick'][1] < 0:
						self.navigate_sound_cursor_reset()
						self.index = (self.index - 1) % len(self.elements)

				elif ACTIONS['Menu Left'] or ACTIONS['Menu Right'] or abs(AXIS_PRESSED['Left Stick'][0]) > 0:
					self.navigation_timer.start()

					if self.selection not in ['Reset Defaults','Back']:

						if (ACTIONS['Menu Right'] or AXIS_PRESSED['Left Stick'][0] > 0) and VOLUME[self.selection] < 1:
							
							self.navigate_sound_cursor_reset()
							VOLUME[self.selection] = round(min(VOLUME[self.selection] + 0.1, 1),1)
							self.volume_sliders[self.index].image = self.volume_images[round(VOLUME[self.selection] * 10)]
							self.game.audio.update_sfx_volume()

						elif (ACTIONS['Menu Left'] or AXIS_PRESSED['Left Stick'][0] < 0) and VOLUME[self.selection] > 0:
					
							self.navigate_sound_cursor_reset()
							VOLUME[self.selection] = round(max(VOLUME[self.selection] - 0.1, 0),1)
							self.volume_sliders[self.index].image = self.volume_images[round(VOLUME[self.selection] * 10)]
							self.game.audio.update_sfx_volume()
		else:
			ACTIONS['Confirm'] = 0
			ACTIONS['Back'] = 0
			for cursor in self.cursors:
				cursor.frame_index = 0

		self.cursors[0].rect.midleft = self.panel_element.rect.left, self.elements[self.index].rect.centery
		self.cursors[1].rect.midright = self.panel_element.rect.right, self.elements[self.index].rect.centery
		self.selection = self.element_list[self.index]

	def navigate_sound_cursor_reset(self):
		self.game.audio.sfx['navigate'].play()
		for cursor in self.cursors:
			cursor.frame_index = 0

	def reset_defaults(self):
		self.game.audio.sfx['confirm'].play()
		for index, volume in enumerate(VOLUME):
			VOLUME[volume] = 0.5
			self.volume_sliders[index].image = self.volume_images[5]
		self.game.audio.update_sfx_volume()
		self.scene.menu = Audio(self.game, self.scene, self.index)


	def next_scene(self):
		
		if ACTIONS['Confirm']:
			if self.selection == 'Back':
				self.game.audio.sfx['back'].play()
				if hasattr(self.scene, 'paused'): # if scene is in game and has a pause variable
					self.scene.menu = Pause(self.game, self.scene)
				else:
					self.scene.menu = Options(self.game, self.scene)

			elif self.selection == 'Reset Defaults':
				self.reset_defaults()
				self.reset_actions()
			self.reset_actions()


		elif ACTIONS['Back']:
			self.game.audio.sfx['back'].play()
			self.scene.menu = Options(self.game, self.scene)
			self.reset_actions()

		elif ACTIONS['Reset Defaults']:
			self.reset_defaults()
			self.reset_actions()

