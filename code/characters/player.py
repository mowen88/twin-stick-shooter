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

            direction = vec2()

            if AXIS_PRESSED['Left Stick'][0]:
                direction.x = AXIS_PRESSED['Left Stick'][0]
            elif AXIS_PRESSED['D-Pad'][0]:
                direction.x = AXIS_PRESSED['D-Pad'][0] 
            elif ACTIONS['Right']:
                direction.x = ACTIONS['Right']
            elif ACTIONS['Left']:
                direction.x = -ACTIONS['Left']

            if AXIS_PRESSED['Left Stick'][1]:
                direction.y = AXIS_PRESSED['Left Stick'][1]
            elif AXIS_PRESSED['D-Pad'][1]:
                direction.y = AXIS_PRESSED['D-Pad'][1] * -1
            elif ACTIONS['Down']:
                direction.y = ACTIONS['Down']
            elif ACTIONS['Up']:
                direction.y = -ACTIONS['Up']

            self.direction = direction


    def update(self, dt):
        self.animate('idle', 6 * dt)
        self.input()
        self.movement(dt)
        
        