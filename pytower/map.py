# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

class MapOffset ():
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
		self.offsets = []
		for offset in yaml['map']['offsets']:
			self.offsets.append( MapOffset( yaml['map']['offsets'][offset] ) )

	def load_for_use ( self ):
		self.script = __import__( self.import_path, None, None, [''] )
		# TODO: Check what is callable so we can proxy.