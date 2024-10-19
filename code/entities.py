import pygame, math
from support import *
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z=1, alignment='center'):
        super().__init__(groups)

        self.image = surf
        self.z = z
        self.rect = self.get_pos(pos, alignment)

    def get_pos(self, pos, alignment):
        rect_methods = {
            'topleft': self.image.get_frect(topleft=pos),
            'topright': self.image.get_frect(topright=pos),
            'bottomleft': self.image.get_frect(bottomleft=pos),
            'bottomright': self.image.get_frect(bottomright=pos),
            'midleft': self.image.get_frect(midleft=pos),
            'midright': self.image.get_frect(midright=pos),
            'midtop': self.image.get_frect(midtop=pos),
            'midbottom': self.image.get_frect(midbottom=pos),
        }
        return rect_methods.get(alignment, self.image.get_frect(center=pos))

class Block(Entity):
    def __init__(self, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z=1, alignment='center'):
        super().__init__(groups, pos, surf, z, alignment)

        self.hitbox = self.rect

class AnimatedEntity(pygame.sprite.Sprite):
    def __init__(self, groups, pos, path, speed, animation_type='loop', z=1):
        super().__init__(groups)

        self.speed = speed
        self.animation_type = animation_type
        self.z = z
        self.frame_index = 0
        self.frames = get_images(path)
        self.frame_count = len(self.frames)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self, speed):
        self.frame_index += speed

        if self.frame_index >= self.frame_count:
            if self.animation_type == 'once':
                self.frame_index = self.frame_count-1
            elif self.animation_type == 'end':
                self.kill()
            else:
                self.frame_index = self.frame_index % self.frame_count

        current_frame = int(self.frame_index)
        if self.image != self.frames[current_frame]:
            self.image = self.frames[current_frame]
        
    def update(self, dt):
        self.animate(self.speed * dt)
