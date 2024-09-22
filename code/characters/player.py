import pygame
from pygame.math import Vector2 as vec2
from settings import *
from support import *
from characters.npc import NPC

class Player(NPC):
    def __init__(self, game, scene, groups, pos, path, z=2):
        super().__init__(game, scene, groups, pos, path)


        self.import_images(path)
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.25, -self.rect.height*0.25)
        self.direction = vec2() 
        self.speed = 120

    def input(self):
        if not self.game.block_input:

            if ACTIONS['Attack']:
                self.scene.create_bullet(self.hitbox.center)
                ACTIONS['Attack'] = 0

            x_direction = 0
            y_direction = 0

            if AXIS_PRESSED['Left Stick'][0]:
                x_direction = AXIS_PRESSED['Left Stick'][0]
            elif AXIS_PRESSED['D-Pad'][0]:
                x_direction = AXIS_PRESSED['D-Pad'][0] 
            elif ACTIONS['Right']:
                x_direction = ACTIONS['Right']
            elif ACTIONS['Left']:
                x_direction = -ACTIONS['Left']

            if AXIS_PRESSED['Left Stick'][1]:
                y_direction = AXIS_PRESSED['Left Stick'][1]
            elif AXIS_PRESSED['D-Pad'][1]:
                y_direction = AXIS_PRESSED['D-Pad'][1]
            elif ACTIONS['Down']:
                y_direction = ACTIONS['Down']
            elif ACTIONS['Up']:
                y_direction = -ACTIONS['Up']

            self.direction.x = x_direction
            self.direction.y = y_direction
 

    def update(self, dt):
        self.animate('idle', 6 * dt)
        self.input()
        self.movement(dt)
        
        