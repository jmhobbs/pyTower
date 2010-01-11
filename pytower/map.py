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
	def __init__( self, yaml ):
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