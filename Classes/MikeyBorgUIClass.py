#!/usr/bin/env python
# coding: Latin-1
import pygame

#	Set the colours
backgroundColour  = pygame.Color(119, 136, 153)
blackColour       = pygame.Color(0,   0,   0)
boxColour         = pygame.Color(205, 201, 201)
consoleColour     = pygame.Color(0,   0,   0)
noImageColour     = pygame.Color(0,   0,   0)
#	Set the colours for fonts
consoleFontColour = (50, 205, 50)

class MikeyBorgUI:
		
	def __init__(self, screenSize, imageSize, consoleSize):
		self.border          = 5
		self.screenSize      = screenSize
		self.imageSize       = [imageSize[0] * 2, imageSize[1] * 2]
		self.imagePosition   = [(screenSize[0] - self.imageSize[0]) - self.border, 5]
		self.consolePosition = [self.border, self.border]
		self.consoleSize     = [screenSize[0] - self.imageSize[0] - (self.border * 3), self.screenSize[1] - (self.border * 2)]
		self.infoPosition    = [self.imagePosition[0], (self.border * 2) + self.imageSize[1]]
		self.infoSize        = [self.imageSize[0], self.screenSize[1] - self.imageSize[1] - (self.border * 3)]
		self.consoleRows     = consoleSize[1]
		self.consoleLength   = consoleSize[0]
		self.consoleChanged  = False
		self.consoleList     = []
		#	Initialize pygame, and set the page title
		pygame.init()
		pygame.display.set_caption("MikeyBorg")
		#	Create the screen
		self.screen = pygame.display.set_mode(screenSize)
		self.screen.fill(backgroundColour)
		#	Set up the font
		self.font = pygame.font.SysFont("monospace", 15)
		#self.text = self.font.render("Hi", True, (255, 0, 0), (255, 255, 255))
		#	Set up the image, console and info boxes
		self.drawImageBorder()
		self.drawConsole()
		self.drawInfoBox()
		pygame.display.update()
		return
	
	def drawImageBorder(self):
		pygame.draw.rect(self.screen, noImageColour, [self.imagePosition[0],   self.imagePosition[1],   self.imageSize[0],   self.imageSize[1]])
		return
	
	def drawConsole(self):
		pygame.draw.rect(self.screen, consoleColour, [self.consolePosition[0], self.consolePosition[1], self.consoleSize[0], self.consoleSize[1]])
		return
	
	def drawInfoBox(self):
		pygame.draw.rect(self.screen, boxColour,     [self.infoPosition[0],    self.infoPosition[1],    self.infoSize[0],    self.infoSize[1]])
		return

	def _displayConsole(self):
		self.consoleChanged  = False
		textLocation = [self.consolePosition[0] + self.border, self.consolePosition[1] + self.border]
		#	Only show the last x rows
		self.consoleList = self.consoleList[-self.consoleRows:]
		#	Clear the console
		self.drawConsole()
		#	Check the length
		i = 0
		for consoleLine in self.consoleList:
			if len(consoleLine) > self.consoleLength:
				self.consoleList.insert(i + 1, consoleLine[-self.consoleLength:])
				self.consoleList[i] = consoleLine[:self.consoleLength]
			i += 1
		#	Only show the last x rows
		self.consoleList = self.consoleList[-self.consoleRows:]
		#	Output it
		for consoleLine in self.consoleList:
			text = self.font.render(consoleLine, True, consoleFontColour)
			self.screen.blit(text, textLocation)
			textLocation[1] += 20
		return

	def addToConsole(self, add):
		self.consoleList.append(add)
		self._displayConsole()
		return
	
	def addFullWidthToConsole(self, add):
		self.addToConsole(add * self.consoleLength)
		return

	def updateImage(self, image):
		self.screen.blit(image, self.imagePosition)
		pygame.display.update()
		return