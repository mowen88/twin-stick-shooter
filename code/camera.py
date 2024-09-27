import pygame, csv
from pygame.math import Vector2 as vec2
from settings import *

class Camera:
	def __init__(self, scene):

		self.scene = scene
		self.scene_size = self.get_scene_size()
		self.offset = vec2()

	def get_scene_size(self):
		with open(f'../scenes/{self.scene.current_scene}/{self.scene.current_scene}.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				rows = (sum(1 for row in reader) +1)
				cols = (len(row))
		return (cols * TILESIZE, rows * TILESIZE)

	def update(self, dt, target):
		# if target == self.scene.player:
		# 	centre_point_x = self.scene.player.rect.centerx - (TILESIZE * 2) * self.scene.player.facing
		# 	if self.scene.player.direction.y > 0:
		# 		centre_point_y = self.scene.player.rect.centery + TILESIZE * self.scene.player.direction.y
		# 	else:
		# 		centre_point_y = self.scene.player.rect.centery
		# else:
		# 	centre_point_x, centre_point_y = target.rect.center

		# self.offset += ((centre_point_x, centre_point_y) - self.offset - RES/2)/10

		self.offset = target.rect.center - RES*0.5

		self.offset.x = max(0, min(self.offset.x, self.scene_size[0] - WIDTH))
		self.offset.y = max(0, min(self.offset.y, self.scene_size[1] - HEIGHT))

	def draw(self, screen):

		sorted_sprites = sorted(self.scene.drawn_sprites, key=lambda sprite: sprite.z)
		for sprite in sorted_sprites:
			offset = sprite.rect.topleft - self.offset
			screen.blit(sprite.image, offset)

		# screen.fill(COLOURS['green'])
		# for layer in LAYERS:
		# 	for sprite in self.scene.drawn_sprites:
		# 		if sprite.z == layer:
		# 			offset = sprite.rect.topleft - self.offset
		# 			screen.blit(sprite.image, offset)
