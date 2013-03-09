import pygame

class Block(pygame.Rect):
	def __init__(self, X, Y, blockWidth, blockHeight, color, alpha):
		self.left = X
		self.top = Y
		self.width = blockWidth
		self.height = blockHeight
		self.surf = pygame.Surface((blockWidth, blockHeight))
		self.surf.set_alpha(alpha)
		self.surf.fill(color)
		
	def changeColor(self, color, alpha):
		self.surf.set_alpha(alpha)
		self.surf.fill(color)
