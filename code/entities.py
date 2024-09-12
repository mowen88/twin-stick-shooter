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
            'midleft': self.image.get_rect(midleft=pos),
            'midright': self.image.get_rect(midright=pos),
            'midtop': self.image.get_rect(midtop=pos),
        }
        return rect_methods.get(alignment, self.image.get_rect(center=pos))


class AnimatedEntity(pygame.sprite.Sprite):
    def __init__(self, groups, pos, speed, path, z=1):
        super().__init__(groups)

        self.speed = speed
        self.z = z
        self.frame_index = 0
        self.frames = get_images(path)
        self.frame_count = len(self.frames)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self, speed, animation_type='loop'):
        self.frame_index += speed

        if self.frame_index >= self.frame_count:
            if animation_type == 'once':
                self.frame_index = self.frame_count-1
            elif animation_type == 'end':
                self.kill()
            else:
                self.frame_index = self.frame_index % self.frame_count

        current_frame = int(self.frame_index)
        if self.image != self.frames[current_frame]:
            self.image = self.frames[current_frame]
        
    def update(self, dt):
        self.animate(self.speed * dt, 'once')
