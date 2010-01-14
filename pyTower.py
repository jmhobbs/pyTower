# -*- coding: utf-8 -*-

import pygame

import yaml
from os import walk

from multiprocessing import Queue # Should move this stuff to messages?
from Queue import Empty

from time import time

from pytower.constants import *
from pytower import messages
from pytower.menus import Menus
from pytower.window import Window
from pytower.game import Game
from pytower.object import Object
from pytower.map import Map

def quit():
	if None != menus:
		menus.join()
	pygame.quit()
	exit()

def notify_ui():
	tx.put_nowait( messages.Message( messages.NOTIFY_TIME, { 'time': game.clock } ) )
	tx.put_nowait( messages.Message( messages.NOTIFY_CASH, { 'cash': game.cash } ) )
	tx.put_nowait( messages.Message( messages.NOTIFY_POPULATION, { 'population': game.population } ) )

pygame.init()

window = Window()

window.init_loading()
window.set_loading( 'Loading Maps' )

maps = []
maps_min = []

for root, dirs, files in walk( 'maps/' ):
	for file in files:
		if file == 'map.yaml':
			import_path = root.replace( '/', '.' ) + '.map'
			f = open( root + '/' + file )
			map_yaml = yaml.load( f )
			f.close()
			# TODO: Version checking
			map = Map( map_yaml, import_path )
			maps.append( map )
			maps_min.append( map.name )

window.set_loading( 'Spawning Menu' )

tx = Queue()
rx = Queue()

menus = Menus( 'qt', tx, rx )

tx.put_nowait( messages.Message( messages.MAPS, {'maps': maps_min } ) )
menus.main_menu()

game = Game()
map = None

window.set_loading( 'Ready!' )

while True:

	# Only redraw if we have to...
	for event in pygame.event.get():
		if event.type == pygame.VIDEOEXPOSE:
			window.update()
		elif event.type == pygame.QUIT:
			tx.put_nowait( messages.Message( messages.QUIT ) )
			pygame.quit()
			exit()

	try:
		msg = rx.get_nowait()
		print "SDL RX:", msg
		if messages.QUIT == msg.instruction:
			quit()
		elif messages.NEW_GAME == msg.instruction:
			for i in maps:
				if i.name == msg.map:
					game.new_from_map( i )
					map = i
					break
			del maps
			del maps_min
			break
	except Empty:
		pygame.time.delay( IPQUEUE_SLEEP )

window.set_loading( 'Loading Objects' )

objects = []
for root, dirs, files in walk( 'objects/' ):
	for file in files:
		if file == 'object.yaml':
			import_path = root.replace( '/', '.' ) + '.map'
			f = open( root + '/' + file )
			object_yaml = yaml.load( f )
			f.close()
			# TODO: Version checking
			objects.append( Object( object_yaml, import_path ) )

window.set_loading( 'Loading UI' )

tx.put_nowait( messages.Message( messages.OBJECTS, {'objects': objects } ) )

menus.in_game_menu()

frame_remains = TICK_REAL_TIME
paused = False
cursor_object = None
while True:

	frame_start = time()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			tx.put_nowait( messages.Message( messages.QUIT ) )
			quit()

		elif event.type == pygame.MOUSEMOTION:
			window.move_cursor( event.pos )

	# Check with the UI message queue
	try:
		msg = rx.get_nowait()
		print msg
		if messages.QUIT == msg.instruction:
			quit()
		elif messages.PAUSE == msg.instruction:
			paused = True
		elif messages.PLAY == msg.instruction:
			paused = False
		elif messages.SET_CURSOR == msg.instruction:
			#cursor_object = msg.object
			window.set_cursor( msg.cursor )
	except Empty:
		pass

	if not paused:
		frame_end = time()
		frame_remains = frame_remains - ( frame_end - frame_start )
		if 0 >= frame_remains:
			game.clock_tick()
			notify_ui()
			frame_remains = TICK_REAL_TIME

	window.update()

		#elif event.type == MOUSEBUTTONUP:
			#if event.button == 1:
				## Snap to grid
				#pos = ( int( event.pos[0] / Constants.SLICE_WIDTH ) * Constants.SLICE_WIDTH, int( event.pos[1] / Constants.FLOOR_HEIGHT ) * Constants.FLOOR_HEIGHT )
				#f = int( pos[1] / Constants.FLOOR_HEIGHT ) + Globals.v_offset
				#s = int( pos[0] / Constants.SLICE_WIDTH ) + Globals.h_offset
				#if "floor" == cursor_object:
					#if Logic.addFloorSlice( (f,s) ):
						#force_fu = True # TODO: Smaller update?

		#elif event.type == KEYUP:
			#if event.key == pygame.K_q:
				#Globals.q_tx.put_nowait( messages.Message( messages.QUIT ) )
				#quit()
			#elif event.key == pygame.K_DOWN:
					#v_offset = v_offset + 1
			#elif event.key == pygame.K_UP:
				#v_offset = v_offset - 1
			#elif event.key == pygame.K_LEFT:
				#h_offset = h_offset - 1
			#elif event.key == pygame.K_RIGHT:
				#h_offset = h_offset + 1
			#elif event.key == pygame.K_HOME:
				#h_offset = 0
				#v_offset = 0 # TODO: Better numbers



	## Over-adjust corrections...
	#if h_offset + Constants.WINDOW_SLICES > Constants.SLICES:
		#h_offset = Constants.SLICES - Constants.WINDOW_SLICES
	#elif h_offset < 0:
		#h_offset = 0

	#if v_offset + Constants.WINDOW_FLOORS > Constants.FLOORS:
		#v_offset = Constants.FLOORS - Constants.WINDOW_FLOORS
	#elif v_offset < 0:
		#v_offset = 0

	## Only bother to render if it is really a move
	#if force_fu or v_offset != Globals.v_offset or h_offset != Globals.h_offset:
		#Globals.v_offset = v_offset
		#Globals.h_offset = h_offset
		#Render.move()
	#else:
		#Render.dirty_update()

