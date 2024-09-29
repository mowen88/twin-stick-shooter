
from state import State
from settings import *
from entities import Entity
from transitions import Fade
from menus.title import TitleScene

class PygameLogo(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.timer = 0
		self.duration = 1
		Entity([self.drawn_sprites], (WIDTH * 0.5, HEIGHT * 0.6), pygame.image.load('../assets/pygame_logo.png').convert_alpha(), 3)
		self.transition = Fade(self.game, [self.update_sprites, self.drawn_sprites], 800)

	def next_scene(self):
		# splash screen never needed on state stack again
		#self.game.stack.pop()
		# MenuBG(self.game).enter_state()
		TitleScene(self.game).enter_state()

	def update(self, dt):
		if self.timer >= self.duration: self.transition.on_complete = [self.next_scene]
		else:self.timer += dt
		self.update_sprites.update(dt)

	def draw(self, screen):
		screen.fill((0,0,0))
		self.game.render_text('Made with', COLOURS['white'], self.game.font, (WIDTH * 0.5, HEIGHT * 0.2))
		self.drawn_sprites.draw(screen)
		