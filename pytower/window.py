# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

import pygame
from constants import *
from utility import FullPath

class Window ():
	def __init__ ( self ):
		"""
		Starts up SDL, loads some common resources.
		"""
		pygame.display.set_icon( pygame.image.load( FullPath( 'resources/icon.16x16.png' ) ) )
		self.window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
		pygame.display.set_caption( 'pyTower - v' + VERSION  )

		# Dirty rectangles for the main window surface (self.window)
		self.windowDirtyRectangles = []

		# Used for the loading screen system
		self.loadingFont = pygame.font.SysFont( None, 48 )
		self.loadingRect = None

		# self.overlay is the "lay on top" layer. This is where the cursor, minimap, etc. are drawn
		self.overlay = pygame.Surface( ( WINDOW_WIDTH, WINDOW_HEIGHT ), pygame.SRCALPHA )
		# self.background is the tiles + flooring + static odds and ends
		self.background = pygame.Surface( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )

		# These are the storage for the background tiles to be loaded into
		self.tiles = [None] * WINDOW_FLOORS

		# These are commonly used resources
		self.resource = {}
		self.resource['floor'] = pygame.image.load( FullPath( 'resources/floor.bmp' ) ).convert()

		# This is the current cursor graphic
		self.cursor = pygame.Surface( ( 0, 0 ) )
		self.cursorRect = ( 0, 0, 0, 0 )

		# These are the offsets for the mapping of window to game surface
		self.floor_offset = 0
		self.slice_offset = 0

	def update ( self ):
		"""
		Update the screen as needed. This uses the windowDirtyRectangles variable
		to figure out what needs to be refreshed.
		"""
		if list == type( self.windowDirtyRectangles ):
			pygame.display.update( self.windowDirtyRectangles )
		self.windowDirtyRectangles = []

	def dirty ( self, rectangle ):
		self.windowDirtyRectangles.append( rectangle )

	def init_loading ( self ):
		"""
		Initialize the loading screen.
		"""
		self.background = pygame.image.load( FullPath( 'resources/loading.bmp' ) ).convert()
		self.window.blit( self.background, ( 0, 0 ) )
		self.loadingRect = None

		self.dirty ( ( 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT ) )
		self.update()

	def set_loading ( self, text ):
		"""
		Set the text on the loading screen.
		"""
		if None != self.loadingRect:
			self.window.blit( self.background, self.loadingRect, self.loadingRect )
			self.dirty( self.loadingRect )

		text = self.loadingFont.render( text , True, BLACK )

		self.loadingRect = text.get_rect()
		self.loadingRect.centerx = self.window.get_rect().centerx
		self.loadingRect.centery = self.window.get_rect().centery

		self.window.blit( text, self.loadingRect )
		self.dirty( self.loadingRect )

		self.update()

	def set_cursor ( self, cursor ):
		"""
		Set the graphic for the cursor.
		"""
		if None == cursor:
			self.cursor = pygame.Surface( ( 0, 0 ) )
		else:
			self.cursor = pygame.image.load( FullPath( cursor ) ).convert()

		self.move_cursor( pygame.mouse.get_pos() )

	def move_cursor ( self, pos ):
		"""
		Move the cursor on the screen.
		"""
		# Snap to the grid
		pos = ( int( pos[0] / SLICE_WIDTH ) * SLICE_WIDTH, int( pos[1] / FLOOR_HEIGHT ) * FLOOR_HEIGHT )
		# Don't bother if we aren't moving outside of a snap
		if pos[0] == self.cursorRect[0] and pos[1] == self.cursorRect[1]:
			return
		# 1 - Blit over previous cursor.
		self.window.blit( self.background, self.cursorRect, self.cursorRect )
		self.window.blit( self.overlay, self.cursorRect, self.cursorRect )
		# 2 - Dirty that rectangle.
		self.dirty( self.cursorRect )
		# 3 - Blit in the new cursor.
		self.window.blit( self.cursor, pos )
		# 4 - Dirty that rectangle.
		self.dirty( ( pos[0], pos[1], self.cursor.get_rect().width, self.cursor.get_rect().height ) )
		# 5 - Save that cursor.
		self.cursorRect = ( pos[0], pos[1], self.cursor.get_rect().width, self.cursor.get_rect().height )

	def load_tile_set ( self, tile_paths ):
		"""
		This function is used when drawing new tiles, i.e. clock change or vertical scroll
		"""
		for i in range( 0, WINDOW_FLOORS ):
			self.tiles[i] = pygame.image.load( tile_paths[i] ).convert()
		self.refresh_background()
		# TODO: Re-blit the flooring and the context

	def refresh_background ( self ):
		"""
		This function is used to redraw on horizonal scroll
		"""
		for i in range( 0, WINDOW_FLOORS ):
			self.background.blit( self.tiles[i], ( 0, FLOOR_HEIGHT * i ), ( self.slice_offset * SLICE_WIDTH, 0, WINDOW_WIDTH, FLOOR_HEIGHT ) )
		self.window.blit( self.background, ( 0, 0 ) )
		self.dirty( ( 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT ) )
		# TODO: Re-blit the flooring and the context