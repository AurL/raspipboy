# RasPipBoy: A Pip-Boy 3000 implementation for Raspberry Pi
#	Neal D Corbett, 2013
# Configuration data

# Device options
#  (These will be automatically be set to 'False' if unavailable)
USE_INTERNET = False		# Download map/place data via internet connection
USE_GPS = False			# Use GPS module, accessed via GPSD daemon
USE_SOUND = True		# Play sounds via RasPi's current sound-source
USE_CAMERA = False		# Use RasPi camera-module as V.A.T.S
USE_SERIAL = False		# Communicate with custom serial-port controller
USE_GPIO = False
GPIO_AVAILABLE = False

QUICKLOAD = True		# If true, commandline-startup bits aren't rendered
FORCE_DOWNLOAD = False	# Don't use cached map-data, if online

# Render screen-objects at this size - smaller is faster
WIDTH = 480
HEIGHT = 320

# Address for map's default position:
#	(used if GPS is inactive)
defaultPlace = "Paris"

# Player data:
PLAYERNAME = 'Waleguene'
PLAYERLEVEL = 33

FPS = 15

import pygame, os

# Using GPIO.BCM as mode
GPIO_ACTIONS = {
#     4: "module_stats", #GPIO 4
# 	14: "module_items", #GPIO 14
# 	15: "module_data", #GPIO 15
# 	17:	"knob_1", #GPIO 17
# 	18: "knob_2", #GPIO 18
# 	7: "knob_3", #GPIO 7
# 	22: "knob_4", #GPIO 22
# 	23: "knob_5", #GPIO 27
# #	31: "dial_up", #GPIO 23
# 	27: "dial_down" #GPIO 7
}


# My Google-API key:
# (this is limited to only 2000 location requests a day,
#    so please don't use this key if you're making your own project!)
gKey = 'AIzaSyB4umXdIssUQX7Wu7rT_c4RdYLCKxfYKq5K0'


# Teensy USB serial: symbolic link set up by creating:
#   /etc/udev/rules.d/99-usb-serial.rules
# With line:
#   SUBSYSTEM=="tty", ATTRS{manufacturer}=="Teensyduino", SYMLINK+="teensy"
SERIALPORT = '/dev/teensy'
# Pi GPIO serial:
#SERIALPORT = '/dev/ttyAMA0'

# Test serial-controller:
if USE_SERIAL:
	# Load libraries used by serial device, if present:
	def loadSerial():
		try:
			print ("Importing Serial libraries...")
			global serial
			import serial
		except:
			# Deactivate serial-related systems if load failed:
			print "SERIAL LIBRARY NOT FOUND!"
			USE_SERIAL = False
	loadSerial()
if(USE_SERIAL):
	try:
		print ("Init serial: %s" %(SERIALPORT))
		ser = serial.Serial(SERIALPORT, 9600)
		ser.timeout=1

		print "  Requesting device identity..."
		ser.write("\nidentify\n")

		ident = ser.readline()
		ident = ident.strip()
		print ("    Value: %s" %(str(ident)))

		if (ident != "PIPBOY"):
			print "  Pip-Boy controls not found on serial-port!"
			#config.USE_SERIAL = False

	except:
		print ("* Failed to access serial! Ignoring serial port")
		USE_SERIAL = False
print ("SERIAL: %s" %(USE_SERIAL))

# Test camera:
if USE_CAMERA:
	# Is there a camera module connected?
	def hasCamera():
		try:
			import picamera
			camera = picamera.PiCamera()
			camera.close()
			return True
		except:
			return False

	USE_CAMERA = hasCamera()
print ("CAMERA: %s" %(USE_CAMERA))

# Downloaded/auto-generated data will be put here:
CACHEPATH = 'cache'
if not os.path.exists(CACHEPATH):
	os.makedirs(CACHEPATH)

DRAWCOLOUR = pygame.Color (255, 255, 255)
TINTCOLOUR = pygame.Color (33, 255, 180)
SELBOXGREY = 50

EVENTS = {
	'SONG_END': pygame.USEREVENT + 1
}

print "Loading images..."
IMAGES = {
	"background":pygame.image.load('images/pipboy_back.png'),
	"scanline":pygame.image.load('images/pipboyscanlines.png'),
	"distort":pygame.image.load('images/pipboydistorteffectmap.png'),
	"statusboy":pygame.image.load('images/pipboy_statusboy.png'),
}

print "(done)"

# Test internet connection:
if USE_INTERNET:
	import urllib2

	def internet_on():
		try:
			# Can we access this Google address?
			response=urllib2.urlopen('http://www.google.com',timeout=5)
			return True
		except urllib2.URLError as err: pass
		return False

	USE_INTERNET = internet_on()
print ("INTERNET: %s" %(USE_INTERNET))

# Test and set up sounds::
MINHUMVOL = 0.7
MAXHUMVOL = 1.0
if USE_SOUND:
	try:
		print "Loading sounds..."
		pygame.mixer.init(44100, -16, 2, 2048)

		SOUNDS = {
			"start":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_up.wav'),
			"end":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_down.wav'),
			"hum":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_hum_lp.wav'),
			"scroll":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_scroll.wav'),
			"changetab":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_tab.wav'),
			"changemode":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_mode.wav'),
			"static":		pygame.mixer.Sound('sounds/radio/ui_radio_static_lp.wav'),
			"tapestart":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_start.wav'),
			"tapestop":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_stop.wav'),
			"lighton":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_on.wav'),
			"lightoff":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_off.wav'),
			"beacon":		pygame.mixer.Sound('sounds/radio/beacon/ui_radio_beacon_header.wav'),
			"camerastart":	pygame.mixer.Sound('sounds/vats/ui_vats_enter.wav'),
			#"cameraexit":	pygame.mixer.Sound('sounds/vats/ui_vats_exit.wav'),
		}
		SOUNDS["hum"].set_volume(MINHUMVOL)
		print "(done)"
	except:
		USE_SOUND = False
print ("SOUND: %s" %(USE_SOUND))

# Set up fonts:
pygame.font.init()
kernedFontName = 'fonts/monofonto-kerned.ttf'
monoFontName = 'fonts/monofonto.ttf'
FONTS = {}
for x in range(10, 28):
	FONTS[x] = pygame.font.Font(kernedFontName, x)

# Scale font-sizes to chosen resolution:
FONT_SML = pygame.font.Font(kernedFontName, int (HEIGHT * (12.0 / 360)))
FONT_MED = pygame.font.Font(kernedFontName, int (HEIGHT * (16.0 / 360.0)))
FONT_LRG = pygame.font.Font(kernedFontName, int (HEIGHT * (18.0 / 360.0)))
MONOFONT = pygame.font.Font(monoFontName, int (HEIGHT * (16.0 / 360.0)))

# Find monofont's character-size:
tempImg = MONOFONT.render("X", True, DRAWCOLOUR, (0, 0, 0))
charHeight = tempImg.get_height()
charWidth = tempImg.get_width()
del tempImg


SPECIAL = [
	'Strengh          5',
	'Perception       8',
	'Endurance        3',
	'Charisme         2',
	'Intelligence     6',
	'Agility          12',
	'Luck             8'
]

# Items [Name, Damage, weight, value, State(CND), icon_path_in_prop_dir]
WEAPON = [
	['Big fucking rifle','130', '7', 1158, 20,'556mm(36/232)', 'rifle.png'],
	['Baseball bat','130', '7', 18, 20,'p382', 'bat.png'],
	['Tazer','130', '7', 18, 20,'bool', 'tazer.png']
]

APPAREL = [
	['Vault 101 suit', 2, 150, 'fancyoutfit.png'],
	['Steampunk glasses', 2, 150, 'sunglasses.png'],
	['Steampunk hat', 2, 150, 'hat.png'],
	['Moon boots', 2, 150, 'fancyoutfit.png']
]

# Weight, Value, effects
AIDS = [
	['Bubble Gum', 1, 1, 'HIT+1  RAD+1' ,'bubblegum.png'],
	['Stimpack', 0, 75, 'HIT+30 ' ,'stimpack.png'],
	['Buffout', 0, 20, 'HIT+60 END+3 STR+2'  ,'buffout.png'],
	['Mentats', 0, 20, 'INT+2 PER+2 CHR+1' ,'mentats.png'],
	['Nuka Cola',1, 20, 'RAD+3 HIT+2' ,'nukacola.png'],
	['Psycho', 0, 20, 'DMG +25%' ,'psycho.png'],
	['RadAway',0, 20, 'RAD-50'  ,'radaway.png'],
	['Purified Water',1, 20, 'HIT+2' ,'water.png'],
	['Cram', 1, 5, 'HIT+1 RAD+3' ,'cram.png'],
	['Jet', 0, 20, 'AP+15' ,'jet.png'],
]

MISC = [
	['OnePlus One', 3, 300, 'stimpak.png'],
	['House keys', 3, 10, 'stimpak.png'],
	['Bus card', 3, 10, 'stimpak.png']
]

AMMO = [
	'9mm ammo         750',
	'357 magnum       120'
]

RADIOSTATION = [
	'Galaxy News Radio',
	'Radio New Vegas',
	'Mojave Music'
]

RADIODIR = [
	'sounds\\radio\\gnr\\',
	'sounds\\radio\\rnv\\',
	'sounds\\radio\\mm\\'
]

PERK = [
	['Cowboy', '25 %% more damage when using any revolver, lever-action firearm, dynamite, knife or hatchet', 'cowboy.png'],
	['Fast Shot', '', 'fastshot.png'],
	['Weapon Handling', 'Weapon Strength Requirements -2', 'weaponhandling.png'],
	['Meat of Champions', "The essence of champions flows through your veins. When you cannibalize corpses you temporarily gain Caesar's intelligence, Mr. House's luck, The King's charisma, and President Kimball's strength.", 'meatofchampions.png'],
	['Rapid Reload', "Rapid Reload allows you to reload all your weapons 25%% faster than normal. This also has the effect of allowing you to switch ammunition types faster.", 'rapidreload.png'],
	['Swift Learner', 'You are indeed a Swift Learner with this Perk, as each level gives you an additional +5%% bonus whenever you earn experience points. This is best taken early.', 'swiftlearner.png'],
	['Vigilant Recycler', "Waste not, want not. When you use Energy Weapons, you are more likely to recover drained ammunition. You also have more efficient recycling recipes available at the wasteland's workbenches.", 'vigilantrecycler.png']
]

SKILL = [
	#['Computer Whiz', 'Can make one extra attempt to hack a locked-down terminal', 'computerwiz.png']
]
# OBJECTS