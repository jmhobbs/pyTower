# -*- coding: utf-8 -*-
import pygame
import time

pygame.init()
pygame.display.set_mode( ( 100,100 ), 0, 32 ) # 6.1M

f = True
while f:
	for event in pygame.event.get():
		if event.type == pygame.KEYUP and event.key == pygame.K_UP:
			f = False
			break

print "load jpg"

x = pygame.image.load( 'maps/default/day.jpg' ) # 25.1 M

f = True
while f:
	for event in pygame.event.get():
		if event.type == pygame.KEYUP and event.key == pygame.K_UP:
			f = False
			break

print "convert"

x = x.convert() # 31.4 M

f = True
while f:
	for event in pygame.event.get():
		if event.type == pygame.KEYUP and event.key == pygame.K_UP:
			f = False
			break

pygame.quit()
exit()