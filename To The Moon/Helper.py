import os, sys, time, pygame
from pygame.locals import *


#Load an image from a file in the Art sub-folder
def load_image(name, colorkey=None):
	fullname = os.path.join('Art')
	fullname = os.path.join(fullname, name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image
	
#Load a sound from a file in the Sound sub-folder
def load_sound(name):
	fullname = os.path.join('Sound')
	fullname = os.path.join(fullname, name)
	try:	
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print 'Error loading sound:',fullname
		raise SystemExit, message
	return sound
	
