import pygame
from support import *
from settings import *
from entities import AnimatedEntity

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, scene, groups, pos, path, z=2):
        super().__init__(groups)

        self.game = game
        self.scene = scene
        self.z = z
        self.frame_index = 0
        self.import_images(path)
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.25, -self.rect.height*0.25)

    def import_images(self, path):
        path = f'../assets/{path}/'
        self.animations = get_animations(path)
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = get_images(full_path)

        self.image = next(iter(self.animations.values()))[0].convert_alpha()

    def animate(self, state, speed, loop=True):
        self.frame_index += speed
        if self.frame_index >= len(self.animations[state]):
            self.frame_index = 0 if loop else len(self.animations[state]) - 1

        self.image = self.animations[state][int(self.frame_index)]
 
    def movement(self, dt):

        if self.direction.magnitude() > 1:
            self.direction = self.direction.normalize()
        
        self.hitbox.center += self.direction * self.speed * dt
        self.rect.center = self.hitbox.center

    def update(self, dt):
        self.animate('idle', 6 * dt)
        self.movement(dt)



