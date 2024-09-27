import pygame, sys, os, time, json, cProfile
from pygame import mixer
from os import walk
from input_manager import InputManager
from audio_manager import AudioManager
from menus.splash_screen import PygameLogo
from support import read_data, write_data
from settings import *

class Game:
    def __init__(self):
 
        mixer.init()
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((RES), pygame.FULLSCREEN|pygame.SCALED)#, vsync=1)
        self.font = pygame.font.Font(FONT, 9)
        self.big_font = pygame.font.Font(FONT, 10)
        self.running = True
        self.in_menu = False
        self.block_input = False
        self.input = InputManager(self)
        self.audio = AudioManager(self)
        
        self.stack = []
        self.pygame_logo = PygameLogo(self)
        self.stack.append(self.pygame_logo)

        read_data('key_map.txt', KEY_MAP)
        read_data('volume.txt', VOLUME)
        read_data('button_maps.txt', BUTTON_MAPS)

    def quit(self):
        write_data('volume.txt', VOLUME)
        write_data('key_map.txt', KEY_MAP)
        write_data('button_maps.txt', BUTTON_MAPS)
        self.running = False
        pygame.quit() 
        sys.exit()

    def get_input(self):
        self.input.get_input()

    def render_text(self, text, colour, font, pos, alignment=False):
        surf = font.render(str(text), False, colour)
        if alignment == 'topleft': rect = surf.get_rect(topleft=pos)
        elif alignment == 'topright': rect = surf.get_rect(topright=pos)
        elif alignment == 'midtop': rect = suxrf.get_rect(midtop=pos)
        else: rect = surf.get_rect(center = pos)
        self.screen.blit(surf, rect)

    def update(self, dt):
        self.stack[-1].update(dt)
 
    def draw(self, screen):
        self.stack[-1].draw(screen)
        pygame.display.flip()

    def main_loop(self):
        dt = self.clock.tick(60)/1000
        events = pygame.event.get()
        self.input.get_input(events)
        self.audio.run()
        self.update(dt)
        self.draw(self.screen)

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.main_loop()
       