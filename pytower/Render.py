# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

import pygame
from Constants.locals import *

class Render ():
	def __init__ ( self ):
		pygame.display.set_icon( pygame.image.load( 'resources/icon.16x16.png' ) )
		self.window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
		pygame.display.set_caption( 'pyTower - v' + VERSION  )

		self.loadingFont = pygame.font.SysFont( None, 48 )
		self.loadingRect = None

		self.context = pygame.Surface( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
		self.windowDirtyRectangles = []
		self.floorSurface = pygame.image.load( 'resources/floor.bmp' ).convert()

	def update ():
		if list == type( self.windowDirtyRectangles ):
			pygame.display.update( self.windowDirtyRectangles )
		self.windowDirtyRectangles = []

	def init_loading ():
		"""
		Initialize the loading screen.
		"""
		self.context = pygame.image.load( 'resources/loading.bmp' ).convert()
		self.window.blit( self.context, ( 0, 0 ) )
		self.loadingRect = None

		self.windowDirtyRectangles.append( ( 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT ) )
		self.update()

def set_loading ( text ):
	"""
	Set the text on the loading screen.
	"""
	if None != self.loadingRect:
		self.window.blit( self.context, self.loadingRect, self.loadingRect )
		self.windowDirtyRectangles.append( self.loadingRect )

	text = self.loadingFont.render( text , True, Colors.BLACK )

	self.loadingRect = text.get_rect()
	self.loadingRect.centerx = self.window.get_rect().centerx
	self.loadingRect.centery = self.window.get_rect().centery

	self.window.blit( text, self.loadingRect )
	self.windowDirtyRectangles.append( self.loadingRect )

	self.update()

def initialize_surfaces ():
	set_loading( 'Finding offsets...' )

	Globals.h_offset = CENTER
	Globals.v_offset = BOTTOM

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
	# Check & load slices
	for i in range( 1, WINDOW_FLOORS ):
		self.window_slices[i-1] = pygame.image.load( 'maps/default/day/%d.jpg' % ( i ) ).convert()
		Globals.s_render.blit( self.window_slices[i-1], ( 0, WINDOW_HEIGHT - ( i * FLOOR_HEIGHT ) ) ) # TODO: Offset from the slice to match window!
	# Load flooring
	# Load objects
	#for i in range( 0, WINDOW_FLOORS ):
		#slice_look_ahead = 0
		#for j in range( 0, WINDOW_SLICES ):
			## slice_look_ahead is used to skip over already rendered things
			#if 0 < slice_look_ahead:
				#slice_look_ahead = slice_look_ahead - 1
				#continue
			#f = Globals.v_offset + i
			#s = Globals.h_offset + j
			#placement = ( j * SLICE_WIDTH, i * FLOOR_HEIGHT )
			#if Globals.game_map[f][s] == None:
				#if ( FLOORS - f ) <= DIRT_FLOORS:
					## Dirt is a special case. We want to read ahead to use as much of our tile as we can
					#r = 1
					#for q in range( 1, 4 ):
						#try:
							#if Globals.game_map[f][s+q] == None:
								#r = r + 1
							#else:
								#break
						#except:
							#break
					#Globals.s_render.blit( Globals.res_dirt, placement, ( 0, 0, r * SLICE_WIDTH, FLOOR_HEIGHT ) )
					#slice_look_ahead = r - 1
			#elif Globals.game_map[f][s] == 0:
				## Empty flooring
				#Globals.s_render.blit( Globals.res_floor, placement )
	self.window.blit( Globals.s_render, ( 0, 0 ) )
	full_update()
	MoveCursor( pygame.mouse.get_pos() )

def RedrawMiniMap ():
	# TODO: Rework
	pass

def MoveCursor ( pos ):
	# Snap to the grid
	pos = ( int( pos[0] / SLICE_WIDTH ) * SLICE_WIDTH, int( pos[1] / FLOOR_HEIGHT ) * FLOOR_HEIGHT )
	# 1 - Blit over previous cursor.
	self.window.blit( Globals.s_render, Globals.r_cursor, Globals.r_cursor )
	# 2 - Dirty that rectangle.
	Globals.dr_window.append( ( Globals.r_cursor[0], Globals.r_cursor[1], Globals.r_cursor[2], Globals.r_cursor[3] ) )
	# 3 - Blit in the new cursor.
	self.window.blit( Globals.s_cursor, pos )
	# 4 - Dirty that rectangle.
	Globals.dr_window.append( ( pos[0], pos[1], Globals.s_cursor.get_rect().width, Globals.s_cursor.get_rect().height ) )
	# 5 - Save that cursor.
	Globals.r_cursor = ( pos[0], pos[1], Globals.s_cursor.get_rect().width, Globals.s_cursor.get_rect().height )
	# 6 - Redraw mini-map
	#RedrawMiniMap()