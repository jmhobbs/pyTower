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

#def quit():
	#if None != ui:
		#ui.join()
	#pygame.quit()
	#exit()

#def notify_ui():
	#m = messages.Message( messages.NOTIFY_TIME )
	#m.time = Globals.game_clock
	#Globals.q_tx.put_nowait( m )
	#m = messages.Message( messages.NOTIFY_CASH )
	#m.cash = Globals.cash
	#Globals.q_tx.put_nowait( m )
	#m = messages.Message( messages.NOTIFY_POPULATION )
	#m.population = Globals.population
	#Globals.q_tx.put_nowait( m )

pygame.init()

window = Window()

window.init_loading()
window.set_loading( 'Loading Maps' )

maps = []

for root, dirs, files in walk( 'maps/' ):
	for file in files:
		if file == 'map.yaml':
			import_path = root.replace( '/', '.' ) + '.map'
			f = open( root + '/' + file )
			map_yaml = yaml.load( f )
			f.close()
			# TODO: Version checking
			maps.append( Map( map_yaml, import_path ) )

window.set_loading( 'Spawning Menu' )

tx = Queue()
rx = Queue()

menus = Menus( 'qt', tx, rx )
menus.main_menu()

window.set_loading( 'Ready!' )

while True:

	# Only redraw if we have to...
	for event in pygame.event.get():
		if event.type == pygame.VIDEOEXPOSE:
			window.update()

	try:
		msg = rx.get_nowait()
		print msg
		if messages.QUIT == msg.instruction:
			pygame.quit()
			exit()
		#elif messages.NEW_GAME == msg.instruction:
			#Globals.cash = 500000
			#Globals.game_clock = [ 1, 1, 1, 0, 0 ]
			#Globals.population = 0
			#break
	except Empty:
		pygame.time.delay( IPQUEUE_SLEEP )

#window.set_loading( 'Loading Objects' )

#objects = []
#for root, dirs, files in walk( 'objects/' ):
	#for file in files:
		#if file == 'object.yaml':
			#import_path = root.replace( '/', '.' ) + '.map'
			#f = open( root + '/' + file )
			#object_yaml = yaml.load( f )
			#f.close()
			## TODO: Version checking
			#objects.append( Object( object_yaml, import_path ) )

#Globals.q_tx.put_nowait( messages.Message( messages.MAPS, { 'maps': Globals.maps } ) )

#ui = Process( target=GUI.show_main_menu, args=( Globals.q_tx, Globals.q_rx ) )
#ui.start()

#Render.set_loading( 'Ready!' )


#Render.initialize_surfaces()

#notify_ui()

#ui = Process( target=GUI.show_in_game_menu, args=( Globals.q_tx, Globals.q_rx ) )
#ui.start()

#Render.stop_loading()

#frame_remains = Constants.FRAME_LENGTH
#paused = False
#cursor_object = None
#while True:

	#frame_start = time()

	#v_offset = Globals.v_offset
	#h_offset = Globals.h_offset
	#force_fu = False

	#for event in pygame.event.get():
		#if event.type == QUIT:
			#Globals.q_tx.put_nowait( messages.Message( messages.QUIT ) )
			#quit()

		#elif event.type == VIDEOEXPOSE:
			#force_fu = True

		#elif event.type == MOUSEMOTION:
			#Render.MoveCursor( event.pos )

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

	## Check with the UI message queue
	#try:
		#msg = Globals.q_rx.get_nowait()
		#print msg
		#if messages.QUIT == msg.instruction:
			#quit()
		#elif messages.PAUSE == msg.instruction:
			#paused = True
		#elif messages.PLAY == msg.instruction:
			#paused = False
		#elif messages.SET_CURSOR == msg.instruction:
			#cursor_object = msg.object
			#Render.SetCursor( msg.cursor )
	#except Empty:
		#pass

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

	## Run the clock!
	#if not paused:
		#frame_end = time()
		#frame_remains = frame_remains - ( frame_end - frame_start )
		#if 0 >= frame_remains:
			#increment_game_clock()
			#notify_ui()
			#frame_remains = Constants.FRAME_LENGTH