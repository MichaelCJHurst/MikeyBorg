#!/usr/bin/env python
# coding: Latin-1
import pygame
from   Classes import PicoBorgRev3 as PiBorgRev

class MikeyBorg:
	
	def __init__(self):
		#	Speed and Power settings
		voltageIn  = 12.0
		voltageOut = 6.0
		if voltageOut > voltageIn:
			self.maxPower = 1.0
		else:
			self.maxPower = voltageOut / float(voltageIn)
		#	Set up the PicoBorg reverse
		self.PBR = PiBorgRev.PicoBorgRev()
		self.PBR.Init()
		#	If no board is found, look for it
		if not self.PBR.foundChip:
			boards = PiBorgRev.ScanForPicoBorgReverse()
			if len(boards) == 0:
				print('No boards found :(')
			else:
				print("No board at address %02X, but found:" % (self.PBR.i2cAddress))
				for board in boards:
					print("	%02X (%d)" (board, board))
				print("To change the board, add self.PBR.i2cAddress = 0x%02X" % (boards[0]))
				sys.exit()
		#	Enable communications failsafe
		self.PBR.ResetEpo()
	
	def forwards(self):
		self._setSpeed(1.0, 1.0)
		return
	
	def reverse(self):
		self._setSpeed(-1.0, -1.0)
		return
	
	def rotateLeft(self):
		self._setSpeed(-1.0, 1.0)
		return
	
	def rotateRight(self):
		self._setSpeed(1.0, -1.0)
		return
	
	#	This function is just to keep _setSpeed hidden, just in case
	# I decide to add more to it at some stage.
	def setSpeed(self, left, right):
		self._setSpeed(left, right)
	
	def motorsOff(self):
		self.PBR.MotorsOff()
		return

	def _setSpeed(self, left, right):
		self.PBR.SetMotor1(right * self.maxPower)
		self.PBR.SetMotor2(-left * self.maxPower)
		return