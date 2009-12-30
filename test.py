# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode( ( 500, 400 ), 0, 32 )
pygame.display.set_caption('Hello world!')

# set up the colors
BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
LTBRN = ( 143, 106, 50 )
DKBRN = ( 87, 63, 30 )
SKYBLU = ( 128, 181, 255 )
NIGHTSKYBLUE = ( 0, 49, 110 )

# draw the white background onto the surface
windowSurface.fill( SKYBLU )

# draw the dirt onto the surface
drawrect = ( windowSurface.get_rect().left, windowSurface.get_rect().bottom - 100, windowSurface.get_rect().width, 100  )
pygame.draw.rect( windowSurface, LTBRN, drawrect )
drawrect = ( windowSurface.get_rect().left, windowSurface.get_rect().bottom - 50, windowSurface.get_rect().width, 50  )
pygame.draw.rect( windowSurface, DKBRN, drawrect )

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
		for event in pygame.event.get():
				if event.type == QUIT:
						pygame.quit()
						sys.exit()
