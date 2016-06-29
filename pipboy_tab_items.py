# RasPipBoy: A Pip-Boy 3000 implementation for Raspberry Pi
#	Neal D Corbett, 2013
# Class for 'Items' tab

import pygame

import config
import pipboy_headFoot as headFoot
from pipboy_ui import SelectableList, ItemView

#Temp
items = {
	"Aid": [config.AIDS, [1,1,3], ['WG', 'VAL', 'EFFECT'], 'images\\art\\aids\\'],
	"Weapons": [config.WEAPON, [1, 1, 1, 1, 2], ['DAM', 'WG', 'VAL', 'CND', ''], 'images\\art\\weapon\\'],
	"Apparel": [config.APPAREL, [1,1,3], ['WG', 'VAL', 'EFFECT'], 'images\\art\\apparel\\'],
	"Misc": [config.MISC, [1,1,3], ['WG', 'VAL', 'EFFECT'], 'images\\art\\misc\\'],
	"Ammo": [config.AIDS, [1,1,3], ['WG', 'VAL', 'EFFECT'], 'images\\art\\aids\\'],
}
class Tab_Items:

	name = "ITEMS"
	modeNames = ["Aid","Weapons","Apparel","Misc","Ammo"]

	class Mode_Items:

		changed = True

		def __init__(self, parent, name, *args, **kwargs):
			print(name)
			elements = items[name]
			self.parent = parent
			self.rootParent = self.parent.rootParent
			self.pageCanvas = pygame.Surface((config.WIDTH, config.HEIGHT))
			self.menu = SelectableList(self.pageCanvas, (20,40), (200, 245), [elt[0] for elt in elements[0]], [], True)
			self.view = ItemView(self.pageCanvas, (233, 40), (245, 245), elements[0], elements[1], elements[2],elements[3])
			self.ui_elements = [self.menu]

		def drawPage(self):
			pageChanged = self.changed
			self.changed = False
			if(pageChanged):
				True
			return self.pageCanvas, pageChanged

		# Called every view changes to this page:
		def resetPage(self):
			True

		# Consume events passed to this page:
		def ctrlEvents(self,events):
			for elt in self.ui_elements:
				if hasattr(elt, "handle_events"):
					elt.handle_events(events)
					if hasattr(elt, "hasChanged"):
						if elt.hasChanged:
							# update view
							self.view.set_element(elt.selected)
			self.changed = True

	# Generate text for header:
	def getHeaderText(self):
		return [self.name, "Wg 180/200", "HP 210/210", "DT 19.0", "Caps 3014",]

	# Trigger page-functions
	def drawPage(self,modeNum):
		pageCanvas, pageChanged = self.modes[modeNum].drawPage()
		return pageCanvas, pageChanged
	def resetPage(self,modeNum):
		self.modes[modeNum].resetPage()
	def ctrlEvents(self,pageEvents,modeNum):
		self.modes[modeNum].ctrlEvents(pageEvents)

	# Tab init:
	def __init__(self, *args, **kwargs):
		self.parent = args[0]
		self.rootParent = self.parent.rootParent
		self.canvas = pygame.Surface((config.WIDTH, config.HEIGHT))
		self.drawnPageNum = -1

		# Item-pages all use the same class instance:
		# self.itemPage = self.Mode_Items(self)
		# self.modes = [self.itemPage,self.itemPage,self.itemPage,self.itemPage,self.itemPage]
		self.modes = [self.Mode_Items(self, 'Aid'), self.Mode_Items(self, 'Weapons'), self.Mode_Items(self, 'Apparel'), self.Mode_Items(self, 'Misc'), self.Mode_Items(self, 'Ammo'), ]

		for n in range(0,5):
			self.modes[n].pageNum = n

		self.header = headFoot.Header(self)

		# Generate footers for mode-pages:
		self.footerImgs = headFoot.genFooterImgs(self.modeNames)