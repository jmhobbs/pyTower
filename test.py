# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *

pygame.init()

# Dimensions
FLOOR_HEIGHT = 40
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_HEIGHT = 110 * FLOOR_HEIGHT
GAME_WIDTH = 75 * FLOOR_HEIGHT
GAME_RATIO = GAME_HEIGHT / GAME_WIDTH
BOTTOM = GAME_HEIGHT - WINDOW_HEIGHT
CENTER = ( GAME_WIDTH - WINDOW_WIDTH ) / 2
MINI_WIDTH = GAME_WIDTH / FLOOR_HEIGHT
MINI_HEIGHT = GAME_HEIGHT / FLOOR_HEIGHT

print "Game Height:", GAME_HEIGHT
print "Game Width:", GAME_WIDTH

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
v_offset = BOTTOM - ( FLOOR_HEIGHT * 5 ) # We don't want absolute bottom, this is 5 floors up.

fullSurface = pygame.Surface( ( GAME_WIDTH, GAME_HEIGHT ) )
fullSurface.fill( SKY_BLUE )

drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - ( FLOOR_HEIGHT * 10 ), fullSurface.get_rect().width, ( FLOOR_HEIGHT * 5 ) )
pygame.draw.rect( fullSurface, LIGHT_BROWN, drawrect )
drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - ( FLOOR_HEIGHT * 5 ), fullSurface.get_rect().width, ( FLOOR_HEIGHT * 5 ) )
pygame.draw.rect( fullSurface, DARK_BROWN, drawrect )

miniSurface = pygame.Surface( ( MINI_WIDTH, MINI_HEIGHT ) )
miniSurface.fill( SKY_BLUE )
drawrect = ( miniSurface.get_rect().left, miniSurface.get_rect().bottom - ( 10 ), miniSurface.get_rect().width, ( 5 ) )
pygame.draw.rect( miniSurface, LIGHT_BROWN, drawrect )
drawrect = ( miniSurface.get_rect().left, miniSurface.get_rect().bottom - ( 5 ), miniSurface.get_rect().width, ( 5 ) )
pygame.draw.rect( miniSurface, DARK_BROWN, drawrect )


windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, WINDOW_WIDTH, WINDOW_HEIGHT ) )

pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				# Check if it is in the mini box
				if event.pos[0] > 10 and event.pos[0] < ( 10 + MINI_WIDTH ) and event.pos[1] > 10 and event.pos[1] < ( 10 + MINI_HEIGHT ):
					h_offset = ( event.pos[0] * FLOOR_HEIGHT ) - WINDOW_WIDTH
					v_offset = ( event.pos[1] * FLOOR_HEIGHT ) - WINDOW_HEIGHT

		elif event.type == KEYUP:
			#print "Keypress:", event.key
			if event.key == 113: # q
				pygame.quit()
				sys.exit()
			elif event.key == 274: # Down
					v_offset = v_offset + FLOOR_HEIGHT
			elif event.key == 273: # Up
				v_offset = v_offset - FLOOR_HEIGHT
			elif event.key == 276 and h_offset: # Right
				h_offset = h_offset - FLOOR_HEIGHT
			elif event.key == 275: # Left
				h_offset = h_offset + FLOOR_HEIGHT
			elif event.key == 278: # Home
				h_offset = CENTER
				v_offset = BOTTOM

	# Over-adjust corrections...
	if ( h_offset + WINDOW_WIDTH ) > GAME_WIDTH:
		h_offset = GAME_WIDTH - WINDOW_WIDTH
	elif h_offset < 0:
		h_offset = 0

	if ( v_offset + WINDOW_HEIGHT ) > GAME_HEIGHT:
		v_offset = GAME_HEIGHT - WINDOW_HEIGHT
	elif v_offset < 0:
		v_offset = 0

	windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, WINDOW_WIDTH, WINDOW_HEIGHT ) )

	drawrect = ( 9, 9, MINI_WIDTH + 2, MINI_HEIGHT + 2 )
	pygame.draw.rect( windowSurface, BLACK, drawrect )

	windowSurface.blit( miniSurface, ( 10, 10 ), ( 0, 0, MINI_WIDTH, MINI_HEIGHT ) )

	drawrect = ( 10 + ( h_offset / FLOOR_HEIGHT ), 10 + ( v_offset / FLOOR_HEIGHT ), ( WINDOW_WIDTH / FLOOR_HEIGHT ), ( WINDOW_HEIGHT / FLOOR_HEIGHT ) )
	pygame.draw.rect( windowSurface, BLACK, drawrect )

	pygame.display.update()