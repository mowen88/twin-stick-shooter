import pygame
from settings import *
from pygame.math import Vector2 as vec2
from timer import Timer
from support import get_animations, get_images
from characters.state_machine import BaseState
from characters.npc import NPC

class Crawler(NPC):

	def __init__(self, game, scene, groups, pos, path, z, facing=1):
		super().__init__(game, scene, groups, pos, path, z)

		self.facing = facing
		self.speed = 40
		self.direction = vec2(self.facing * self.speed, 0)
		self.rect = self.image.get_frect(center=pos)
		self.hitbox = self.rect.inflate(int(-self.rect.width*0.5), int(-self.rect.height*0.5))
		self.angle = 0
		
		self.last_side = None
		self.state = Idle(self)

	def animate(self, dt, state, loop=True):
		self.frame_index += 15 * dt
		frame_count = len(self.animations[state])

		if self.frame_index >= frame_count:
			self.frame_index = 0 if loop else frame_count -1

		image_flip = self.facing == -1 

		facing = self.facing if self.facing == 1 else 0  
 
		rotated_image = pygame.transform.rotate(self.animations[state][int(self.frame_index)], self.angle)

		self.image = pygame.transform.flip(rotated_image, image_flip, False)

	def get_raycast_collisions(self, raycast):
		for sprite in self.scene.block_sprites:
			if sprite.hitbox.colliderect(raycast):
				return True
		return False

	def move(self, dt):

		bottom = self.get_raycast_collisions(pygame.FRect(self.hitbox.x, self.hitbox.y + self.hitbox.height, self.hitbox.width, 1))
		top = self.get_raycast_collisions(pygame.FRect(self.hitbox.x, self.hitbox.y -1, self.hitbox.width, 1))
		left = self.get_raycast_collisions(pygame.FRect(self.hitbox.x-1, self.hitbox.y, 1, self.hitbox.height))
		right = self.get_raycast_collisions(pygame.FRect(self.hitbox.x + self.hitbox.width, self.hitbox.y, 1, self.hitbox.height))

		if bottom: 
			self.last_side = 'bottom'
			self.angle = 0
			self.direction.y = self.speed
		elif top: 
			self.last_side = 'top'
			self.angle = 180
			self.direction.y = -self.speed
		elif left: 
			self.last_side = 'left'
			self.angle = 270 if self.facing == 1 else 90
			self.direction.x = -self.speed
		elif right:
			self.last_side = 'right'
			self.angle = 90 if self.facing == 1 else 270
			self.direction.x = self.speed

		if bottom and right: self.direction = vec2(-self.speed, 0) if self.facing == -1 else vec2(0, -self.speed)
		elif bottom and left: self.direction = vec2(0, -self.speed) if self.facing == -1 else vec2(self.speed, 0)
		elif top and left: self.direction = vec2(self.speed, 0) if self.facing == -1 else vec2(0, self.speed)
		elif top and right: self.direction = vec2(0, self.speed) if self.facing == -1 else vec2(-self.speed, 0)

		elif not bottom and not top and not left and not right:

			if self.last_side == 'left': self.direction = vec2(-self.speed, 0)
			elif self.last_side == 'right': self.direction = vec2(self.speed, 0)
			elif self.last_side == 'top': self.direction = vec2(0, -self.speed)
			elif self.last_side == 'bottom': self.direction = vec2(0, self.speed)


class Idle(BaseState):
    def __init__(self, entity):
        super().__init__(entity)

    def state_logic(self, entity):
        pass

    def update(self, dt, entity):
        entity.animate(dt, self.state_name)
        entity.move(dt)
        entity.movement(dt)


class Run(BaseState):
    def __init__(self, entity):
        super().__init__(entity)

    def state_logic(self, entity):
    	pass

    def update(self, dt, entity):
     
        entity.animate(dt, self.state_name)
        entity.move(dt)

