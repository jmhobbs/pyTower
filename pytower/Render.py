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

	Globals.h_offset = 0
	Globals.v_offset = 0

	set_loading( 'Building surfaces...' )

	SetCursor( None )

	set_loading( 'Drawing map...' )

	# TODO: Mini map...

	set_loading( 'Reticulating splines...' )

	# TODO: Blit the initial map on.

def SetCursor ( cursor ):
	if None == cursor:
		Globals.s_cursor = pygame.Surface( ( 0, 0 ) )

def move ():
	# TODO: Rework
	pass

def RedrawMiniMap ():
	# TODO: Rework
	pass

def MoveCursor ( pos ):
	# Snap to the grid
	pos = ( int( pos[0] / Constants.SLICE_WIDTH ) * Constants.SLICE_WIDTH, int( pos[1] / Constants.FLOOR_HEIGHT ) * Constants.FLOOR_HEIGHT )
	# 1 - Blit over previous cursor.
	# TODO: Rework?
	# 2 - Dirty that rectangle.
	#Globals.dr_window.append( ( Globals.r_cursor[0], Globals.r_cursor[1], Globals.r_cursor[2], Globals.r_cursor[3] ) )
	# 3 - Blit in the new cursor.
	Globals.s_window.blit( Globals.s_cursor, pos )
	# 4 - Dirty that rectangle.
	Globals.dr_window.append( ( pos[0], pos[1], Globals.s_cursor.get_rect().width, Globals.s_cursor.get_rect().height ) )
	# 5 - Save that cursor.
	Globals.r_cursor = ( pos[0], pos[1], Globals.s_cursor.get_rect().width, Globals.s_cursor.get_rect().height )
	# 6 - Redraw mini-map
	#RedrawMiniMap()