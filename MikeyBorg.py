#!/usr/bin/env python
# coding: Latin-1

import pygame
from   Classes         import MikeyBorgClass
from   Classes         import MikeyCamClass
from   multiprocessing import Process, Value
from   configparser    import SafeConfigParser

#	Read the settings from the config file
config = SafeConfigParser()
config.read("MikeyBorg.ini")
screenWidth   = int(config.get("screen", "width"))
screenHeight  = int(config.get("screen", "height"))
imageWidth    = int(config.get("image",  "width"))
imageHeight   = int(config.get("image",  "height"))
imagePath     = config.get("image", "path")
#	Variables defined using above configurable variables
displayWidth  = imageWidth  * 2
displayHeight = imageHeight * 2
imageX        = (screenWidth - displayWidth) / 2
imageY        = 20

#	Set the colours
black      = pygame.Color(0, 0, 0)
messageBar = pygame.Color(119, 136, 153)
background = pygame.Color(211, 211, 211)
print("Initialising screen")
pygame.init()
pygame.display.set_caption("Press [ESC] to quit")
screen = pygame.display.set_mode([screenWidth, screenHeight])
screen.fill(background)
#	Font initialisation
monospaceFont = pygame.font.SysFont("monospace", 15)
#	Draw 'border' around the image
pygame.draw.rect(screen, black, (imageX - 5, imageY - 5, displayWidth + 10, displayHeight + 10))
#	Draw the message bar
pygame.draw.rect(screen, messageBar, (imageX - 5, imageY + 5 + displayHeight, displayWidth + 10, 20))
pygame.display.update()

MikeyCam  = MikeyCamClass.MikeyCam([imageWidth, imageHeight])
MikeyBorg = MikeyBorgClass.MikeyBorg()
closeNow  = Value("b", 0)
#	Class used for the inputs
class Inputs:
	def __init__(self):
		#	Variables used for movement
		self.hadEvent        = False
		self.moveUp          = False
		self.moveDown        = False
		self.moveLeft        = False
		self.moveRight       = False
		self.speedMultiplier = 1
	#	Function to read the inputs
	def readInputs(self, events, close):
		#	Handle each event individually
		for event in events:
			self.hadEvent = False
			#	If ESC pressed, quit
			if event.type == pygame.QUIT:
				self.hadEvent = True
				close.value   = 1
			#	Else if this is a key press
			elif event.type == pygame.KEYDOWN:
				self.hadEvent = True
				#	Work out which key was pressed
				if event.key == pygame.K_w:
					self.moveUp = True
				elif event.key == pygame.K_s:
					self.moveDown = True
				elif event.key == pygame.K_a:
					self.moveLeft = True
				elif event.key == pygame.K_d:
					self.moveRight = True
				elif event.key == pygame.K_ESCAPE:
					self.hadEvent = True
					close.value   = 1
				elif event.key == pygame.K_LSHIFT:
					self.speedMultiplier = 0.5
			#	Else check if this is a key release
			elif event.type == pygame.KEYUP:
				self.hadEvent = True
				if event.key == pygame.K_w:
					self.moveUp = False
				elif event.key == pygame.K_s:
					self.moveDown = False
				elif event.key == pygame.K_a:
					self.moveLeft = False
				elif event.key == pygame.K_d:
					self.moveRight = False
				elif event.key == pygame.K_LSHIFT:
					self.speedMultiplier = 1
		return
	#	Function to perform what was inputted
	def manageInputs(self, MikeyBorg):
		self.hadEvent = False
		turnSpeed = 0.2 * self.speedMultiplier
		fullSpeed = 1.0 * self.speedMultiplier
		#	If going forwards
		if self.moveUp:
			#	If also going left
			if self.moveLeft == True and self.moveRight == False:
				MikeyBorg.setSpeed(turnSpeed, fullSpeed)
			#	If also going right
			elif self.moveLeft == False and self.moveRight == True:
				MikeyBorg.setSpeed(fullSpeed, turnSpeed)
			#	If just going forward
			else:
				MikeyBorg.setSpeed(fullSpeed, fullSpeed)
		#	If going backwards
		elif self.moveDown:
			#	If also going left
			if self.moveLeft == True and self.moveRight == False:
				MikeyBorg.setSpeed(-fullSpeed, -turnSpeed)
			#	If also going right
			elif self.moveLeft == False and self.moveRight == True:
				MikeyBorg.setSpeed(-turnSpeed, -fullSpeed)
			#	If just going backwards
			else:
				MikeyBorg.setSpeed(-fullSpeed, -fullSpeed)
		#	If going left
		elif self.moveLeft:
			#	Turn left, if not also going right
			if self.moveRight == False:
				MikeyBorg.setSpeed(-fullSpeed, fullSpeed)
		#	If going right
		elif self.moveRight:
			MikeyBorg.setSpeed(fullSpeed, -fullSpeed)
		else:
			MikeyBorg.motorsOff()
		return

#	Function used to update the display
def displayLoop(MikeyCam, close):
		try:
			while True:
				image = MikeyCam.getImage([displayWidth, displayHeight])
				screen.blit(image, [imageX, imageY])
				pygame.display.update()
				if close.value == 1:
					break
			MikeyCam.stop()
		except KeyboardInterrupt:
			close.value = 1
			MikeyCam.stop()
		
#	Function to manage the inputs and movement
def inputLoop(MikeyBorg, close):
	inputs = Inputs()
	#try:
	while True:
		inputs.readInputs(pygame.event.get(), close)
		if close.value == 1:
			break
		if inputs.hadEvent:
			inputs.manageInputs(MikeyBorg)
	MikeyBorg.motorsOff()
	#except: KeyboardInterrupt:
	#	MikeyBorg.motorsOff()

displayProcess = Process(target=displayLoop, args=(MikeyCam,  closeNow,))
inputProcess   = Process(target=inputLoop,   args=(MikeyBorg, closeNow,))
displayProcess.daemon = True
inputProcess.daemon   = True
displayProcess.start()
inputProcess.start()

displayProcess.join()
inputProcess.join()
print("Program Finished")
print("======================================")