# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *

from multiprocessing import Process, Queue

from pytower import Constants
from pytower import Colors
from pytower import Messages
import pytower.QtUi as pytower_ui # Later we can build a GTK+ or other UI and use it too

def update_loading_screen ( text, last_rectangle=None ):
	if None != last_rectangle:
		windowSurface.blit( loading, last_rectangle, last_rectangle )
	text = loadingFont.render( text , True, Colors.BLACK )
	textRect = text.get_rect()
	textRect.centerx = windowSurface.get_rect().centerx
	textRect.centery = windowSurface.get_rect().centery
	windowSurface.blit( text, textRect )
	pygame.display.update()
	return textRect

pygame.init()

# set up the window
windowSurface = pygame.display.set_mode( ( Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ), 0, 32 )
pygame.display.set_caption( 'pyTower - v' + Constants.VERSION  )

# Set up font for loading...
loadingFont = pygame.font.SysFont( None, 48 )

# Show the loading image. TODO: Actually load something.
loading = pygame.image.load( 'resources/loading.bmp' ).convert()
windowSurface.blit( loading, ( 0, 0 ) )

last_loading_rectangle = update_loading_screen( 'Building surfaces...' )
pygame.time.delay( 500 )

# Viewport offsets
h_offset = Constants.CENTER
v_offset = Constants.BOTTOM - ( Constants.FLOOR_HEIGHT * 5 )

# This is the whole game surface
fullSurface = pygame.Surface( ( Constants.GAME_WIDTH, Constants.GAME_HEIGHT ) )

# TODO: Replace with a real startup routine that draws nice dirt & sky :-/
fullSurface.fill( Colors.SKY_BLUE )
drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - ( Constants.FLOOR_HEIGHT * 10 ), fullSurface.get_rect().width, ( Constants.FLOOR_HEIGHT * 5 ) )
pygame.draw.rect( fullSurface, Colors.LIGHT_BROWN, drawrect )
drawrect = ( fullSurface.get_rect().left, fullSurface.get_rect().bottom - ( Constants.FLOOR_HEIGHT * 5 ), fullSurface.get_rect().width, ( Constants.FLOOR_HEIGHT * 5 ) )
pygame.draw.rect( fullSurface, Colors.DARK_BROWN, drawrect )

last_loading_rectangle = update_loading_screen( 'Cloning mini model...' , last_loading_rectangle )
pygame.time.delay( 500 )

# This is a representative surface used as a "map"
miniSurface = pygame.Surface( ( Constants.MINI_WIDTH, Constants.MINI_HEIGHT ) )
miniSurface.set_alpha( 200 )
miniSurface.fill( Colors.SKY_BLUE )
drawrect = ( miniSurface.get_rect().left, miniSurface.get_rect().bottom - ( 10 ), miniSurface.get_rect().width, ( 10 ) )
pygame.draw.rect( miniSurface, Colors.LIGHT_BROWN, drawrect )

last_loading_rectangle = update_loading_screen( 'Making you wait...' , last_loading_rectangle )
pygame.time.delay( 500 )

last_loading_rectangle = update_loading_screen( 'Ready!' , last_loading_rectangle )
pygame.display.update()
del loading # Cleanup

ui_send_q = Queue()
ui_recieve_q = Queue()
ui = Process( target=pytower_ui.show_main_menu, args=( ui_send_q, ui_recieve_q ) )
ui.start()

while True:
	pygame.display.update()
	try:
		msg = ui_recieve_q.get_nowait()
		print msg
		if Messages.QUIT == msg.instruction:
			ui.join()
			pygame.quit()
			exit()
		elif Messages.NEWGAME == msg.instruction:
			break
	except:
		pygame.time.delay( Constants.IPQUEUE_SLEEP )

# Now blit the starting, blank surface on
windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ) )
pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				# Check if it is in the mini box, move the box if needed.
				if event.pos[0] > 10 and event.pos[0] < ( 10 + Constants.MINI_WIDTH ) and event.pos[1] > 10 and event.pos[1] < ( 10 + Constants.MINI_HEIGHT ):
					h_offset = ( event.pos[0] * Constants.FLOOR_HEIGHT ) - Constants.WINDOW_WIDTH
					v_offset = ( event.pos[1] * Constants.FLOOR_HEIGHT ) - Constants.WINDOW_HEIGHT

		elif event.type == KEYUP:
			#print "Keypress:", event.key
			if event.key == 113: # q
				ui.terminate() # TODO: Be nicer. Try a queue event & join or something.
				pygame.quit()
				sys.exit()
			elif event.key == 274: # Down
					v_offset = v_offset + Constants.FLOOR_HEIGHT
			elif event.key == 273: # Up
				v_offset = v_offset - Constants.FLOOR_HEIGHT
			elif event.key == 276 and h_offset: # Right
				h_offset = h_offset - Constants.FLOOR_HEIGHT
			elif event.key == 275: # Left
				h_offset = h_offset + Constants.FLOOR_HEIGHT
			elif event.key == 278: # Home
				h_offset = Constants.CENTER
				v_offset = Constants.BOTTOM

	# Over-adjust corrections...
	if ( h_offset + Constants.WINDOW_WIDTH ) > Constants.GAME_WIDTH:
		h_offset = Constants.GAME_WIDTH - Constants.WINDOW_WIDTH
	elif h_offset < 0:
		h_offset = 0

	if ( v_offset + Constants.WINDOW_HEIGHT ) > Constants.GAME_HEIGHT:
		v_offset = Constants.GAME_HEIGHT - Constants.WINDOW_HEIGHT
	elif v_offset < 0:
		v_offset = 0

	windowSurface.blit( fullSurface, ( 0, 0 ), ( 0 + h_offset, 0 + v_offset, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ) )

	drawrect = ( 9, 9, Constants.MINI_WIDTH + 2, Constants.MINI_HEIGHT + 2 )
	pygame.draw.rect( windowSurface, Colors.BLACK, drawrect )

	windowSurface.blit( miniSurface, ( 10, 10 ), ( 0, 0, Constants.MINI_WIDTH, Constants.MINI_HEIGHT ) )

	drawrect = ( 10 + ( h_offset / Constants.FLOOR_HEIGHT ), 10 + ( v_offset / Constants.FLOOR_HEIGHT ), ( Constants.WINDOW_WIDTH / Constants.FLOOR_HEIGHT ), ( Constants.WINDOW_HEIGHT / Constants.FLOOR_HEIGHT ) )
	pygame.draw.rect( windowSurface, Colors.BLACK, drawrect )

	pygame.display.update()