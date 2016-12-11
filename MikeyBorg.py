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
screenWidth   = int(config.get("screen",  "width"))
screenHeight  = int(config.get("screen",  "height"))
imageWidth    = int(config.get("image",   "width"))
imageHeight   = int(config.get("image",   "height"))
imagePath     =     config.get("image",   "path")
consoleWidth  = int(config.get("console", "width"))
consoleHeight = int(config.get("console", "height"))
#	Variables defined using above configurable variables
displayWidth  = imageWidth  * 2
displayHeight = imageHeight * 2
imageX        = (screenWidth - displayWidth) / 2
imageY        = 20
#	Initialize the stuff
MikeyBorgUI = MikeyBorgUIClass.MikeyBorgUI([screenWidth, screenHeight], [imageWidth, imageHeight], [consoleWidth, consoleHeight])
MikeyCam  = MikeyCamClass.MikeyCam([imageWidth, imageHeight])
MikeyBorg = MikeyBorgClass.MikeyBorg()
closeNow  = Value("b", 0)

#	Function used to update the display
def cameraLoop(close, MikeyBorgUI, MikeyCam):
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

#	Function used to display the controls in the console
def showControls():
	MikeyBorgUI.addFullWidthToConsole("=")
	MikeyBorgUI.addToConsole("MikeyBorg Version 1.0.0")
	MikeyBorgUI.addFullWidthToConsole("=")
	MikeyBorgUI.addToConsole("Press 'W' to go forward")
	MikeyBorgUI.addToConsole("Press 'A' to turn left")
	MikeyBorgUI.addToConsole("Press 'D' to turn right")
	MikeyBorgUI.addToConsole("Press 'S' to go backwards")
	MikeyBorgUI.addToConsole("Press '[SHIFT]' to go slower")
	MikeyBorgUI.addToConsole("Press '[ESC]' to quit")
	MikeyBorgUI.addFullWidthToConsole("=")
		
#	Function to manage the inputs and movement
def inputLoop(close, MikeyBorg):
	inputs = InputsClass.Inputs()
	while True:
		inputs.readInputs(pygame.event.get(), close)
		if close.value == 1:
			break
		elif inputs.hadEvent:
			inputs.manageInputs(MikeyBorg)
	MikeyBorg.motorsOff()

showControls()

cameraProcess         = Process(target=cameraLoop,  args=(closeNow, MikeyBorgUI, MikeyCam,))
inputProcess          = Process(target=inputLoop,   args=(closeNow, MikeyBorg,))
cameraProcess.daemon  = True
inputProcess.daemon   = True
cameraProcess.start()
inputProcess.start()

cameraProcess.join()
inputProcess.join()
print("Program Finished")
print("======================================")