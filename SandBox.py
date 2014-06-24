#---------------------------------------------------------------------#
import sys
import pygame
import numpy as np
from numpy import *
#---------------------------------------------------------------------#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
#---------------------------------------------------------------------#
class Sand(object):
	def __init__(self):
		self.screen = (800, 600)
		self.firerate = 60
		self.enum = 7
		self.fun = True
		self.report = False
#---------------------------------------------------------------------#
class Enemy(pygame.sprite.Sprite):
	def __init__(self, sandbox, color = WHITE, report = False):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((20, 20))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.live = True
		self.speed = np.array([-1, 0, 1, 2, -2])
		self.bonusx = 0
		self.bonusy = 0
		np.random.shuffle(self.speed)
		self.sandbox = sandbox
		self.rect.x = np.random.randint(0, self.sandbox.screen[0] - 20)
		self.rect.y = np.random.randint(0, self.sandbox.screen[1] - 20)
		self.health = 100.0
		self.report = report
		self.uptime = 0
	def harassment(self, bullet):
		self.health = self.health - bullet.damage + (bullet.speed[0] - self.speed[0]) * 1.5 + (bullet.speed[1] - self.speed[1]) * 1.5
		self.bonusx = bullet.speed[0]
		self.bonusy = bullet.speed[1]
		if self.report: print self.health
		if self.health <= 0:
			self.death()
	def heal(self, health):
		self.health = self.health + health.heal
		if self.report: print self.health
	def death(self):
		self.live = False
		if self.report: print self.live, self.statusreport()
	def fire(self):
		bullet = Bullet(self.sandbox, self.rect.x, self.rect.y)
		return bullet
	def __shuffling_(self):
		np.random.shuffle(self.speed)
		self.bonusx = 0
		self.bonusy = 0
	def __wall__(self):
		if self.rect.x > self.sandbox.screen[0] - 20:
			self.rect.x = self.sandbox.screen[0] - 20
			self.__shuffling_()
		if self.rect.x < 0:
			self.rect.x = 0
			self.__shuffling_()
		if self.rect.y > self.sandbox.screen[1] - 20:
			self.rect.y = self.sandbox.screen[1] - 20
			self.__shuffling_()
		if self.rect.y < 0:
			self.rect.y = 0
			self.__shuffling_()
	def move(self):
		self.rect.x = self.rect.x + self.speed[0] + self.bonusx
		self.rect.y = self.rect.y + self.speed[1] + self.bonusy
		self.uptime = self.uptime + 0.01
		self.__wall__()
	def statusreport(self):
		status = {"class": "blockagent", "x_position": self.rect.x, "y_position": self.rect.y, "x_speed": self.speed[0], "y_speed": self.speed[1], "x_speed_bonus": self.bonusx, "y_speed_bonus": self.bonusy, "health": self.health, "uptime": self.uptime}
		return status
#---------------------------------------------------------------------#
class Health(pygame.sprite.Sprite):
	def __init__(self, sandbox):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5, 5))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.live = True
		self.sandbox = sandbox
		self.rect.x = np.random.randint(0, self.sandbox.screen[0] - 5)
		self.rect.y = np.random.randint(0, self.sandbox.screen[1] - 5)
		self.heal = 5.0
		self.ttl = 500
	def death(self):
		self.live = False
	def move(self):
		self.ttl = self.ttl - 1
		self.heal = self.heal + 0.01
		if self.ttl <= 0:
			self.death()
	def statusreport(self):
		status = {"class": "healthbox", "x_position": self.rect.x, "y_position": self.rect.y, "heal_rate": self.heal, "ttl": self.ttl}
		return status
#---------------------------------------------------------------------#
class Bullet(pygame.sprite.Sprite):
	def __init__(self, sandbox, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5, 5))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.live = True
		self.speed = np.array([-5, 5, 0, 4, -4, 3, -3, 2, -2, 1, -1])
		np.random.shuffle(self.speed)
		self.sandbox = sandbox
		self.rect.x = x + 8
		self.rect.y = y + 8
		self.damage = 10.0 + 6.5 * np.maximum(np.absolute(self.speed[0]), np.absolute(self.speed[1]))
	def death(self):
		self.live = False
	def __wall__(self):
		if self.rect.x > self.sandbox.screen[0] - 5:
			self.rect.x = self.sandbox.screen[0] - 5
			self.death()
		if self.rect.x < 0:
			self.rect.x = 0
			self.death()
		if self.rect.y > self.sandbox.screen[1] - 5:
			self.rect.y = self.sandbox.screen[1] - 5
			self.death()
		if self.rect.y < 0:
			self.rect.y = 0
			self.death()
	def move(self):
		self.rect.x = self.rect.x + self.speed[0]
		self.rect.y = self.rect.y + self.speed[1]
		self.__wall__()
	def statusreport(self):
		status = {"class": "bullet", "x_position": self.rect.x, "y_position": self.rect.y, "x_speed": self.speed[0], "y_speed": self.speed[1], "damage": self.damage}
		return status
#---------------------------------------------------------------------#
class Collision(object):
	@staticmethod
	def test(list, obj, type = "none"):
		for block in list:
			if block.rect.x > obj.rect.x:
				if block.rect.y > obj.rect.y:
					if block.rect.x < obj.rect.x + 20:
						if block.rect.y < obj.rect.y + 20:
							block.death()
							if type == "hit":
								obj.harassment(block)
							elif type == "heal":
								obj.heal(block)
#---------------------------------------------------------------------#
class Agent(object):
	@staticmethod
	def create(sand):
		random = (np.random.randint(10, 255), np.random.randint(10, 255), np.random.randint(10, 255))
		agent = Enemy(sand, random, report = True)
		return agent
#---------------------------------------------------------------------#
class Cleaner(object):
	@staticmethod
	def clean(list):
		for block in list:
			if block.live == False:
				list.remove(block)
#---------------------------------------------------------------------#
class Global(object):
	@staticmethod
	def report(list):
		for block in list:
			print block.statusreport()
#---------------------------------------------------------------------#
pygame.init()
sand = Sand()
window = pygame.display.set_mode((sand.screen[0], sand.screen[1]))
enemy_list = []
bullet_list = []
health_list = []
all_list = pygame.sprite.Group()
for i in xrange(sand.enum):
	block = Enemy(sand)	
	enemy_list.append(block)
	all_list.add(block)
agent = Agent.create(sand)
all_list.add(agent)
clock = pygame.time.Clock()
brain = np.array(range(sand.firerate))
#---------------------------------------------------------------------#
def iteration(data = False):
	global agent
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
	window.fill(BLACK)
	for block in enemy_list:
		np.random.shuffle(brain)
		if brain[0] == 0:
			fire = block.fire()
			bullet_list.append(fire)
			all_list.add(fire)
	np.random.shuffle(brain)
	if brain[0] == 1:
		apt = Health(sand)
		health_list.append(apt)
		all_list.add(apt)
	Collision.test(bullet_list, agent, type = "hit")
	Collision.test(health_list, agent, type = "heal")
	Cleaner.clean(all_list)
	Cleaner.clean(bullet_list)
	Cleaner.clean(health_list)
	if agent.live == False:
		all_list.remove(agent)
		agent = Agent.create(sand)
		all_list.add(agent)
	all_list.draw(window)
	if sand.report: print len(all_list), len(enemy_list), len(bullet_list), len(health_list)
	for block in all_list:
		block.move()
	clock.tick(60)
	pygame.display.update()
	if data:
		return Global.report(all_list)
#---------------------------------------------------------------------#
#iteration(data = True)
#while sand.fun:
#	iteration(data = False)
#---------------------------------------------------------------------#
"""
while sand.fun:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
	window.fill(BLACK)
	for block in enemy_list:
		np.random.shuffle(brain)
		if brain[0] == 0:
			fire = block.fire()
			bullet_list.append(fire)
			all_list.add(fire)
	np.random.shuffle(brain)
	if brain[0] == 1:
		apt = Health(sand)
		health_list.append(apt)
		all_list.add(apt)
	Collision.test(bullet_list, agent, type = "hit")
	Collision.test(health_list, agent, type = "heal")
	Cleaner.clean(all_list)
	Cleaner.clean(bullet_list)
	Cleaner.clean(health_list)
	if agent.live == False:
		all_list.remove(agent)
		agent = Agent.create(sand)
		all_list.add(agent)
	all_list.draw(window)
	if sand.report: print len(all_list), len(enemy_list), len(bullet_list), len(health_list)
	for block in all_list:
		block.move()
	clock.tick(60)
	pygame.display.update()
	#Global.report(all_list)
"""
#---------------------------------------------------------------------#