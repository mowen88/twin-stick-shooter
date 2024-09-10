import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z=4):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.z =z