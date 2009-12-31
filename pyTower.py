# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *

from multiprocessing import Process, Queue

from pytower import constants
from pytower import colors
import pytower.qtui as pytower_ui # Later we can build a GTK+ or other UI and use it too

def update_loading_screen ( text, last_rectangle=None ):
	if None != last_rectangle:
		windowSurface.blit( loading, last_rectangle, last_rectangle )
	text = loadingFont.render( text , True, colors.BLACK )
	textRect = text.get_rect()
	textRect.centerx = windowSurface.get_rect().centerx
	textRect.centery = windowSurface.get_rect().centery
	windowSurface.blit( text, textRect )
	pygame.display.update()
	return textRect

pygame.init()

# set up the window
windowSurface = pygame.display.set_mode( ( constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT ), 0, 32 )
pygame.display.set_caption( 'pyTower - v' + constants.VERSION  )

# Set up font for loading...
loadingFont = pygame.font.SysFont( None, 48 )

# Show the loading image. TODO: Actually load something.
loading = pygame.image.load( 'resources/loading.bmp' ).convert()
windowSurface.blit( loading, ( 0, 0 ) )

last_loading_rectangle = update_loading_screen( 'Building surfaces...' )
pygame.time.delay( 500 )

# Viewport offsets
h_offset = constants.CENTER
v_offset = constants.BOTTOM - ( constants.FLOOR_HEIGHT * 5 )

# This is the whole game surface
fullSurface = pygame.Surface( ( constants.GAME_WIDTH, constants.GAME_HEIGHT ) )

# TODO: Replace with a real startup routine that draws nice dirt & sky :-/
fullSurface.fill( colors.SKY_BLUE )
drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - ( constants.FLOOR_HEIGHT * 10 ), fullSurface.get_rect().width, ( constants.FLOOR_HEIGHT * 5 ) )
pygame.draw.rect( fullSurface, colors.LIGHT_BROWN, drawrect )
drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - ( constants.FLOOR_HEIGHT * 5 ), fullSurface.get_rect().width, ( constants.FLOOR_HEIGHT * 5 ) )
pygame.draw.rect( fullSurface, colors.DARK_BROWN, drawrect )

last_loading_rectangle = update_loading_screen( 'Cloning mini model...' , last_loading_rectangle )
pygame.time.delay( 500 )

# This is a representative surface used as a "map"
miniSurface = pygame.Surface( ( constants.MINI_WIDTH, constants.MINI_HEIGHT ) )
miniSurface.set_alpha( 200 )
miniSurface.fill( colors.SKY_BLUE )
drawrect = ( miniSurface.get_rect().left, miniSurface.get_rect().bottom - ( 10 ), miniSurface.get_rect().width, ( 10 ) )
pygame.draw.rect( miniSurface, colors.LIGHT_BROWN, drawrect )

last_loading_rectangle = update_loading_screen( 'Making you wait...' , last_loading_rectangle )
pygame.time.delay( 500 )

last_loading_rectangle = update_loading_screen( 'Ready!' , last_loading_rectangle )
pygame.display.update()
del loading # Cleanup

ui_send_q = Queue()
ui_recieve_q = Queue()
ui = Process( target=pytower_ui.show_main_menu, args=( ui_send_q, ui_recieve_q ) )
ui.start()

pygame.time.delay( 500 )
ui_send_q.put_nowait( "Test" )

while True:
	pygame.display.update()
	try:
		instruction = ui_recieve_q.get_nowait()
		ui.terminate() # TODO: Be nicer. Try a queue event & join or something.
		ui.join()
		pygame.quit()
		sys.exit()
	except:
		pygame.time.delay( constants.IPQUEUE_SLEEP )

# Now blit the starting, blank surface on
windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT ) )
pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				# Check if it is in the mini box, move the box if needed.
				if event.pos[0] > 10 and event.pos[0] < ( 10 + constants.MINI_WIDTH ) and event.pos[1] > 10 and event.pos[1] < ( 10 + constants.MINI_HEIGHT ):
					h_offset = ( event.pos[0] * constants.FLOOR_HEIGHT ) - constants.WINDOW_WIDTH
					v_offset = ( event.pos[1] * constants.FLOOR_HEIGHT ) - constants.WINDOW_HEIGHT

		elif event.type == KEYUP:
			#print "Keypress:", event.key
			if event.key == 113: # q
				ui.terminate() # TODO: Be nicer. Try a queue event & join or something.
				pygame.quit()
				sys.exit()
			elif event.key == 274: # Down
					v_offset = v_offset + constants.FLOOR_HEIGHT
			elif event.key == 273: # Up
				v_offset = v_offset - constants.FLOOR_HEIGHT
			elif event.key == 276 and h_offset: # Right
				h_offset = h_offset - constants.FLOOR_HEIGHT
			elif event.key == 275: # Left
				h_offset = h_offset + constants.FLOOR_HEIGHT
			elif event.key == 278: # Home
				h_offset = constants.CENTER
				v_offset = constants.BOTTOM

	# Over-adjust corrections...
	if ( h_offset + constants.WINDOW_WIDTH ) > constants.GAME_WIDTH:
		h_offset = constants.GAME_WIDTH - constants.WINDOW_WIDTH
	elif h_offset < 0:
		h_offset = 0

	if ( v_offset + constants.WINDOW_HEIGHT ) > constants.GAME_HEIGHT:
		v_offset = constants.GAME_HEIGHT - constants.WINDOW_HEIGHT
	elif v_offset < 0:
		v_offset = 0

	windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT ) )

	drawrect = ( 9, 9, constants.MINI_WIDTH + 2, constants.MINI_HEIGHT + 2 )
	pygame.draw.rect( windowSurface, colors.BLACK, drawrect )

	windowSurface.blit( miniSurface, ( 10, 10 ), ( 0, 0, constants.MINI_WIDTH, constants.MINI_HEIGHT ) )

	drawrect = ( 10 + ( h_offset / constants.FLOOR_HEIGHT ), 10 + ( v_offset / constants.FLOOR_HEIGHT ), ( constants.WINDOW_WIDTH / constants.FLOOR_HEIGHT ), ( constants.WINDOW_HEIGHT / constants.FLOOR_HEIGHT ) )
	pygame.draw.rect( windowSurface, colors.BLACK, drawrect )

	pygame.display.update()