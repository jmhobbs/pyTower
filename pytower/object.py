# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

class ObjectSprite ():
	def __init__ ( self, yaml, name ):
		self.name = name
		self.hoffset = yaml['h_offset']
		self.voffset = yaml['v_offset']

class Object ():
	def __init__( self, yaml, import_path ):
		self.import_path = import_path
		self.type = yaml['object']['type']
		self.name = yaml['object']['name']
		self.version = yaml['object']['version']
		self.author_name = yaml['object']['author']['name']
		self.author_link = yaml['object']['author']['link']
		self.floors = yaml['object']['dimensions']['floors']
		self.slices = yaml['object']['dimensions']['slices']
		self.cost = yaml['object']['cost']
		self.stars = yaml['object']['stars']
		self.offsets = []
		for offset in yaml['object']['sprites']:
			self.offsets.append( ObjectSprite( yaml['object']['sprites'][offset], offset ) )

	def load_for_use ( self ):
		self.script = __import__( self.import_path, None, None, [''] )
		# TODO: Check what is callable so we can proxy.