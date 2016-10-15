#!/usr/bin/env python
# coding: Latin-1
#	Configurable variables
debug = False
interval = 1
screenWidth = 512
screenHeight = 512
#	Start program
print("======================================")
print("Running Test One for MikeyBorg")
print("======================================")
print("Importing Libraries")
#   Import libraries
import PicoBorgRev3 as PicoBorgRev
import pygame
import threading
import pygame.camera
from pygame.locals import *
import io
import time
import os
from PIL import Image
print("Imported Libraries")
print("Setting up reverse")
#   set-up reverse
PBR = PicoBorgRev.PicoBorgRev()
PBR.Init()
#   If no board is found, look for it
if not PBR.foundChip:
	boards = PicoBorgRev.ScanForPicoBorgReverse()
	if len(boards) == 0:
		print('No boards found :(')
	else:
		print("No board at address %02X, but found:" % (PBR.i2cAddress))
		for board in boards:
			print("	%02X (%d)" (board, board))
		print("To change the board, add PBR.i2cAddress = 0x%02X" % (boards[0]))
		
		sys.exit()
#	enable communications failsafe
print("Enabling communications failsafe")
PBR.ResetEpo()
print("Setting movement settings")
#	Movement Settings
timeForward1m = 5.7
timeSpin360 = 4.8
#	Power Settings
voltageIn = 1.6 * 10
voltageOut = 6.0
#	setup power limits
if voltageOut > voltageIn:
	maxPower = 1.0
else:
	maxPower = voltageOut / float(voltageIn)
#	Variables for motor speeds
leftMotors = 0
rightMotors = 0
#	Setup pygame and key states
print("Initialising key states")
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
streamLength = screenWidth * screenHeight * 3
black = pygame.Color(0, 0, 0)
print("Initialising screen")
pygame.init()
print("Initialising camera")
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0", [screenWidth, screenHeight], "RGM")
cam.start()
print("Displaying screen")
image = cam.get_image()
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Press [ESC] to quit")
screen.fill(black)

print("Defining Camera class")
class CameraClass(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	
	def run(self):
		while True:
			#	If an image is ready, use it
			if cam.query_image():
				image = cam.get_image()
				screen.blit(image, [0, 0])
				#	Update background with the image
				pygame.display.update()
				time.sleep(interval)

print("Defining Event class")
class EventClass(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	
	def run(self):
		while True:
		#	Variables accessible outside this function
			global hadEvent
			global moveUp
			global moveDown
			global moveLeft
			global moveRight
			global moveQuit
			events = pygame.event.get()
			#	Handle each event individually
			for event in events:
				#	If ESC pressed, quit
				if event.type == pygame.QUIT:
					hadEvent = True
					moveQuit = True
				#	Else check if this is a key press
				elif event.type == pygame.KEYDOWN:
					hadEvent = True
					if event.key == pygame.K_UP:
						moveUp = True
					elif event.key == pygame.K_DOWN:
						moveDown = True
					elif event.key == pygame.K_LEFT:
						moveLeft = True
					elif event.key == pygame.K_RIGHT:
						moveRight = True
					elif event.key == pygame.K_ESCAPE:
						moveQuit = True
				#	Else check if this is a key release
				elif event.type == pygame.KEYUP:
					hadEvent = True
					if event.key == pygame.K_UP:
						moveUp = False
					elif event.key == pygame.K_DOWN:
						moveDown = False
					elif event.key == pygame.K_LEFT:
						moveLeft = False
					elif event.key == pygame.K_RIGHT:
						moveRight = False
					elif event.key == pygame.K_ESCAPE:
						moveQuit = False
			#	If something has changed since last iteration, do something
			if hadEvent:
				hadEvent = False
				#	If ESC was clicked
				if moveQuit:
					print("[ESC] clicked, terminating program")
					PBR.MotorsOff()
					print("Program Finished")
					print("======================================")
					pygame.quit()
					exit()
				#	If going forwards
				elif moveUp:
					#	If also going left
					if moveLeft == True and moveRight == False:
						SetSpeed(0.2, 1.0)
					#	If also going right
					elif moveLeft == False and moveRight == True:
						SetSpeed(1.0, 0.2)
					#	If just going forward
					else:
						SetSpeed(1.0, 1.0)
				#	If going backwards
				elif moveDown:
					#	If also going left
					if moveLeft == True and moveRight == False:
						SetSpeed(-1, -0.2)
					#	If also going right
					elif moveLeft == False and moveRight == True:
						SetSpeed(-0.2, -1)
					#	If just going backwards
					else:
						SetSpeed(-1, -1)
				#	If going left
				elif moveLeft:
					#	Turn left, if not also going right
					if moveRight == False:
						SetSpeed(-1.0, 1.0)
				#	If going right
				elif moveRight:
					SetSpeed(1.0, -1.0)
				else:
					PBR.MotorsOff()

def SetSpeed(driveLeft, driveRight):
	PBR.SetMotor1(driveRight * maxPower)
	PBR.SetMotor2(-driveLeft * maxPower)

print("======================================")
print("Initialisation complete, awaiting input")
print("Press [ESC] to quit")
print("======================================")

cameraThread = CameraClass(1, "Camera", 1)
eventThread  = EventClass(2,  "Event",  1)

cameraThread.start()
eventThread.start()

#PBR.MotorsOff()
#print("Program Finished")
#print("======================================")
