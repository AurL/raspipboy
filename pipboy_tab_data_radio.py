# RasPipBoy: A Pip-Boy 3000 implementation for Raspberry Pi
#	Neal D Corbett, 2013
# 'Radio' page
import os
import pygame
import config
from radioui import Oscilloscope
from pipboy_ui import SelectableList
from random import choice

class Mode_Radio:

	changed = True

	def __init__(self, *args, **kwargs):
		self.name = "Radio"
		self.pageCanvas = pygame.Surface((config.WIDTH, config.HEIGHT))
		self.menu = SelectableList(self.pageCanvas, (20,40), (200, 50), config.RADIOSTATION, [self.play, self.stop], False)
		self.ui_elements = [self.menu]
		self.oscilloscope = Oscilloscope(self.pageCanvas, (283, 60), (188, 188))
		self.player = Radio(self.oscilloscope)

	def drawPage(self):
		pageChanged = (self.changed or pygame.mixer.music.get_busy())
		if(pageChanged):
			self.oscilloscope.update()
		self.changed = False
		return self.pageCanvas, pageChanged

	# Called every view changes to this page:
	def resetPage(self):
		True

	# Consume events passed to this page:
	def ctrlEvents(self,events):
		for elt in self.ui_elements:
			if hasattr(elt, "handle_events"):
				elt.handle_events(events)

		self.changed = True

	def play(self, index):
		self.player.set_directory(config.RADIODIR[self.menu.get_enabled()])
		self.player.play_random()

	def stop(self, index):
		self.player.stop()


class Radio():

	STATES = {
		'stopped': 0,
		'playing': 1,
		'paused': 2
	}

	def __init__(self, oscillo, *args, **kwargs):
		self.state = self.STATES['stopped']
		self.directory = '';
		self.files = []
		self.oscillo = oscillo
		pygame.mixer.music.set_endevent(config.EVENTS['SONG_END'])

	def set_directory(self, directory):
		self.directory = directory
		self.load_files()

	def play_random(self):
		f = choice(self.files)
		self.filename = f
		self.oscillo.load_music(f)
		pygame.mixer.music.load(f)
		pygame.mixer.music.play()
		self.state = self.STATES['playing']
		self.oscillo.running = True

	def play(self):
		if self.state == self.STATES['paused']:
			pygame.mixer.music.unpause()
			self.state = self.STATES['playing']
		else:
			self.play_random()
		self.oscillo.running = True

	def pause(self):
		self.state = self.STATES['paused']
		pygame.mixer.music.pause()

	def stop(self):
		self.state = self.STATES['stopped']
		pygame.mixer.music.stop()

	def load_files(self):
		files = []
		for f in os.listdir(self.directory):
			if f.endswith(".mp3") or f.endswith(".ogg") or f.endswith(".wav"):
				files.append(self.directory + f)
		self.files = files
