#!/usr/bin/env python
# coding: Latin-1
import pygame
import pygame.camera

class MikeyCam:
		
	def __init__(self, screen, imageSize, imagePosition, displaySize):
		self.screen        = screen
		self.imageSize     = imageSize
		self.imagePosition = imagePosition
		self.displaySize   = displaySize
		self.takePicture   = False
		self.imagePath     = "SavedImages/"

		pygame.camera.init()
		self.cam = pygame.camera.Camera("/dev/video0", imageSize, "RGM")
		self.cam.start()
		self._getImage()
		pygame.display.update()
		print("Camera Initialised")

	def loop(self, close):
		try:
			while True:
				self._getImage()
				if close.value == 1:
					break
			self.cam.stop()
			print("Camera Stopped")
		except KeyboardInterrupt:
			self.cam.stop()
			print("Camera Killed")

	def _getImage(self):
		image = self.cam.get_image()
		image = pygame.transform.scale(image, self.displaySize)
		self.screen.blit(image, self.imagePosition)
		pygame.display.update()
		return