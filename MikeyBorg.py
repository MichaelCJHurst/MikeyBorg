#!/usr/bin/env python
# coding: Latin-1
#	Configurable variables
screenWidth   = 800
screenHeight  = 480
imageWidth    = 240 #	Needs to be at least half of the screenWidth
imageHeight   = 180 #	Needs to be at least half of the screenHeight
imagePath     = "SavedImages/"
#	Variables defined using above configurable variables
displayWidth  = imageWidth  * 2
displayHeight = imageHeight * 2
imageX        = (screenWidth - displayWidth) / 2
imageY        = 20

import pygame
from   Classes         import MikeyBorgClass
from   Classes         import MikeyCamClass
from   multiprocessing import Process, Value

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

MikeyCam  = MikeyCamClass.MikeyCam(screen, [imageWidth, imageHeight], [imageX, imageY], [displayWidth, displayHeight])
MikeyBorg = MikeyBorgClass.MikeyBorg()
closeNow  = Value("b", 0)

MikeyCamProcess  = Process(target=MikeyCam.loop,  args=(closeNow,))
MikeyBorgProcess = Process(target=MikeyBorg.loop, args=(closeNow,))
MikeyCamProcess.start()
MikeyBorgProcess.start()

MikeyCamProcess.join()
MikeyBorgProcess.join()
print("Program Finished")
print("======================================")