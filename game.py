import pygame
import random
from test1 import *

class Game:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((800,600))
		pygame.display.set_caption("test")
		self.clock = pygame.time.Clock()
		self.running = True

	def getRunning(self):
		return self.running

	def new(self):
		self.all_sprites = pygame.sprite.Group()
		self.player = Player(200,200)
		self.all_sprites.add(self.player)
		self.run()

	def run(self):
		self.playing = True
		while self.playing:
			self.clock.tick(50)
			self.events()
			self.update()
			self.draw()

	def update(self):
		self.all_sprites.update()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.player.jumpCheck()
					self.player.jump()

	def draw(self):
		self.screen.fill((0,0,0))
		self.all_sprites.draw(self.screen)
		pygame.display.flip()

g = Game()
while g.getRunning():
	g.new()
pygame.quit()



	