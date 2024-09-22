import pygame, sys, os, time, json, cProfile
from pygame import mixer
from os import walk
from input_manager import InputManager
from menus.splash_screen import PygameLogo
from settings import *

class Game:
    def __init__(self):
 
        mixer.init()
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((RES))#, pygame.FULLSCREEN|pygame.SCALED)
        self.font = pygame.font.Font(FONT, 9)
        self.big_font = pygame.font.Font(FONT, 10)
        self.running = True
        self.in_menu = False
        self.block_input = False
        self.input = InputManager(self)
        
        self.stack = []
        self.pygame_logo = PygameLogo(self)
        self.stack.append(self.pygame_logo)

    def quit(self):
        self.running = False
        pygame.quit() 
        sys.exit()

    def get_input(self):
        self.input.get_input()

    def render_text(self, text, colour, font, pos, alignment=False):
        surf = font.render(str(text), False, colour)
        if alignment == 'topleft': rect = surf.get_rect(topleft=pos)
        elif alignment == 'topright': rect = surf.get_rect(topright=pos)
        elif alignment == 'midtop': rect = surf.get_rect(midtop=pos)
        else: rect = surf.get_rect(center = pos)
        self.screen.blit(surf, rect)

    def update(self, dt):
        self.stack[-1].update(dt)
 
    def draw(self, screen):
        self.stack[-1].draw(screen)
        pygame.display.flip()

    def main_loop(self):
        dt = self.clock.tick()/1000
        events = pygame.event.get()
        self.input.get_input(events)
        self.update(dt)
        self.draw(self.screen)

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.main_loop()
       