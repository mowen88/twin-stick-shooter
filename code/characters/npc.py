

import pygame
from settings import *
from timer import Timer
from support import get_animations, get_images
from characters.state_machine import BaseState

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, scene, groups, pos, path, z):
        super().__init__(groups)
    
        self.game = game
        self.scene = scene
        self.z = z
        self.frame_index = 0
        self.import_images(path)
        self.image = self.animations['idle'][self.frame_index].convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(int(-self.rect.width*0.75), int(-self.rect.height*0.5))
        self.old_hitbox = self.hitbox.copy()
        self.wall_raycast = self.hitbox.inflate(2, 0)
        self.floor_raycast = pygame.FRect(0,0, self.hitbox.width, 2)
        self.gravity = 500
        self.jump_height = 250
        self.facing = 1
        self.speed = 100
        self.direction = pygame.math.Vector2(0, self.gravity)
        self.max_fall_speed = 400
        self.on_ground = False
        self.hit_wall = False
        self.timers = {'jump':Timer(0.2)}
        self.state = Idle(self)

    def import_images(self, path):
        path = f'../assets/{path}/'
        self.animations = get_animations(path)
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = get_images(full_path)

        self.image = next(iter(self.animations.values()))[0].convert_alpha()

    def animate(self, dt, state, loop=True):

            self.frame_index += 15 * dt
            frame_count = len(self.animations[state])

            if self.frame_index >= frame_count:
                self.frame_index = 0 if loop else frame_count -1
            
            image_flip = self.facing == -1 

            facing = self.facing if self.facing == 1 else 0  
            current_frame = self.animations[state][int(self.frame_index)]     
            self.image = pygame.transform.flip(current_frame, image_flip, False)

    def get_raycast_collision(self, raycast_box):
        for sprite in self.scene.block_sprites:
            if raycast_box.colliderect(sprite.hitbox):
                return True
        return False    

    def collisions(self, axis):
        for sprite in self.scene.block_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                if axis == 'x':
                    if self.direction.x > 0 and self.hitbox.right >= sprite.hitbox.left:
                        self.hitbox.right = sprite.hitbox.left
                        self.direction.x = 0
                        
                    elif self.direction.x < 0 and self.hitbox.left <= sprite.hitbox.right:
                        self.hitbox.left = sprite.hitbox.right
                        self.direction.x = 0

                    self.rect.centerx = self.hitbox.centerx

                if axis == 'y':
                    if self.direction.y > 0 and self.hitbox.bottom >= sprite.hitbox.top:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.direction.y = 0
                        self.on_ground = True
                    elif self.direction.y < 0 and self.hitbox.top <= sprite.hitbox.bottom:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.direction.y = 0

                    self.rect.centery = self.hitbox.centery

    def set_state(self, state):
        self.state = state

    def move_x(self, direction):
        if direction == 1: self.facing = 1
        elif direction == -1: self.facing = -1
        self.direction.x = direction * self.speed

    def jump(self):
        if self.timers['jump'].running:
            self.direction.y = -self.jump_height

    def update_raycasts(self):
        self.old_hitbox = self.hitbox.copy()
        self.wall_raycast.center = self.hitbox.center
        self.floor_raycast.midtop = self.hitbox.midbottom
        if not self.get_raycast_collision(self.floor_raycast):
            self.on_ground = False

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt
        self.direction.y = min(self.max_fall_speed, self.direction.y)

    def movement(self, dt):

        self.hitbox.centerx += self.direction.x * dt
        self.rect.centerx = self.hitbox.centerx 
        self.collisions('x')
    
        self.hitbox.centery += self.direction.y * dt
        self.rect.centery = self.hitbox.centery
        self.collisions('y')

        self.update_raycasts()

    def state_logic(self):
        new_state = self.state.state_logic(self)
        if new_state: self.state = new_state
        else: self.state

    def update(self, dt):
        self.state_logic()
        self.state.update(dt, self)
        
        for timer in self.timers.values():
            timer.update(dt)

class Idle(BaseState):
    def __init__(self, npc):
        super().__init__(npc)

    def state_logic(self, npc):
        if npc.direction.x != 0:
            npc.set_state(Run(npc))

    def update(self, dt, npc):
        npc.move_x(-1)
        npc.animate(dt, self.state_name)
        npc.apply_gravity(dt)
        npc.movement(dt)

class Run(BaseState):
    def __init__(self, npc):
        super().__init__(npc)

    def state_logic(self, npc):

        if npc.direction.x == 0:
            npc.set_state(Idle(npc))

        if npc.direction.y > 0:
            npc.set_state(Fall(npc))

    def update(self, dt, npc):
        npc.move_x(-1)
        npc.animate(dt, self.state_name)
        npc.apply_gravity(dt)
        npc.movement(dt)


class Fall(BaseState):
    def __init__(self, npc):
        super().__init__(npc)
        npc.hit_wall = False

    def state_logic(self, npc):

        if npc.on_ground:
            npc.set_state(Idle(npc))

    def update(self, dt, npc):
        npc.animate(dt, self.state_name, False)
        npc.apply_gravity(dt)
        npc.movement(dt)





