import pygame

class Player(pygame.Rect):
	def __init__(self, X, Y, width, height, accel = 0, speed = 0):
		self.left = X
		self.top = Y
		self.width = width
		self.height = height
		self.accel = accel
		self.speed = speed