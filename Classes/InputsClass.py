#!/usr/bin/env python
# coding: Latin-1
import pygame

class Inputs:

	def __init__(self):
		#	Variables used for movement
		self.hadEvent        = False
		self.moveUp          = False
		self.moveDown        = False
		self.moveLeft        = False
		self.moveRight       = False
		self.speedMultiplier = 1

	#	Function to read the inputs
	def readInputs(self, events, close):
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
		return

	#	Function to perform what was inputted
	def manageInputs(self, MikeyBorg):
		self.hadEvent = False
		turnSpeed = 0.2 * self.speedMultiplier
		fullSpeed = 1.0 * self.speedMultiplier
		#	If going forwards
		if self.moveUp:
			#	If also going left
			if self.moveLeft == True and self.moveRight == False:
				MikeyBorg.setSpeed(turnSpeed, fullSpeed)
			#	If also going right
			elif self.moveLeft == False and self.moveRight == True:
				MikeyBorg.setSpeed(fullSpeed, turnSpeed)
			#	If just going forward
			else:
				MikeyBorg.setSpeed(fullSpeed, fullSpeed)
		#	If going backwards
		elif self.moveDown:
			#	If also going left
			if self.moveLeft == True and self.moveRight == False:
				MikeyBorg.setSpeed(-fullSpeed, -turnSpeed)
			#	If also going right
			elif self.moveLeft == False and self.moveRight == True:
				MikeyBorg.setSpeed(-turnSpeed, -fullSpeed)
			#	If just going backwards
			else:
				MikeyBorg.setSpeed(-fullSpeed, -fullSpeed)
		#	If going left
		elif self.moveLeft:
			#	Turn left, if not also going right
			if self.moveRight == False:
				MikeyBorg.setSpeed(-fullSpeed, fullSpeed)
		#	If going right
		elif self.moveRight:
			MikeyBorg.setSpeed(fullSpeed, -fullSpeed)
		else:
			MikeyBorg.motorsOff()
		return