#!/usr/bin/env python
# coding: Latin-1

#   Import libraries
import PicoBorgRev3 as PicoBorgRev
import time
import math
import sys

print("Running Test One for MikeyBorg")
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
#	disable communications failsafe
PBR.SetCommsFailsafe(False)
PBR.ResetEpo()

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

#	Generic Movement
def PerformMove(driveLeft, driveRight, numSeconds):
	#	set the motors running
	PBR.SetMotor1(driveRight * maxPower)
	PBR.SetMotor2(-driveLeft * maxPower)
	#	wait for the time specified
	time.sleep(numSeconds)
	#	turn off the motors
	PBR.MotorsOff()

print("Testing moving forwards:")
PerformMove(+1.0, +1.0, 2)
print("Testing moving backwards:")
PerformMove(-1.0, -1.0, 2)
print("Testing moving left:")
PerformMove(+1.0, -1.0, 2)
print("Testing moving right:")
PerformMove(-1.0, +1.0, 2)