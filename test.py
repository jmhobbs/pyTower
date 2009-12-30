# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *

pygame.init()

# Dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_WIDTH = 3000 # Up to 100 single hotel rooms wide
GAME_HEIGHT = 5250 # 150 Floors @ 35px each
BOTTOM = GAME_HEIGHT - WINDOW_HEIGHT
CENTER = ( GAME_WIDTH - WINDOW_WIDTH ) / 2
# set up the colors
BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
LIGHT_BROWN = ( 143, 106, 50 )
DARK_BROWN = ( 87, 63, 30 )
SKY_BLUE = ( 128, 181, 255 )
NIGHT_SKY_BLUE = ( 0, 49, 110 )

# set up the window
windowSurface = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ), 0, 32 )
pygame.display.set_caption( 'pyTower Testing Ground' )

h_offset = CENTER
v_offset = BOTTOM - 175 # We don't want absolute bottom, this is 5 floors up.

fullSurface = pygame.Surface( ( GAME_WIDTH, GAME_HEIGHT ) )
fullSurface.fill( SKY_BLUE )

drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - 350, fullSurface.get_rect().width, 175 )
pygame.draw.rect( fullSurface, LIGHT_BROWN, drawrect )
drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - 175, fullSurface.get_rect().width, 175 )
pygame.draw.rect( fullSurface, DARK_BROWN, drawrect )

windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, WINDOW_WIDTH, WINDOW_HEIGHT ) )
pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYUP:
			print "Keypress:", event.key
			if event.key == 113: # q
				pygame.quit()
				sys.exit()
			elif event.key == 274: # Down
				v_offset = v_offset + 35
			elif event.key == 273: # Up
				v_offset = v_offset - 35
			elif event.key == 276: # Right
				h_offset = h_offset + 35
			elif event.key == 275: # Left
				h_offset = h_offset - 35
			elif event.key == 278: # Home
				h_offset = CENTER
				v_offset = BOTTOM
	windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, WINDOW_WIDTH, WINDOW_HEIGHT ) )
	pygame.display.update()