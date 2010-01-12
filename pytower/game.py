# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

import

class Game ():
	def __init__ ( self ):
		"""
		Initializes a game. Just sets stub values.
		"""
		self.map = None
		self.cash = None
		self.clock = None

	def load_from_file ( self, path ):
		"""
		Will eventually load data from a file.
		TODO
		"""
		print "Stub!"

	def new_from_map ( self, map ):
		"""
		Will eventually start a new game from a Map object.
		TODO
		"""
		print "Stub!"

	def clock_tick ( self ):
		"""
		Increment the game clock by one tick (5 game time minutes)
		"""
		self.clock[4] = self.clock[4] + 5
		if self.clock[4] >= 60:
			self.clock[4] = 0
			self.clock[3] = self.clock[3] + 1
			if self.clock[3] > 24:
				self.clock[3] = 1
				self.clock[2] = self.clock[2] + 1
				if self.clock[2] > 6:
					self.clock[2] = 1
					self.clock[1] = self.clock[1] + 1
					if self.clock[1] > 12:
						self.clock[1] = 1
						self.clock[0] = self.clock[0] + 1