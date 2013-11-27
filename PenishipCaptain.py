#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PenishipCaptain.py
#  
#  Copyright 2013 JerryMrSlime <JerryMrSlime@JERRYMRSLIME-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import pygame as py

from pygame.locals import *
from random import randrange


class Player(object):
	def __init__(self):
		#Render vars
		self.images = []
		self.loadImages()
		#Timer vars
		self.currentFrame = 0
		self.elapsedTime = 0
		self.delay = 100
		#Movement vars
		self.x, self.y = 0, 0
		self.vx, self.vy = 0, 0
		self.width = self.images[0].get_width
		self.height = self.images[0].get_height
		self.speed = 5
		self.friction = 0.6
		self.rect = Rectangle(self.x, self.y, self.width, self.height)
		#Shot vars
		self.bullets = []
		self.shot = True
		
	def Update(self):
		self.updateAnimation()
		self.Controls()
		self.movementUpdate()
		self.rect.Update(self.x, self.y)
		self.updateBullets()
		
	def Render(self, screen):
		screen.blit(self.images[self.currentFrame], (self.x, self.y))
		self.renderBullets(screen)
	
	def updateBullets(self):
		for bullet in self.bullets:
			bullet.Update()
			if bullet.death:
				self.bullets.remove(bullet)
			
	def renderBullets(self, screen):
		for bullet in self.bullets:
			bullet.Render(screen)
			
	def Controls(self):
		key = py.key.get_pressed()
		if key[K_UP]:
			self.vy = -self.speed
		elif key[K_DOWN]:
			self.vy = self.speed
		else:
			self.vy = 0
		if key[K_RIGHT]:
			self.vx = self.speed
		elif key[K_LEFT]:
			self.vx = -self.speed
		else:
			self.vx = 0
		if key[K_SPACE] and self.shot:
			self.bullets.append(Bullet(self.x, self.y, self.bullet_img))
			
	def movementUpdate(self):
		self.vx = self.vx * self.friction
		self.vy = self.vy * self.friction
		self.x += self.vx
		self.y += self.vy
		
	def updateAnimation(self):
		if py.time.get_ticks() - self.elapsedTime > self.delay:
			self.elapsedTime = py.time.get_ticks()
			self.currentFrame += 1
			if self.currentFrame > 1:
				self.currentFrame = 0
	
	def loadImages(self):
		for i in range (1, 3):
			self.images.append(py.image.load("resources/graphics/player_"+str(i)+".png").convert_alpha())
		self.bullet_img = py.image.load("resources/graphics/ball.png").convert_alpha()

class Bullet(object):
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.width = self.img.get_width()
		self.height = self.img.get_height()
		self.rect = Rectangle(self.x, self.y, self.width, self.height)
		self.death = False
		self.speed = 5
		
	def Update(self):
		self.rect.Update(self.x, self.y)
		self.x += self.speed
		self.setBounds()
	
	def setBounds(self):
		if self.x > 800 or self.x < 0 or self.y > 600 or self.y < 0:
			self.death = True
			print "Bullet destroyed"
			
	def Render(self, screen):
		screen.blit(self.img, (self.x, self.y))
		
class Collision(object):
	def Update(self, r1, r2):
		if (r1.x > r2.width + r2.x or
		r1.y > r2.height + r2.y or
		r1.x + r1.width < r2.x or
		r1.y + r1.height < r2.y):
			return False
		else:
			return True
		
class Rectangle(object):
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
	def Update(self, x, y):
		self.x = x
		self.y = y
		
def main():
	py.init()
	screen = py.display.set_mode((800, 600))
	py.display.set_caption("PenishipCaptain")
	
	clear = (135, 206, 250)
	clock = py.time.Clock()
	exit = False
	
	player = Player()
	
	while not exit:
		screen.fill(clear)
		for event in py.event.get():
			if event.type == QUIT:
				exit = True
				
		player.Render(screen)
		player.Update()
		py.display.update()
		clock.tick(60)
	return 0

if __name__ == '__main__':
	main()

