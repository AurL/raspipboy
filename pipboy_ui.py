import pygame
import config
import os

# Contains all UI elements base class.
# callbacks is for (onEnable, onDisable)
class SelectableList:
	def __init__(self, parent_image, pos, size, items, callbacks, allow_multi):
		self.pos = pos
		self.size = size
		self.image = pygame.Surface(size).convert()
		self.parent_image = parent_image
		self.items = items
		self.callbacks = callbacks
		self.selected = 0
		self.enabled = []
		self.select(self.selected)
		self.allow_multi = allow_multi
		self.hasChanged = False
		#Enable sound here

	def select(self, item):
		self.selected = item
		self.hasChanged = True
		self.update()

	def get_enabled(self):
		if self.enabled:
			return self.enabled[0]

	def toggleItem(self, index):
		if index in self.enabled:
			self.enabled.remove(index)
			if(len(self.callbacks) == 2):
				self.callbacks[1](index)
		else:
			if self.allow_multi is False:
				self.enabled = []

			self.enabled.append(index)
			if len(self.callbacks) > 0:
				self.callbacks[0](index)

		self.update()

	def handle_events(self, event):
		if (type(event) is list):
			if event[0] == 'sel':
				self.toggleItem(self.selected)
			elif type(event[0]) is list and len(event[0]) == 3:
				change = -event[0][2]
				# Check that this is always a list with 3 elements
				if self.selected + change >= 0 and self.selected + change < len(self.items):
						self.select(self.selected + change)
						if config.USE_SOUND:
								config.SOUNDS["changemode"].play()

	def update(self):
		self.image.fill((0, 0, 0))
		offset = 7
		for i in range(len(self.items)):
			text = config.FONTS[13].render(" %s " % self.items[i], True, config.DRAWCOLOUR, (0, 0, 0))
			if i == self.selected:
				selected_rect = (0, offset - 2, 180, text.get_size()[1] + 4)
				pygame.draw.rect(self.image, config.DRAWCOLOUR, selected_rect, 2)
			if i in self.enabled:
				pygame.draw.rect(self.image, config.DRAWCOLOUR, [6, text.get_size()[1]/2.0 + offset - 2, 6, 6] , 0)
			self.image.blit(text, (15, offset))
			offset += text.get_size()[1] + 6

		self.parent_image.blit(self.image, self.pos)


#square types [small, large, perks]
SMALL = [ 80, 20 , 9]
MID = [ 160, 20 , 19]
LARGE = [ 236, 20 , 29] #Size: 185 185
PERK =  [ 200, 100, 90]
offset_x = 6
class ItemView:
	# item_data: list of data elements to be added
	# item_layout: one dimension list with indexes for ui type (SMALL=1, LARGE=2, PERK=3  adding - to keep space of element)
	def __init__(self, parent_image, pos, size, item_data, item_layout, data_caption, art_dir=''):
		self.pos = pos
		self.size = size
		self.image = pygame.Surface(size).convert()
		self.parent_image = parent_image

		self.item_data = item_data
		self.item_layout = item_layout
		self.data_caption = data_caption
		self.content = []
		self.art_dir = art_dir
		self.art = None
		self.set_element(0)

	def set_element(self, index):
		print('ok')
		self.content = self.item_data[index][1:len(self.data_caption) + 1:]
		self.art = pygame.image.load(os.path.join(self.art_dir, self.item_data[index][-1]))
		self.art = pygame.transform.scale(self.art, (155, 155))
		self.redraw()

	def split_text(self, text, length):
		textlength = len(text)
		index = 0
		elements = []
		text.rstrip()
		while index < textlength:
			t = text[index * length:(index + 1) * length:]
			elements.append(t)
			index+=1
		return elements

	def build_content(self, index, string_size):
		if(len(self.data_caption) == 0):
				caption = self.content[index]
		else:
				caption = '{}{}{}'.format(self.data_caption[index], ' ' * (string_size - (len(self.data_caption[index]) + len(str(self.content[index])))), self.content[index])
		return caption

	def draw_small(self, index, pos_x, pos_y):
		pygame.draw.line(self.image,
			config.DRAWCOLOUR,
			(pos_x, pos_y ), (pos_x + SMALL[0] - 4, pos_y),
			 2)
		pygame.draw.line(self.image,
			config.DRAWCOLOUR,
			(pos_x + SMALL[0] - 4, pos_y ), (pos_x + SMALL[0] - 4, pos_y + SMALL[1]),
			 2)

	def draw_mid(self, index, pos_x, pos_y):
		pygame.draw.line(self.image,
			config.DRAWCOLOUR,
			(pos_x, pos_y ), (pos_x + MID[0] - 4, pos_y),
			 2)
		pygame.draw.line(self.image,
			config.DRAWCOLOUR,
			(pos_x + MID[0] - 4, pos_y ), (pos_x + MID[0] - 4, pos_y + MID[1]),
			 2)
		return pos_x + MID[0]

	def draw_large(self, index, pos_y):
		pygame.draw.line(self.image,
			config.DRAWCOLOUR,
			(0, pos_y ), (LARGE[0], pos_y),
			 2)
		pygame.draw.line(self.image,
			config.DRAWCOLOUR,
			(LARGE[0], pos_y ), (LARGE[0], pos_y + LARGE[1]),
			 2)

	def handle_events(self, event):
		if (type(event) is list):
			if event[0] == 'sel':
				self.toggleItem(self.selected)
			elif type(event[0]) is list and len(event[0]) == 3:
				change = -event[0][2]
				# Check that this is always a list with 3 elements
				if self.selected + change >= 0 and self.selected + change < len(self.items):
						self.select(self.selected + change)
						if config.USE_SOUND:
								config.SOUNDS["changemode"].play()

	def redraw(self):
		self.image.fill((0, 0, 0))
		offset = 5
		offset_x = 0
		offset_y = 175
		current_line_score = 0
		for e, t in enumerate(self.item_layout):
			if t == 1:
				text = config.FONTS[16].render(self.build_content(e, SMALL[2]), True, config.DRAWCOLOUR, (0, 0, 0))
				self.image.blit(text, (offset_x, offset_y))
				self.draw_small(e, offset_x, offset_y)
				offset_x += SMALL[0]
				current_line_score += 1
			if t == 2:
				text = config.FONTS[16].render(self.build_content(e, MID[2]), True, config.DRAWCOLOUR, (0, 0, 0))
				self.image.blit(text, (offset_x, offset_y))
				self.draw_mid(e, offset_x, offset_y)
				offset_y += 20 + offset_y
			if t == 3:
				offset_y += 20 + offset
				text = config.FONTS[16].render(self.build_content(e, LARGE[2]), True, config.DRAWCOLOUR, (0, 0, 0))
				self.image.blit(text, (0, offset_y))
				self.draw_large(e, offset_y)
			if t == 4:
				caption = self.split_text(self.content[e], 32)
				for i, el in enumerate(caption):
					text = config.FONTS[14].render(el, True, config.DRAWCOLOUR, (0, 0, 0))
					self.image.blit(text, (0, offset_y + i * (text.get_size()[1])))
				self.draw_large(e, offset_y)
			if current_line_score == 3 and e < len(self.item_layout) - 2 and self.item_layout[e + 1] != 3 :
				offset_y += 20 + offset
				current_line_score = 0
				offset_x = 0

		self.image.blit(self.art, (40, 0), None, pygame.BLEND_RGBA_ADD)
		self.parent_image.blit(self.image, self.pos)