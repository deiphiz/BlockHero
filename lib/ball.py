import pygame

class Ball(pygame.Rect):
	def __init__(self, X, Y, size, color, dir = (0, 0)):
		self.left = X
		self.top = Y
		self.width = size
		self.height = size
		self.color = color
		self.dirX = dir[0]
		self.dirY = dir[1]
