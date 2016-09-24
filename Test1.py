#!/usr/bin/env python
# coding: Latin-1
print("======================================")
print("Running Test One for MikeyBorg")
print("======================================")
print("Importing Libraries")
#   Import libraries
import PicoBorgRev3 as PicoBorgRev
import pygame
import time
import math
import sys
import os
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
#PBR.SetCommsFailsafe(False)
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
#	Input refresh interval, so it can be controlled >:)
interval = 0.01

#	Setup pygame and key states
print("Initialising pygame and key states")
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
pygame.init()
screen = pygame.display.set_mode([300, 300])
pygame.display.set_caption("Press [ESC] to quit")

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

#	Generic Movement
def PerformMove(driveLeft, driveRight, numSeconds):
	#	set the motors running
	PBR.SetMotor1(driveRight * maxPower)
	PBR.SetMotor2(-driveLeft * maxPower)
	#	wait for the time specified
	time.sleep(numSeconds)
	#	turn off the motors
	PBR.MotorsOff()
print("======================================")
print("Initialisation complete, running tests")
print("======================================")
print("Testing moving forwards:")
PerformMove(+1.0, +1.0, 2)
time.sleep(0.25)
print("Testing moving backwards:")
PerformMove(-1.0, -1.0, 2)
time.sleep(0.25)
print("Testing moving left:")
PerformMove(+1.0, -1.0, 2)
time.sleep(0.25)
print("Testing moving right:")
PerformMove(-1.0, +1.0, 2)
time.sleep(0.25)
print("======================================")
print("Testing complete, awaiting input")
print("Press [ESC] to quit")
print("======================================")

try:
	#	Loop forevermore, unless ESC pressed
	while True:
		#	Get the currently pressed keys
		PygameHandler(pygame.event.get())
		#	If something has changed since last iteration, do something
		if hadEvent:
			hadEvent = False
			if moveQuit:
				print("[ESC] clicked, terminating program")
				break;
			elif moveLeft:
				PBR.SetMotor1(+maxPower)
				PBR.SetMotor2(+maxPower)
			elif moveRight:
				PBR.SetMotor1(-maxPower)
				PBR.SetMotor2(-maxPower)
			elif moveUp:
				PBR.SetMotor1(+maxPower)
				PBR.SetMotor2(-maxPower)
			elif moveDown:
				PBR.SetMotor1(-maxPower)
				PBR.SetMotor2(+maxPower)
			else:
				#	No key pressed, stop motors
				PBR.MotorsOff()
		#	Wait for the interval
		time.sleep(interval)
	#	Stop the motors
	PBR.MotorsOff()
#	CTRL+C pressed, so quit
except KeyboardInterrupt:
	PBR.MotorsOff()
print("Program Finished")
print("======================================")