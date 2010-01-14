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
from pytower.utility import FullPath
from pytower import logic

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
			map = Map( map_yaml, import_path, FullPath( root ) )
			maps.append( map )
			maps_min.append( map.name )

window.set_loading( 'Spawning Menu' )

tx = Queue()
rx = Queue()

menus = Menus( 'qt', tx, rx )

tx.put_nowait( messages.Message( messages.MAPS, {'maps': maps_min } ) )
menus.main_menu()

game = Game()

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
			import_path = root.replace( '/', '.' ) + '.object'
			f = open( root + '/' + file )
			object_yaml = yaml.load( f )
			f.close()
			# TODO: Version checking
			objects.append( Object( object_yaml, import_path ) )

window.set_loading( 'Loading UI' )

tx.put_nowait( messages.Message( messages.OBJECTS, {'objects': objects } ) )

menus.in_game_menu()

window.floor_offset = game.map.floors - WINDOW_FLOORS - int( game.map.dirt_floors / 2 )
window.slice_offset = 0 #TODO: Fix this to a good value: int( game.map.slices / 2 ) ?
window.load_tile_set( game.map.get_tile_paths( window.floor_offset, game.clock ) )

frame_remains = TICK_REAL_TIME
paused = False
cursor_object = None
while True:

	frame_start = time()

	floor_offset = window.floor_offset
	slice_offset = window.slice_offset

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			tx.put_nowait( messages.Message( messages.QUIT ) )
			quit()

		elif event.type == pygame.MOUSEMOTION:
			window.move_cursor( event.pos )

		#elif event.type == pygame.MOUSEBUTTONUP:
			#if event.button == 1:
				## Snap to grid
				#pos = ( int( event.pos[0] / SLICE_WIDTH ) * SLICE_WIDTH, int( event.pos[1] / FLOOR_HEIGHT ) * FLOOR_HEIGHT )
				#floor = int( pos[1] / FLOOR_HEIGHT ) + window.floor_offset
				#slice = int( pos[0] / SLICE_WIDTH ) + window.slice_offset
				#if "floor" == cursor_object:
					#if logic.addFloorSlice( pos, game ):
						#window.refresh( floor, slice, game )

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				floor_offset = floor_offset + 1
			elif event.key == pygame.K_UP:
				floor_offset = floor_offset - 1
			elif event.key == pygame.K_LEFT:
				slice_offset = slice_offset - 1
			elif event.key == pygame.K_RIGHT:
				slice_offset = slice_offset + 1

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
			cursor_object = msg.object
			window.set_cursor( msg.cursor )
	except Empty:
		pass


	# Over-adjust corrections...
	if slice_offset + WINDOW_SLICES > game.map.slices:
		slice_offset = game.map.slices - WINDOW_SLICES
	elif slice_offset < 0:
		slice_offset = 0

	if floor_offset + WINDOW_FLOORS > game.map.floors:
		floor_offset = game.map.floors - WINDOW_FLOORS
	elif floor_offset < 0:
		floor_offset = 0

	# Now choose the right rendering function
	if floor_offset != window.floor_offset:
		window.floor_offset = floor_offset
		window.slice_offset = slice_offset
		window.load_tile_set( game.map.get_tile_paths( window.floor_offset, game.clock ) )
	elif slice_offset != window.slice_offset:
		window.slice_offset = slice_offset
		window.refresh_background()

	if not paused:
		frame_end = time()
		frame_remains = frame_remains - ( frame_end - frame_start )
		if 0 >= frame_remains:
			game.clock_tick()
			notify_ui()
			frame_remains = TICK_REAL_TIME

	window.update()