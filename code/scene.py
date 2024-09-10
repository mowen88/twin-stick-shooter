import pygame
from state import State
from settings import *
from pytmx.util_pygame import load_pygame
from menus.pause import Pause
from entities import Entity, AnimatedEntity
from characters.player import Player
from transitions import Fade, CirclesTransition
from bullet import Bullet


class Scene(State):
    def __init__(self, game):
        State.__init__(self, game)

        #self.game.stack.pop()
        self.paused = False
        self.quit_to_menu = False
        self.game.menu_state = False
        self.bg_colour = COLOURS['green']
        self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (HALF_WIDTH, HALF_HEIGHT), 'characters/player', z=3)
        self.transition = Fade(self.game, [self.update_sprites, self.drawn_sprites], 500)
  
    def next_scene(self):
        #from menus.options import Options
        self.exit_state()



    def create_scene(self):
        pass

    def create_bullet(self, pos):
        Bullet([self.drawn_sprites], pos)

    def events(self, events):
        events.get_input()

    def update(self, dt):
        # if ACTIONS['Back']:
        #     self.transition.on_complete = [self.next_scene]
        #     ACTIONS['Back'] = 0
        if not self.game.block_input:
            if ACTIONS['Pause']:
                self.paused = not self.paused
                from menus.menu import BaseMenu
                Pause(self.game).enter_state()
                ACTIONS['Pause'] = 0

        # if self.quit_to_menu:
        #     self.paused = False
        #     self.transition.on_complete = [self.next_scene]

        #if self.paused:
        self.update_sprites.update(dt)

    def draw(self, screen):

        screen.fill(self.bg_colour)
        self.drawn_sprites.draw(screen)

        for x in range(5):
            for sprite in self.drawn_sprites:
                if sprite.z == x:
                    screen.blit(sprite.image, sprite.rect)

        pygame.draw.rect(screen, COLOURS['white'], self.player.hitbox, 2)

        # self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
        #             str('Stack: ' + str(len(self.game.stack))),
        #             None])
