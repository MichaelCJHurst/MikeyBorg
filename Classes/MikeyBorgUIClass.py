#!/usr/bin/env python
# coding: Latin-1
import pygame

#	Set the colours
backgroundColour  = pygame.Color(119, 136, 153)
blackColour       = pygame.Color(0,   0,   0)
boxColour         = pygame.Color(0,   0,   0)
noImageColour     = pygame.Color(0,   0,   0)

class MikeyBorgUI:
		
	def __init__(self, screenSize, imageSize):
		self.border          = 5
		self.screenSize      = screenSize
		self.imageSize       = [imageSize[0] * 2, imageSize[1] * 2]
		self.imagePosition   = [(screenSize[0] - self.imageSize[0]) - self.border, 5]
		self.consolePosition = [self.border, self.border]
		self.consoleSize     = [screenSize[0] - self.imageSize[0] - (self.border * 3), self.screenSize[1] - (self.border * 2)]
		self.infoPosition    = [self.imagePosition[0], (self.border * 2) + self.imageSize[1]]
		self.infoSize        = [self.imageSize[0], self.screenSize[1] - self.imageSize[1] - (self.border * 3)]
		#	Initialize pygame, and set the page title
		pygame.init()
		pygame.display.set_caption("MikeyBorg")
		#	Create the screen
		self.screen = pygame.display.set_mode(screenSize)
		self.screen.fill(backgroundColour)
		#	Set up the font
		self.font = pygame.font.SysFont("monospace", 15)
		#	Set up the image, console and info boxes
		pygame.draw.rect(self.screen, noImageColour, [self.imagePosition[0],   self.imagePosition[1],   self.imageSize[0],   self.imageSize[1]])
		pygame.draw.rect(self.screen, boxColour,     [self.consolePosition[0], self.consolePosition[1], self.consoleSize[0], self.consoleSize[1]])
		pygame.draw.rect(self.screen, boxColour,     [self.infoPosition[0],    self.infoPosition[1],    self.infoSize[0],    self.infoSize[1]])
		pygame.display.update()
		return

	def updateImage(self, image):
		self.screen.blit(image, self.imagePosition)
		pygame.display.update()
		return