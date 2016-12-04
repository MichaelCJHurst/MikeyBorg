#!/usr/bin/env python
# coding: Latin-1
import pygame
import time
from   Classes         import InputsClass
from   Classes         import MikeyBorgClass
from   Classes         import MikeyCamClass
from   Classes         import MikeyBorgUIClass
from   configparser    import SafeConfigParser
from   multiprocessing import Process, Value

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
#	Initialize the stuff
MikeyBorgUI = MikeyBorgUIClass.MikeyBorgUI([screenWidth, screenHeight], [imageWidth, imageHeight])
MikeyCam  = MikeyCamClass.MikeyCam([imageWidth, imageHeight])
MikeyBorg = MikeyBorgClass.MikeyBorg()
closeNow  = Value("b", 0)

#	Function used to update the display
def displayLoop(MikeyCam, close):
		try:
			while True:
				image = MikeyCam.getImage([displayWidth, displayHeight])
				if not image == False:
					MikeyBorgUI.updateImage(image)
				if close.value == 1:
					break
			MikeyCam.stop()
		except KeyboardInterrupt:
			close.value = 1
			MikeyCam.stop()
		
#	Function to manage the inputs and movement
def inputLoop(MikeyBorg, close):
	inputs = InputsClass.Inputs()
	while True:
		inputs.readInputs(pygame.event.get(), close)
		if close.value == 1:
			break
		if inputs.hadEvent:
			inputs.manageInputs(MikeyBorg)
	MikeyBorg.motorsOff()

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