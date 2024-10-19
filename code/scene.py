import pygame
from pygame.math import Vector2 as vec2
from state import State
from settings import *
from pytmx.util_pygame import load_pygame
from camera import Camera
from menus.pause import Pause
from entities import Entity, Block, AnimatedEntity
from characters.npc import NPC
from characters.player import Player
from transitions import Fade, CirclesTransition
from bullet import Bullet


class Scene(State):
    def __init__(self, game, current_scene='0', entry_point='0'):
        State.__init__(self, game)

        self.update_sprites.empty()
        self.drawn_sprites.empty()
        self.paused = False
        self.bg_colour = COLOURS['grey']

        self.current_scene = current_scene
        self.entry_point = entry_point

        self.block_sprites = pygame.sprite.Group()

        self.camera = Camera(self) 
        self.tmx_data = load_pygame(f'../scenes/{self.current_scene}/{self.current_scene}.tmx')
        self.create_scene()
        self.camera.offset = vec2(self.target.rect.center - RES/2)

        self.crosshair_pos = RES/2
        self.crosshair = self.get_crosshair('game_cursor')
        self.menu = Pause(self.game, self)
        self.transition = Fade(self.game, [self.update_sprites], 250, COLOURS['white'], pygame.Surface(RES))
    
        
    def create_scene(self):
        layers = []
        for layer in self.tmx_data.layers:
            layers.append(layer.name)

        if 'entries' in layers:
            for obj in self.tmx_data.get_layer_by_name('entries'):
                if obj.name == self.entry_point:
                    self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (HALF_WIDTH, HALF_HEIGHT), 'characters/player', z=3)
                    self.target = self.player

        if 'entities' in layers:
            for obj in self.tmx_data.get_layer_by_name('entities'):
                if obj.name == 'npc':
                    self.npc = NPC(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'characters/randomer', z=3)

        if 'blocks' in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name('blocks').tiles():
                Block([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), pygame.Surface((TILESIZE,TILESIZE)), 3, 'topleft')

    def get_crosshair(self, cursor_type):
        pos = pygame.mouse.get_pos() if not self.game.input.joystick else self.crosshair_pos
        cursor = Entity([self.drawn_sprites], pos, pygame.image.load(f'../assets/particles/{cursor_type}.png'), 7)
        return cursor

    def next_scene(self):
        #from menus.options import Options
        self.exit_state()

    def create_bullet(self, pos):
        Bullet([self.drawn_sprites], pos)

    def events(self, events):
        events.get_input()

    def update(self, dt):


        if self.paused:
            self.crosshair.rect.topleft = RES
            self.menu.update(dt)
        else:
            self.crosshair.rect.center = pygame.mouse.get_pos()
            self.update_sprites.update(dt)
            self.camera.update(dt, self.target)
            self.crosshair_pos = RES/2 + self.camera.offset

        if not self.game.block_input:
            if ACTIONS['Pause']:
                self.paused = not self.paused
                self.game.audio.sfx['confirm'].play()
                self.menu.index = 0
                self.game.audio.pause_music(self.paused)
                for sprite in self.menu.menu_sprites:
                    sprite.frame_index = 0
                #from menus.menu import BaseMenu
                ACTIONS['Pause'] = 0
                ACTIONS['Confirm'] = 0
                ACTIONS['Left Click'] = 0

        # if self.quit_to_menu:
        #     self.paused = False
        #     self.transition.on_complete = [self.next_scene]

    def draw(self, screen):

        screen.fill(COLOURS['blue'])
        self.camera.draw(screen)

        if self.paused: self.menu.draw(screen)
        if self.transition.alpha > 0: screen.blit(self.transition.image, (0,0))
 
        self.debug([str('FPS: '+ str(int(self.game.clock.get_fps()))),
                    str('Stack: ' + str(len(self.game.stack))),
                    str(self.player.timers['jump_buffer'].counter),
                    str(self.player.direction.x),
                    None])

        pygame.draw.rect(screen, COLOURS['yellow'], self.player.floor_raycast)
