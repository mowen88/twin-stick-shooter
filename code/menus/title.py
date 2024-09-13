import random
from state import State
from settings import *
from entities import Entity, AnimatedEntity
from transitions import Fade
from timer import Timer
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

class TitleScene(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.get_bg_particles()
		from menus.main_menu import MainMenu
		self.menu = MainMenu(self.game, self)
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

	def next_scene(self):
		from scene import Scene
		Scene(self.game).enter_state()

	def update(self, dt):
		self.update_sprites.update(dt)
		self.menu.update(dt)

	def draw(self, screen):

		screen.fill(COLOURS['purple'])

		sorted_sprites = sorted(self.drawn_sprites, key=lambda sprite: sprite.z)
		for sprite in sorted_sprites:
			screen.blit(sprite.image, sprite.rect)

		self.menu.draw(screen)

		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
                    str('Stack: ' + str(len(self.game.stack))),
                    str(self.transition.alpha),
                    None])
