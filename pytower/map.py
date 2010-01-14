# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

from constants import *

class MapBackground ():
	def __init__ ( self, yaml ):
		self.directory = yaml['dir']
		self.hour = yaml['hour']
		self.minute = yaml['minute']

class Map ():
	def __init__( self, yaml, import_path, real_path ):
		self.import_path = import_path
		self.real_path = real_path
		self.name = yaml['map']['name']
		self.version = yaml['map']['version']
		self.author_name = yaml['map']['author']['name']
		self.author_link = yaml['map']['author']['link']
		self.floors = yaml['map']['dimensions']['floors']
		self.slices = yaml['map']['dimensions']['slices']
		self.dirt_floors = yaml['map']['dimensions']['dirtfloors']
		self.backgrounds = []
		for background in yaml['map']['backgrounds']:
			self.backgrounds.append( MapBackground( yaml['map']['backgrounds'][background] ) )

	def load_for_use ( self ):
		self.script = __import__( self.import_path, None, None, [''] )
		# TODO: Check what is callable so we can proxy.

	def get_tile_paths ( self, voffset, clock ):
		tiles = []
		# TODO: Do something useful with the clock
		for i in range( 0, WINDOW_FLOORS ):
			tiles.append( '%s/%s/%d.jpg' % ( self.real_path, self.backgrounds[0].directory, self.floors - ( voffset + i ) ) )
		return tiles