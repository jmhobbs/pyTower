# -*- coding: utf-8 -*-
import pygame

import Constants
import Colors
import Globals

def init ():
	Globals.s_window = pygame.display.set_mode( ( Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ), 0, 32 )
	pygame.display.set_caption( 'pyTower - v' + Constants.VERSION  )
	Globals.f_loading = pygame.font.SysFont( None, 48 )

# We aren't a full screen game, so every once in a while we need a full update.
def full_update ():
	pygame.display.update()

def dirty_update ():
	pygame.display.update( Globals.dr_window )

def load_resources ():
	Globals.res_floor = pygame.image.load( 'resources/floor.bmp' ).convert()
	Globals.res_dirt = pygame.image.load( 'resources/dirt.bmp' ).convert()

def draw_floor ( h_offset, floors ):
	Globals.s_full.blit( Globals.res_floor, ( h_offset, Constants.GAME_HEIGHT - ( Constants.FLOOR_HEIGHT * floors ) ) )
	move()

def start_loading ():
	Globals.s_loading = pygame.image.load( 'resources/loading.bmp' ).convert()
	Globals.s_window.blit( Globals.s_loading, ( 0, 0 ) )
	Globals.r_loading = None

def set_loading ( text ):
	if None != Globals.r_loading:
		Globals.s_window.blit( Globals.s_loading, Globals.r_loading, Globals.r_loading )
	text = Globals.f_loading.render( text , True, Colors.BLACK )
	Globals.r_loading = text.get_rect()
	Globals.r_loading.centerx = Globals.s_window.get_rect().centerx
	Globals.r_loading.centery = Globals.s_window.get_rect().centery
	Globals.s_window.blit( text, Globals.r_loading )
	pygame.display.update() # TODO: Switch to dirty rectangle

def stop_loading ():
	del Globals.s_loading
	Globals.s_loading = None

def initialize_surfaces ():
	# Viewport offsets
	set_loading( 'Finding offsets...' )
	pygame.time.delay( 250 )
	Globals.h_offset = Constants.CENTER
	Globals.v_offset = Constants.BOTTOM - ( Constants.FLOOR_HEIGHT * 5 )
	set_loading( 'Building surface...' )
	pygame.time.delay( 250 )
	Globals.s_full = pygame.Surface( ( Constants.GAME_WIDTH, Constants.GAME_HEIGHT ) )
	# TODO: Replace with a real startup routine that draws nice dirt & sky :-/
	Globals.s_full.fill( Colors.SKY_BLUE )
	for y in range( 1, 10 ):
		for x in range( 0, Constants.GAME_WIDTH, Constants.FLOOR_HEIGHT ):
			Globals.s_full.blit( Globals.res_dirt, ( x, Globals.s_full.get_rect().bottom - ( Constants.FLOOR_HEIGHT * y ) ) )
	#drawrect = ( Globals.s_full.get_rect().left, Globals.s_full.get_rect().bottom - ( Constants.FLOOR_HEIGHT * 10 ), Globals.s_full.get_rect().width, ( Constants.FLOOR_HEIGHT * 5 ) )
	#pygame.draw.rect( Globals.s_full, Colors.LIGHT_BROWN, drawrect )
	#drawrect = ( Globals.s_full.get_rect().left, Globals.s_full.get_rect().bottom - ( Constants.FLOOR_HEIGHT * 5 ), Globals.s_full.get_rect().width, ( Constants.FLOOR_HEIGHT * 5 ) )
	#pygame.draw.rect( Globals.s_full, Colors.DARK_BROWN, drawrect )
	set_loading( 'Drawing map...' )
	pygame.time.delay( 250 )
	# This is a representative surface used as a "map"
	Globals.s_mini = pygame.Surface( ( Constants.MINI_WIDTH, Constants.MINI_HEIGHT ) )
	Globals.s_mini.set_alpha( 200 )
	Globals.s_mini.fill( Colors.SKY_BLUE )
	drawrect = ( Globals.s_mini.get_rect().left, Globals.s_mini.get_rect().bottom - ( 10 ), Globals.s_mini.get_rect().width, ( 10 ) )
	pygame.draw.rect( Globals.s_mini, Colors.LIGHT_BROWN, drawrect )
	set_loading( 'Reticulating splines...' )
	pygame.time.delay( 500 )
	# Now blit the starting, blank surface on
	Globals.s_window.blit( Globals.s_full, ( 0, 0 ), ( 0 + Globals.h_offset, 0 + Globals.v_offset, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ) )
	drawrect = ( 9, 9, Constants.MINI_WIDTH + 2, Constants.MINI_HEIGHT + 2 )
	pygame.draw.rect( Globals.s_window, Colors.BLACK, drawrect )
	Globals.s_window.blit( Globals.s_mini, ( 10, 10 ), ( 0, 0, Constants.MINI_WIDTH, Constants.MINI_HEIGHT ) )
	drawrect = ( 10 + ( Globals.h_offset / Constants.FLOOR_HEIGHT ), 10 + ( Globals.v_offset / Constants.FLOOR_HEIGHT ), ( Constants.WINDOW_WIDTH / Constants.FLOOR_HEIGHT ), ( Constants.WINDOW_HEIGHT / Constants.FLOOR_HEIGHT ) )
	pygame.draw.rect( Globals.s_window, Colors.BLACK, drawrect )
	full_update()

def move ():
	Globals.s_window.blit( Globals.s_full, ( 0, 0 ), ( 0 + Globals.h_offset, 0 + Globals.v_offset, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT ) )

	drawrect = ( 9, 9, Constants.MINI_WIDTH + 2, Constants.MINI_HEIGHT + 2 )
	pygame.draw.rect( Globals.s_window, Colors.BLACK, drawrect )

	Globals.s_window.blit( Globals.s_mini, ( 10, 10 ), ( 0, 0, Constants.MINI_WIDTH, Constants.MINI_HEIGHT ) )

	drawrect = ( 10 + ( Globals.h_offset / Constants.FLOOR_HEIGHT ), 10 + ( Globals.v_offset / Constants.FLOOR_HEIGHT ), ( Constants.WINDOW_WIDTH / Constants.FLOOR_HEIGHT ), ( Constants.WINDOW_HEIGHT / Constants.FLOOR_HEIGHT ) )
	pygame.draw.rect( Globals.s_window, Colors.BLACK, drawrect )

	full_update()