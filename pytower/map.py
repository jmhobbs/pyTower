# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

class MapBackground ():
	def __init__ ( self, yaml ):
		self.directory = yaml['dir']
		self.hour = yaml['hour']
		self.minute = yaml['minute']

class Map ():
	def __init__( self, yaml, import_path ):
		self.import_path = import_path
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

	def get_tile_path ( self, clock ):
		rval = self.backgrounds[0]
		cdiff = 0
		for background in self.backgrounds:
