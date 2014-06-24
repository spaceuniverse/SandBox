#---------------------------------------------------------------------#
import sys
import pygame
import numpy as np
from numpy import *
#---------------------------------------------------------------------#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RANDOM = (np.random.randint(10, 255), np.random.randint(10, 255), np.random.randint(10, 255))
#---------------------------------------------------------------------#
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((20, 20))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.live = True
		self.speed = np.array([-1, 0, 1, 2, -2])
		np.random.shuffle(self.speed)
		self.rect.x = np.random.randint(0, 800 - 20)
		self.rect.y = np.random.randint(0, 600 - 20)
	def death(self):
		self.live = False
	def fire(self):
		pass
	def move(self):		
		self.rect.x = self.rect.x + self.speed[0]
		self.rect.y = self.rect.y + self.speed[1]
		if self.rect.x > 800 - 20:
			self.rect.x = 800 - 20
			np.random.shuffle(self.speed)
		if self.rect.x < 0:
			self.rect.x = 0
			np.random.shuffle(self.speed)
		if self.rect.y > 600 - 20:
			self.rect.y = 600 - 20
			np.random.shuffle(self.speed)
		if self.rect.y < 0:
			self.rect.y = 0
			np.random.shuffle(self.speed)
#---------------------------------------------------------------------#
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5, 5))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.live = True
	def death(self):
		self.live = False
#---------------------------------------------------------------------#
pygame.init()
window = pygame.display.set_mode((800, 600))
enemy_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
all_list = pygame.sprite.Group()
for i in xrange(5):
	block = Enemy()	
	enemy_list.add(block)
	all_list.add(block)
clock = pygame.time.Clock()
#score = 0
#---------------------------------------------------------------------#
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
	window.fill(BLACK)
	#hit_list = pygame.sprite.spritecollide(player, block_list, True)
	#for block in blocks_hit_list:
	#	score += 1
	#	print score
	all_list.draw(window)
	for block in all_list:
		block.move()
	clock.tick(60)
	pygame.display.flip()
#---------------------------------------------------------------------#
"""
while True:
	for event in pygame.event.get():
		window.fill(BLACK)
		#player_position = pygame.mouse.get_pos()
		#x = player_position[0]
		#y = player_position[1]
		#player.rect.x = x
		#player.rect.y = y
		#blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
		#for block in blocks_hit_list:
		#	score += 1
		#	print score
		all_sprites_list.draw(window)
		for block in all_sprites_list:
			block.move()
		#box = pygame.Rect(x, y, 100, 100)
		#pygame.draw.rect(window, (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)), box, 0)
		#pygame.draw.line(window, (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)), (0, 0), (x, y))
		clock.tick(60)
		pygame.display.flip()
		#pygame.display.update()
		if event.type == pygame.QUIT:
			sys.exit(0)
		else:
			print event
"""
#---------------------------------------------------------------------#