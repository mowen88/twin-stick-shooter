
from state import State
from settings import *
from entities import Entity, AnimatedEntity
from transitions import Fade, CirclesTransition
from menus.background_sprites import BoxParticle
from timer import Timer
from scene import Scene

class Menu(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.bg_colour = COLOURS['purple']
		self.boxes = self.get_bg_particles()
		# self.bg_img = pygame.image.load('../assets/misc_images/gradient_bg.png').convert_alpha()
		# self.bg = Entity([self.drawn_sprites], RES/2, self.bg_img)
		self.title = 'Main Menu'
		self.transition = Fade(self.game, COLOURS['white'])
		self.navigation_timer = Timer(0.2)
		self.navigation_timer.start()
		self.line_spacing = TILESIZE
		self.column_offset = WIDTH * 0.4
		self.max_items_per_column = 5
		self.element_list = ['Start Game','Options','Controls','Quit']
		self.multi_column = True if len(self.element_list) > self.max_items_per_column else False
		self.elements = self.get_elements()
		self.index = 0
		self.selection = self.element_list[self.index]
		self.cursor = AnimatedEntity([self.update_sprites, self.drawn_sprites], self.elements[self.index].rect.midleft, '../assets/particles/menu_cursor_right', 'player')

	def get_bg_particles(self):
		boxes = []
		for x in range(int(RES.magnitude()//2)):
			boxes.append(BoxParticle())
		return boxes

	def navigate(self):
		if not self.game.block_input and not self.navigation_timer.running:
			if  MENU_ACTIONS['Down'] or AXIS_PRESSED['Left Stick'][1] > 0 or AXIS_PRESSED['D-Pad'][1] < 0:
				self.index = (self.index + 1) % len(self.elements)
				self.navigation_timer.start()
				self.cursor.frame_index = 0
				
			elif MENU_ACTIONS['Up'] or AXIS_PRESSED['Left Stick'][1] < 0 or AXIS_PRESSED['D-Pad'][1] > 0:
				self.index = (self.index - 1) % len(self.elements)
				self.navigation_timer.start()
				self.cursor.frame_index = 0

			if self.multi_column:
				if MENU_ACTIONS['Left'] or MENU_ACTIONS['Right'] or AXIS_PRESSED['Left Stick'][0] or AXIS_PRESSED['D-Pad'][0]:
					self.navigation_timer.start()
					self.cursor.frame_index = 0

					if self.index < self.max_items_per_column:
						self.index = min(self.index + self.max_items_per_column, len(self.element_list)-1)
					else:
						self.index -= self.max_items_per_column

			if MENU_ACTIONS['OK']:
				self.transition.on_complete = [self.next_scene]
				MENU_ACTIONS['OK'] = 0

			if MENU_ACTIONS['Back'] and self.title != 'Main Menu':
				self.transition.on_complete = [self.prev_scene]
				MENU_ACTIONS['Back'] = 0

			# update cursor and selection
			self.cursor.rect.midright = self.elements[self.index].rect.midleft
			self.selection = self.element_list[self.index]

	def get_elements(self):

	    obj_list = []
	    offset = 0
	    alignment = 'midleft' if self.multi_column else 'midtop'
	    start_x = WIDTH * 0.15 if self.multi_column else WIDTH * 0.5
	    start_y = HEIGHT * 0.3

	    for index, option in enumerate(self.element_list):
	        if index % self.max_items_per_column == 0 and index != 0:
	            start_x += self.column_offset
	            offset = 0

	        offset += self.line_spacing
	        image = self.game.font.render(option, False, COLOURS['cyan'])
	        pos = start_x, start_y + offset
	        menu_obj = Entity([self.drawn_sprites], pos, image, 'player', alignment)
	        obj_list.append(menu_obj)

	    return obj_list

	def prev_scene(self):
		self.exit_state()

	def next_scene(self):
		if self.selection == 'Start Game':
			Scene(self.game).enter_state()
		elif self.selection in ['Options','Controls']:
			from menus.options import Options
			Options(self.game).enter_state()
		else:
			# if quit
			self.game.quit()

	def update(self, dt):

		for box in self.boxes:
			box.update(dt)
		
		self.navigate()
		self.update_sprites.update(dt)
		self.transition.update(dt)
		self.navigation_timer.update(dt)


	def draw(self, screen):
		screen.fill(self.bg_colour)

		for box in self.boxes:
			box.draw(screen)

		self.drawn_sprites.draw(screen)
		self.game.render_text(self.title, COLOURS['white'], self.game.font, (WIDTH * 0.5, TILESIZE * 3))

		self.transition.draw(screen)

		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
                    str('Stack: ' + str(len(self.game.stack))),
                    str(list(AXIS_PRESSED.values())),
                    None])
