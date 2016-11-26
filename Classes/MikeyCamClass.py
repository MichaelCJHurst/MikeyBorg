#!/usr/bin/env python
# coding: Latin-1
import pygame
import pygame.camera

class MikeyCam:
		
	def __init__(self, imageSize):
		self.isActive = False

		pygame.camera.init()
		self.cam = pygame.camera.Camera("/dev/video0", imageSize, "RGM")
		self.start()

	def getImage(self, imageSize):
		image = self.cam.get_image()
		image = pygame.transform.scale(image, imageSize)
		return image
	
	def toggle(self):
		if self.isActive:
			self.stop()
		else:
			self.start()
		return
	
	def start(self):
		if not self.isActive:
			self.cam.start()
			self.isActive = True
		return
	
	def stop(self):
		if self.isActive:
			self.cam.stop()
			self.isActive = False
		return