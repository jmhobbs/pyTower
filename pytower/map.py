# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

from constants import *

class MapBackground ():
	def __init__ ( self, yaml ):
		self.file = yaml['file']
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

	def get_current_background ( self, clock ):
		cbg = self.backgrounds[-1]
		for i in self.backgrounds:
			if i.hour > clock['hour']:
				break;
			elif ( i.hour == clock['hour'] and i.minute <= clock['minute'] ) or i.hour < clock['hour']:
				cbg = self
		return cbg