#!/usr/bin/env python
# coding: Latin-1
#	Configurable variables
debug = False
interval = 0.01
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
#import picamera
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
voltageIn = 12.0
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
print("Initialising camera")
#camera = picamera.PiCamera()
#camera.vflip = False
#camera.hflip = False
#camera.brightness = 60
#camera.resolution = (screenWidth, screenHeight)
#camera.framerate = 24
#camera.start_preview()
#rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)
print("Initialising screen")
pygame.init()
pygame.camera.init()
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Press [ESC] to quit")
screen.fill(black)

print("Defining functions")
#	Function to handle events
def PygameHandler(events):
	#	Variables accessible outside this function
	global hadEvent
	global moveUp
	global moveDown
	global moveLeft
	global moveRight
	global moveQuit
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

#	Testing Movement
def TestMove(driveLeft, driveRight, numSeconds):
	#	set the motors running
	PBR.SetMotor1(driveRight * maxPower)
	PBR.SetMotor2(-driveLeft * maxPower)
	#	wait for the time specified
	time.sleep(numSeconds)
	#	turn off the motors
	PBR.MotorsOff()
#	Setting speeds
def SetSpeed(driveLeft, driveRight):
	PBR.SetMotor1(driveRight * maxPower)
	PBR.SetMotor2(-driveLeft * maxPower)
#	If debugging, run tests
if debug == True:
	print("======================================")
	print("Initialisation complete, running tests")
	print("======================================")
	print("Testing moving forwards:")
	TestMove(+1.0, +1.0, 2)
	time.sleep(0.25)
	print("Testing moving backwards:")
	TestMove(-1.0, -1.0, 2)
	time.sleep(0.25)
	print("Testing moving left:")
	TestMove(+1.0, -1.0, 2)
	time.sleep(0.25)
	print("Testing moving right:")
	TestMove(-1.0, +1.0, 2)
	time.sleep(0.25)
	print("======================================")
	print("Testing complete, awaiting input")
	print("Press [ESC] to quit")
	print("======================================")
#	If not debugging, just wait for input
else:
	print("======================================")
	print("Initialisation complete, awaiting input")
	print("Press [ESC] to quit")
	print("======================================")
cam = pygame.camera.Camera("/dev/video0", [screenWidth, screenHeight], "RGM")
cam.start()
image = cam.get_image()
try:
	#	Loop forevermore, unless ESC pressed
	while True:
		#	Camera stuff
		#       If image is ready, use it
		if cam.query_image():
                        image = cam.get_image()
                        #       Set image as background
                        screen.blit(image, [0, 0])
		#stream = io.BytesIO()
		#camera.capture(stream, use_video_port=True, format="rgb", resize=(screenWidth, screenHeight))
		#stream.seek(0)
		#stream.readinto(rgb)
		#stream.close()

		#img = pygame.image.frombuffer(stream, [screenWidth, screenHeight], "RGB")
		#stream.close()
		#img = pygame.image.frombuffer(rgb[0:(streamLength)], [screenWidth, screenHeight], "RGB")
		#screen.blit(img, (0, 0))
		pygame.display.update()
		#	Get the currently pressed keys
		PygameHandler(pygame.event.get())
		#	If something has changed since last iteration, do something
		if hadEvent:
			hadEvent = False
			#	If ESC was clicked
			if moveQuit:
				print("[ESC] clicked, terminating program")
				break
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
		#	Wait for the interval
		#time.sleep(interval)
	#	Stop the motors
	PBR.MotorsOff()
#	CTRL+C pressed, so quit
except KeyboardInterrupt:
	PBR.MotorsOff()
print("Program Finished")
print("======================================")
