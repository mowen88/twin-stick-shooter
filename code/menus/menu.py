import random
from state import State
from settings import *
from entities import Entity, AnimatedEntity
from transitions import Fade
from timer import Timer
from scene import Scene
from menus.base_menu import BaseMenu


class BoxParticle(pygame.sprite.Sprite):
	def __init__(self, groups, pos, colour, surf, z=1, alignment='topleft'):
		super().__init__(groups)

		self.image = surf
		self.z = z
		self.image.fill(colour)
		self.rect = self.image.get_frect(topleft = pos)
		self.alpha = 255
		self.direction = pygame.math.Vector2(random.uniform(0.1, 1.0), random.uniform(0.1, 1.0))
		self.speed = 20
		self.vel = self.direction * self.speed

	def update(self, dt):
		self.alpha = random.randrange(0, 255)
		self.rect.topleft += self.vel * dt

		if self.rect.x > WIDTH:
			self.rect.x = -self.rect.width
		if self.rect.y > HEIGHT:
			self.rect.y = -self.rect.height

		self.image.set_alpha(self.alpha)


class MainMenu(BaseMenu):
	def __init__(self, game):
		super().__init__(game)

		self.title = 'Main Menu'
		self.element_list = ['Start Game','Options','Controls','Quit','Option 1','Option 2','Option 3','Back']
		self.index = 0
		self.selection = self.element_list[self.index]
		self.elements = self.get_elements()
		self.cursors = self.get_cursors()

		self.get_bg_particles()
		self.transition = Fade(self.game, [self.update_sprites, self.drawn_sprites], 1000)

	def get_bg_particles(self):
		boxes = []
		for x in range(int(RES.magnitude())):
			pos = (random.random() * WIDTH, random.random() * HEIGHT)
			size = (random.random()*TILESIZE*0.5, random.random()*TILESIZE*0.5)
			surf = pygame.Surface(size)
			colour = random.choice([COLOURS['brown'], COLOURS['salmon']])
			boxes.append(BoxParticle([self.update_sprites, self.drawn_sprites], pos, colour, surf, z=1))
		return boxes

	def navigate(self):

		if self.navigation_timer.running and not (ACTIONS['Menu Down'] or ACTIONS['Menu Up'] or abs(AXIS_PRESSED['Left Stick'][1]) > 0):
			self.navigation_timer.stop()

		if not self.game.block_input:
			if ACTIONS['OK']:
				self.transition.on_complete = [self.next_scene]
				ACTIONS['OK'] = 0

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
	
		self.cursors[0].rect.midleft = self.elements[self.index].rect.midright
		self.cursors[1].rect.midright = self.elements[self.index].rect.midleft
		self.selection = self.element_list[self.index]



	def next_scene(self):
		if self.selection == 'Start Game':
			Scene(self.game).enter_state()
		elif self.selection in ['Options']:
			from menus.options import OptionsMenu
			OptionsMenu(self.game).enter_state()
		elif self.selection in ['Controls']:
			from menus.controls import ControlsMenu
			ControlsMenu(self.game).enter_state()
		else:
			# if quit
			self.game.quit()


	def draw(self, screen):

		print(self.navigation_timer.running)
		screen.fill(COLOURS['purple'])

		sorted_sprites = sorted(self.drawn_sprites, key=lambda sprite: sprite.z)
		for sprite in sorted_sprites:
			screen.blit(sprite.image, sprite.rect)
		
		#self.drawn_sprites.draw(screen)

		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
                    str('Stack: ' + str(len(self.game.stack))),
                    str(self.transition.alpha),
                    None])