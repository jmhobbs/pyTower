# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

import pygame

import Constants
import Colors
import Globals

def init ():
	"""
	Set up the pygame working area.
	"""
	pygame.display.set_icon( pygame.image.load( 'resources/icon.16x16.png' ) )
	Globals.s_window = pygame.display.set_mode( ( Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ) )
	pygame.display.set_caption( 'pyTower - v' + Constants.VERSION  )
	Globals.f_loading = pygame.font.SysFont( None, 48 )
	Globals.s_render = pygame.Surface( ( Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ) )

def full_update ():
	"""
	Update the whole window surface. Usefull for moves or expose events.
	"""
	pygame.display.update()
	Globals.dr_window = []

def dirty_update ():
	"""
	Only update the rectangles that are dirty.
	"""
	if list == type( Globals.dr_window ):
		pygame.display.update( Globals.dr_window )
	Globals.dr_window = []

def load_resources ():
	"""
	Load up any re-usable resources we might need.
	"""
	Globals.res_floor = pygame.image.load( 'resources/floor.bmp' ).convert()
	Globals.res_dirt = pygame.image.load( 'resources/dirt.bmp' ).convert()

def start_loading ():
	"""
	Initialize the loading screen.
	"""
	Globals.s_loading = pygame.image.load( 'resources/loading.bmp' ).convert()
	Globals.s_window.blit( Globals.s_loading, ( 0, 0 ) )
	Globals.r_loading = None
	full_update()

def set_loading ( text ):
	"""
	Set the text on the loading screen.
	"""
	if None != Globals.r_loading:
		Globals.s_window.blit( Globals.s_loading, Globals.r_loading, Globals.r_loading )
		Globals.dr_window.append( Globals.r_loading )

	text = Globals.f_loading.render( text , True, Colors.BLACK )

	Globals.r_loading = text.get_rect()
	Globals.r_loading.centerx = Globals.s_window.get_rect().centerx
	Globals.r_loading.centery = Globals.s_window.get_rect().centery

	Globals.s_window.blit( text, Globals.r_loading )
	Globals.dr_window.append( Globals.r_loading )

	dirty_update()

def stop_loading ():
	"""
	Clean up the loading screen.
	"""
	del Globals.s_loading
	Globals.s_loading = None

def initialize_surfaces ():
	set_loading( 'Finding offsets...' )

	Globals.h_offset = Constants.CENTER
	Globals.v_offset = Constants.BOTTOM

	set_loading( 'Building surfaces...' )

	SetCursor( None )

	set_loading( 'Reticulating splines...' )
	pygame.time.delay( 750 )

	move()

def SetCursor ( cursor ):
	if None == cursor:
		Globals.s_cursor = pygame.Surface( ( 0, 0 ) )
	else:
		Globals.s_cursor = pygame.image.load( cursor ).convert()
	MoveCursor( pygame.mouse.get_pos() )

def move ():
	for i in range( 0, Constants.WINDOW_FLOORS ):
		slice_look_ahead = 0
		for j in range( 0, Constants.WINDOW_SLICES ):
			# slice_look_ahead is used to skip over already rendered things
			if j < slice_look_ahead:
				continue
			f = Globals.v_offset + i
			s = Globals.h_offset + j
			placement = ( j * Constants.SLICE_WIDTH, i * Constants.FLOOR_HEIGHT )
			if Globals.game_map[f][s] == None:
				# Nothing there. Draw dirt or sky.
				if ( Constants.FLOORS - f ) > Constants.DIRT_FLOORS:
					pygame.draw.rect( Globals.s_render, Colors.SKY_BLUE, ( placement[0], placement[1], Constants.SLICE_WIDTH, Constants.FLOOR_HEIGHT ) )
				else:
					# Dirt is a special case. We want to read ahead to use as much of our tile as we can
					r = 1
					for q in range( 0, 3 ):
						try:
							if Globals.game_map[f][s+q] != None:
								break
						except:
							break
						r = r + 1
					Globals.s_render.blit( Globals.res_dirt, placement, ( 0, 0, r * Constants.SLICE_WIDTH, Constants.FLOOR_HEIGHT ) )
					slice_look_ahead = j + r
			elif Globals.game_map[f][s] == 0:
				# Empty flooring
				Globals.s_render.blit( Globals.res_floor, placement )
	Globals.s_window.blit( Globals.s_render, ( 0, 0 ) )
	full_update()
	MoveCursor( pygame.mouse.get_pos() )

def RedrawMiniMap ():
	# TODO: Rework
	pass

def MoveCursor ( pos ):
	# Snap to the grid
	pos = ( int( pos[0] / Constants.SLICE_WIDTH ) * Constants.SLICE_WIDTH, int( pos[1] / Constants.FLOOR_HEIGHT ) * Constants.FLOOR_HEIGHT )
	# 1 - Blit over previous cursor.
	Globals.s_window.blit( Globals.s_render, Globals.r_cursor, Globals.r_cursor )
	# 2 - Dirty that rectangle.
	Globals.dr_window.append( ( Globals.r_cursor[0], Globals.r_cursor[1], Globals.r_cursor[2], Globals.r_cursor[3] ) )
	# 3 - Blit in the new cursor.
	Globals.s_window.blit( Globals.s_cursor, pos )
	# 4 - Dirty that rectangle.
	Globals.dr_window.append( ( pos[0], pos[1], Globals.s_cursor.get_rect().width, Globals.s_cursor.get_rect().height ) )
	# 5 - Save that cursor.
	Globals.r_cursor = ( pos[0], pos[1], Globals.s_cursor.get_rect().width, Globals.s_cursor.get_rect().height )
	# 6 - Redraw mini-map
	#RedrawMiniMap()