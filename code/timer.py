import pygame
from settings import *

class Timer:
	def __init__(self, duration, on_complete=None):

		self.duration = duration
		self.on_complete = on_complete
		self.counter = 0
		self.running = False

	def start(self):
		 self.running = True

	def stop(self):
		self.running = False
		self.counter = 0
	
	def reset(self):
		self.counter = self.duration

	def update(self, dt):
		if self.running:
			self.counter += dt
			if self.counter >= self.duration:
				self.counter = 0
				if self.on_complete is not None:
					self.on_complete()
				else:
					self.running = False

class GameTimer:
	def __init__(self, game):
		self.game = game

		self.active = False
		self.secs = 0
		self.mins = 0
		self.hours = 0
		self.elapsed_time = SAVE_DATA['time_elapsed']

	def add_times(self, time1, time2):
		hours1, mins1, secs1 = map(int, time1.split(':'))
		hours2, mins2, secs2 = map(int, time2.split(':'))
		
		total_hours = hours1 + hours2
		total_mins = mins1 + mins2
		total_secs = secs1 + secs2

		total_mins += total_secs//60
		total_secs %= 60
		total_hours += total_mins//60
		total_mins %= 60

		result = "%02d:%02d:%02d" % (total_hours, total_mins, total_secs)

		return result

	def get_elapsed_time(self):
	    return "%02d:%02d:%02d" % (self.hours, self.mins, self.secs)

	def reset(self):
		self.elapsed_time = 0

	def stop_start(self):
		self.active = not self.active

	def update(self, dt):
		if self.active:
			self.elapsed_time += dt/60 

			self.hours = int(self.elapsed_time//3600)
			self.mins = int((self.elapsed_time % 3600)//60)
			self.secs = int(self.elapsed_time % 60)
