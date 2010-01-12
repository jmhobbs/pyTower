# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

import pygame
from constants.locals import *
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
		self.overlay = pygame.Surface( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
		# self.background is the tiles + flooring + static odds and ends
		self.background = pygame.Surface( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )

		# These are commonly used resources
		self.resource = {}
		self.resource['floor'] = pygame.image.load( 'resources/floor.bmp' ).convert()

		# This is the current cursor graphic
		self.cursor = pygame.Surface( ( 0, 0 ) )
		self.cursorRect = ( 0, 0, 0, 0 )

	def update ( self ):
		"""
		Update the screen as needed. This uses the windowDirtyRectangles variable
		to figure out what needs to be refreshed.
		"""
		if list == type( self.windowDirtyRectangles ):
			pygame.display.update( self.windowDirtyRectangles )
		self.windowDirtyRectangles = []

	def init_loading ( self ):
		"""
		Initialize the loading screen.
		"""
		self.background = pygame.image.load( FullPath( 'resources/loading.bmp' ) ).convert()
		self.window.blit( self.background, ( 0, 0 ) )
		self.loadingRect = None

		self.windowDirtyRectangles.append( ( 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT ) )
		self.update()

	def set_loading ( self, text ):
		"""
		Set the text on the loading screen.
		"""
		if None != self.loadingRect:
			self.window.blit( self.background, self.loadingRect, self.loadingRect )
			self.windowDirtyRectangles.append( self.loadingRect )

		text = self.loadingFont.render( text , True, Colors.BLACK )

		self.loadingRect = text.get_rect()
		self.loadingRect.centerx = self.window.get_rect().centerx
		self.loadingRect.centery = self.window.get_rect().centery

		self.window.blit( text, self.loadingRect )
		self.windowDirtyRectangles.append( self.loadingRect )

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
		if pos[0] == self.cursorRect[0] and pos[1] == self.cursorRect[1]:
			return # Don't bother if we aren't moving outside of a snap
		# 1 - Blit over previous cursor.
		self.window.blit( self.background, self.cursorRect, self.cursorRect )
		self.window.blit( self.overlay, self.cursorRect, self.cursorRect )
		# 2 - Dirty that rectangle.
		self.windowDirtyRectangles.append( ( self.cursorRect[0], self.cursorRect[1], self.cursorRect[2], self.cursorRect[3] ) )
		# 3 - Blit in the new cursor.
		self.window.blit( self.cursor, pos )
		# 4 - Dirty that rectangle.
		self.windowDirtyRectangles.append( ( pos[0], pos[1], Globals.s_cursor.get_rect().width, Globals.s_cursor.get_rect().height ) )
		# 5 - Save that cursor.
		self.cursorRect = ( pos[0], pos[1], self.cursor.get_rect().width, self.cursor.get_rect().height )

	def update_background ( self ):
		for i in range( 1, WINDOW_FLOORS ):
			self.window_slices[i-1] = pygame.image.load( 'maps/default/day/%d.jpg' % ( i ) ).convert()
			Globals.s_render.blit( self.window_slice