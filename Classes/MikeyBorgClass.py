#!/usr/bin/env python
# coding: Latin-1
import pygame
from   Classes import PicoBorgRev3 as PiBorgRev

class MikeyBorg:
	
	def __init__(self):
		#	Variables used for movement
		self.hadEvent        = False
		self.moveUp          = False
		self.moveDown        = False
		self.moveLeft        = False
		self.moveRight       = False
		self.speedMultiplier = 1
		#	Speed and Power settings
		voltageIn  = 12.0
		voltageOut = 6.0
		if voltageOut > voltageIn:
			self.maxPower = 1.0
		else:
			self.maxPower = voltageOut / float(voltageIn)
		self.leftMotors  = 0
		self.rightMotors = 0
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
		print("MikeyBorg Initialised")
	
	def loop(self, close):
		try:
			while True:
				self._readInputs(pygame.event.get(), close)
				if close.value == 1:
					break
				self._manageInputs()
			self.PBR.MotorsOff()
			print("Motors Stopped")
		except KeyboardInterrupt:
			self.PBR.MotorsOff()
			print("Motors Killed")

	#	Function to read the inputs
	def _readInputs(self, events, close):
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
	#	Function to perform what was inputted
	def _manageInputs(self):
		if self.hadEvent:
			self.hadEvent = False
			#	If going forwards
			if self.moveUp:
				#	If also going left
				if self.moveLeft == True and self.moveRight == False:
					self._setSpeed(0.2, 1.0)
				#	If also going right
				elif self.moveLeft == False and self.moveRight == True:
					self._setSpeed(1.0, 0.2)
				#	If just going forward
				else:
					self._setSpeed(1.0, 1.0)
			#	If going backwards
			elif self.moveDown:
				#	If also going left
				if self.moveLeft == True and self.moveRight == False:
					self._setSpeed(-1, -0.2)
				#	If also going right
				elif self.moveLeft == False and self.moveRight == True:
					self._setSpeed(-0.2, -1)
				#	If just going backwards
				else:
					self._setSpeed(-1, -1)
			#	If going left
			elif self.moveLeft:
				#	Turn left, if not also going right
				if self.moveRight == False:
					self._setSpeed(-1.0, 1.0)
			#	If going right
			elif self.moveRight:
				self._setSpeed(1.0, -1.0)
			else:
				self.PBR.MotorsOff()
	#	Function to set the motor speeds
	def _setSpeed(self, left, right):
		self.PBR.SetMotor1(right * self.maxPower * self.speedMultiplier)
		self.PBR.SetMotor2(-left * self.maxPower * self.speedMultiplier)