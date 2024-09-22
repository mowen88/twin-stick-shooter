import random
from state import State
from settings import *
from entities import Entity, AnimatedEntity
from transitions import Fade
from timer import Timer
from menus.base_menu import BaseMenu
from menus.main_menu import MainMenu

class SmokeParticle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, colour, radius, z=1, alignment='topleft'):
        super().__init__(groups)
  
        self.z = z
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, colour, (radius, radius), radius)
        self.rect = self.image.get_frect(topleft=pos)
        self.alpha = 255
        self.random_float = random.uniform(0.1, 1.0)
        self.direction = pygame.math.Vector2(self.random_float, self.random_float)
        self.speed = 15
        self.vel = self.direction * self.speed

    def update(self, dt):
        self.alpha = random.randrange(50, 200)

        self.rect.topleft += self.vel * dt

        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width
        if self.rect.y > HEIGHT:
            self.rect.y = -self.rect.height

        # Apply alpha to the image
        self.image.set_alpha(self.alpha)



class TitleScene(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.get_bg_particles()
		self.menu = MainMenu(self.game, self)
		self.transition = Fade(self.game, [self.update_sprites, self.drawn_sprites], 1000)

	def get_bg_particles(self):
		circles = []
		for x in range(int(RES.magnitude())*2):
			pos = (random.random() * WIDTH, random.random() * HEIGHT)
			radius = random.random()*TILESIZE*0.75
			#colour = random.choice([COLOURS['deep_red'], COLOURS['red']])
			colour = COLOURS['blue']
			circles.append(SmokeParticle([self.update_sprites, self.drawn_sprites], pos, colour, radius, z=1))
		return circles

	def next_scene(self):
		from scene import Scene
		Scene(self.game).enter_state()

	def update(self, dt):
		self.update_sprites.update(dt)
		self.menu.update(dt)

	def draw(self, screen):

		screen.fill(COLOURS['deep_blue'])

		sorted_sprites = sorted(self.drawn_sprites, key=lambda sprite: sprite.z)
		for sprite in sorted_sprites:
			screen.blit(sprite.image, sprite.rect)

		self.menu.draw(screen)

		self.debug([str('FPS: '+ str(int(self.game.clock.get_fps()))),
                    str('Stack: ' + str(len(self.game.stack))),
                    str(self.transition.alpha),
                    None])
