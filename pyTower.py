# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *

from multiprocessing import Process, Queue

from pytower import Constants
from pytower import Colors
from pytower import Messages
from pytower import Globals
import pytower.QtUi as GUI # Later we can build a GTK+ or other UI and use it too
import pytower.Render as Render

def quit():
	ui.join()
	pygame.quit()
	exit()

pygame.init()

Render.init()

Render.start_loading()
Render.set_loading( 'Loading...' )
# TODO: Load something...
Globals.q_tx = Queue()
Globals.q_rx = Queue()
ui = Process( target=GUI.show_main_menu, args=( Globals.q_tx, Globals.q_rx ) )
ui.start()
Render.set_loading( 'Ready!' )

while True:
	Render.full_update()
	try:
		msg = Globals.q_rx.get_nowait()
		print msg
		if Messages.QUIT == msg.instruction:
			quit()
		elif Messages.NEWGAME == msg.instruction:
			break
	except:
		pygame.time.delay( Constants.IPQUEUE_SLEEP )

Render.initialize_surfaces()
Render.stop_loading()

while True:
	v_offset = Globals.v_offset
	h_offset = Globals.h_offset

	for event in pygame.event.get():
		if event.type == QUIT:
			quit()

		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				# Check if it is in the mini box, move the box if needed.
				if event.pos[0] > 10 and event.pos[0] < ( 10 + Constants.MINI_WIDTH ) and event.pos[1] > 10 and event.pos[1] < ( 10 + Constants.MINI_HEIGHT ):
					h_offset = ( event.pos[0] * Constants.FLOOR_HEIGHT ) - Constants.WINDOW_WIDTH
					v_offset = ( event.pos[1] * Constants.FLOOR_HEIGHT ) - Constants.WINDOW_HEIGHT

		elif event.type == KEYUP:
			if event.key == 113: # q
				ui.terminate()
				quit()
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

	# Only bother to render if it is really a move
	if v_offset != Globals.v_offset or h_offset != Globals.h_offset:
		Globals.v_offset = v_offset
		Globals.h_offset = h_offset
		Render.move()