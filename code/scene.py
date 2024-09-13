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


        self.update_sprites.empty()
        self.drawn_sprites.empty()
        self.paused = False
        self.bg_colour = COLOURS['grey']
        self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (HALF_WIDTH, HALF_HEIGHT), 'characters/player', z=3)
        self.transition = Fade(self.game, [self.update_sprites, self.drawn_sprites], 250)
        self.menu = Pause(self.game, self)
        #ACTIONS['Pause'] = 0 # if hold pause while fading in, pause menu does not activate, only when explicitly pressed
  
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
        if self.paused:
            self.menu.update(dt)
        else:
            self.update_sprites.update(dt)

        if not self.game.block_input:
            if ACTIONS['Pause']:
                self.menu.index = 0
                self.paused = not self.paused
                for sprite in self.menu.menu_sprites:
                    sprite.frame_index = 0
                #from menus.menu import BaseMenu
                ACTIONS['Pause'] = 0
                ACTIONS['OK'] = 0
                self.menu.alpha = 0

        # if self.quit_to_menu:
        #     self.paused = False
        #     self.transition.on_complete = [self.next_scene]

    def draw(self, screen):

        screen.fill(self.bg_colour)
        self.drawn_sprites.draw(screen)

        sorted_sprites = sorted(self.drawn_sprites, key=lambda sprite: sprite.z)
        for sprite in sorted_sprites:
            screen.blit(sprite.image, sprite.rect)

        pygame.draw.rect(screen, COLOURS['white'], self.player.hitbox, 2)

        if self.paused:
            self.menu.draw(screen)

        # self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
        #             str('Stack: ' + str(len(self.game.stack))),
        #             None])
