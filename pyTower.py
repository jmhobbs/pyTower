# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *

import yaml
from os import walk

from multiprocessing import Process, Queue
from Queue import Empty

from time import time

from pytower import Constants
from pytower import Colors
from pytower import Messages
from pytower import Globals
import pytower.QtUi as GUI
import pytower.Render as Render

def quit():
	ui.join()
	pygame.quit()
	exit()

def notify_ui():
	m = Messages.Message( Messages.NOTIFY_TIME )
	m.time = Globals.game_clock
	Globals.q_tx.put_nowait( m )
	m = Messages.Message( Messages.NOTIFY_CASH )
	m.cash = Globals.cash
	Globals.q_tx.put_nowait( m )
	m = Messages.Message( Messages.NOTIFY_POPULATION )
	m.population = Globals.population
	Globals.q_tx.put_nowait( m )

def increment_game_clock():
	Globals.game_clock[4] = Globals.game_clock[4] + 5
	if Globals.game_clock[4] >= 60:
		Globals.game_clock[4] = 0
		Globals.game_clock[3] = Globals.game_clock[3] + 1
		if Globals.game_clock[3] > 24:
			Globals.game_clock[3] = 1
			Globals.game_clock[2] = Globals.game_clock[2] + 1
			if Globals.game_clock[2] > 6:
				Globals.game_clock[2] = 1
				Globals.game_clock[1] = Globals.game_clock[1] + 1
				if Globals.game_clock[1] > 12:
					Globals.game_clock[1] = 1
					Globals.game_clock[0] = Globals.game_clock[0] + 1

pygame.init()

Render.init()

Render.start_loading()
Render.set_loading( 'Loading Objects' )

for root, dirs, files in walk( 'objects/' ):
	for file in files:
		if file == 'object.yaml':
			f = open( root + '/' + file )
			dm = yaml.load( f )
			f.close()
			Globals.objects[0].append( dm )
			print dm['object']['name']

Render.set_loading( 'Spawning Menu' )

Globals.q_tx = Queue()
Globals.q_rx = Queue()
ui = Process( target=GUI.show_main_menu, args=( Globals.q_tx, Globals.q_rx ) )
ui.start()

Render.set_loading( 'Ready!' )

while True:

	# Only redraw if we have to...
	for event in pygame.event.get():
		if event.type == VIDEOEXPOSE:
			Render.full_update()

	try:
		msg = Globals.q_rx.get_nowait()
		print msg
		if Messages.QUIT == msg.instruction:
			quit()
		elif Messages.NEW_GAME == msg.instruction:
			Globals.cash = 500000
			Globals.game_clock = [ 1, 1, 1, 0, 0 ]
			Globals.population = 0
			break
	except Empty:
		pygame.time.delay( Constants.IPQUEUE_SLEEP )

Render.initialize_surfaces()

notify_ui()

ui = Process( target=GUI.show_in_game_menu, args=( Globals.q_tx, Globals.q_rx ) )
ui.start()

Render.stop_loading()

frame_remains = Constants.FRAME_LENGTH
paused = False
while True:

	frame_start = time()

	v_offset = Globals.v_offset
	h_offset = Globals.h_offset
	force_fu = False

	for event in pygame.event.get():
		if event.type == QUIT:
			quit()

		if event.type == VIDEOEXPOSE:
			force_fu = True

		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				# Check if it is in the mini box, move the box if needed.
				if event.pos[0] > 10 and event.pos[0] < ( 10 + Constants.MINI_WIDTH ) and event.pos[1] > 10 and event.pos[1] < ( 10 + Constants.MINI_HEIGHT ):
					h_offset = ( event.pos[0] * Constants.FLOOR_HEIGHT ) - Constants.WINDOW_WIDTH
					v_offset = ( event.pos[1] * Constants.FLOOR_HEIGHT ) - Constants.WINDOW_HEIGHT

		elif event.type == KEYUP:
			if event.key == pygame.K_q: # q
				ui.terminate()
				quit()
			elif event.key == pygame.K_DOWN:
					v_offset = v_offset + Constants.FLOOR_HEIGHT
			elif event.key == pygame.K_UP:
				v_offset = v_offset - Constants.FLOOR_HEIGHT
			elif event.key == pygame.K_LEFT and h_offset:
				h_offset = h_offset - Constants.FLOOR_HEIGHT
			elif event.key == pygame.K_RIGHT:
				h_offset = h_offset + Constants.FLOOR_HEIGHT
			elif event.key == pygame.K_HOME:
				h_offset = Constants.CENTER
				v_offset = Constants.BOTTOM

	# Check with the UI message queue
	try:
		msg = Globals.q_rx.get_nowait()
		print msg
		if Messages.QUIT == msg.instruction:
			quit()
		elif Messages.PAUSE == msg.instruction:
			paused = True
		elif Messages.PLAY == msg.instruction:
			paused = False
	except Empty:
		pass

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
	if force_fu or v_offset != Globals.v_offset or h_offset != Globals.h_offset:
		Globals.v_offset = v_offset
		Globals.h_offset = h_offset
		Render.move()

	# Run the clock!
	if not paused:
		frame_end = time()
		frame_remains = frame_remains - ( frame_end - frame_start )
		if 0 >= frame_remains:
			increment_game_clock()
			notify_ui()
			frame_remains = Constants.FRAME_LENGTH