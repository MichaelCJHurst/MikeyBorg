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
			print("Camera Stopped")
		except KeyboardInterrupt:
			MikeyCam.stop()
			print("Camera Killed")

displayProcess  = Process(target=displayLoop,  args=(MikeyCam, closeNow,))
MikeyBorgProcess = Process(target=MikeyBorg.loop, args=(closeNow,))
displayProcess.start()
MikeyBorgProcess.start()

displayProcess.join()
MikeyBorgProcess.join()
print("Program Finished")
print("======================================")