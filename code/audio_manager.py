import pygame, sys, os
from settings import *

class AudioManager:
	def __init__(self, game):
		self.game = game
		self.sfx = self.import_sfx('../audio/sfx')

	def pause_music(self, paused=True):
		if paused: return pygame.mixer.music.pause()
		else: return pygame.mixer.music.unpause()

	def play_music(self, track, loop=True):
	    #self.track_index = start_index
	    # track = TRACKS[self.track_index]
	    pygame.mixer.music.load(f'../audio/music/{track}.mp3')
	    pygame.mixer.music.play(-1 if loop else 1, VOLUME['Music Volume'] * VOLUME['Master Volume'], 2000)

	def run_music(self):
	    pygame.mixer.music.set_volume(VOLUME['Music Volume'] * VOLUME['Master Volume'])

	def stop_music(fadeout_time=5000):
	    pygame.mixer.music.fadeout(fadeout_time)

	def import_sfx(self, path, volume=VOLUME['Sound Volume'] * VOLUME['Master Volume']):
	    sfx_dict = {}
	    for root, _, sfx_files in os.walk(path):
	        for sfx in sfx_files:
	            full_path = os.path.join(root, sfx)
	            sfx_name, sfx_ext = os.path.splitext(sfx)
	            if sfx_ext.lower() == '.wav':
	                sound = pygame.mixer.Sound(full_path)
	                sound.set_volume(volume)
	                sfx_dict[sfx_name] = sound
	    return sfx_dict

	def update_sfx_volume(self):
		new_volume = VOLUME['Sound Volume'] * VOLUME['Master Volume']
		for sound in self.sfx.values():
			sound.set_volume(new_volume)

	def run(self):
		self.run_music()