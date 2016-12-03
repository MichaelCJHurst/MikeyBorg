#!/usr/bin/env python
# coding: Latin-1
import pygame

#	Set the colours
backgroundColour  = pygame.Color(211, 211, 211)
blackColour       = pygame.Color(0, 0, 0)
imageBorderColour = pygame.Color(0, 0, 0)
messageBarColour  = pygame.Color(119, 136, 153)

class MikeyBorgUI:
		
	def __init__(self, screenSize, imageSize):
		self.screenSize = screenSize
		self.imageSize  = imageSize
		self.display    = [imageSize[0] * 2, imageSize[1] * 2]
		self.imageX     = (screenSize[0] - self.display[0]) / 2
		self.imageY     = 20
		#	Initialize pygame, and set the page title
		pygame.init()
		pygame.display.set_caption("MikeyBorg")
		#	Create the screen
		self.screen = pygame.display.set_mode(screenSize)
		self.screen.fill(backgroundColour)
		#	Set up the font
		self.font = pygame.font.SysFont("monospace", 15)
		#	Set up the image box
		pygame.draw.rect(self.screen, imageBorderColour, (self.imageX - 5, self.imageY - 5, self.display[0] + 10, self.display[1] + 10))
		pygame.display.update()
		return

	def updateImage(self, image):
		self.screen.blit(image, [self.imageX, self.imageY])
		pygame.display.update()
		return