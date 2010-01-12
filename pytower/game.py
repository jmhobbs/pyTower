# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

from constants import *

class Game ():
	def __init__ ( self ):
		"""
		Initializes a game. Just sets stub values.
		"""
		self.map = None
		self.cash = None
		self.set_clock()
		self.population = None
		self.peak_population = None

	def load_from_file ( self, path ):
		"""
		Will eventually load data from a file.
		TODO
		"""
		print "Stub!"

	def new_from_map ( self, map ):
		"""
		Start a new game from a Map object.
		"""
		# Here's how this works.  The top left slice of the object goes in that index slot.
		# All the other ones it overlaps get a # that references that slot. None means empty.
		# "0" means floor there, but otherwise empty.
		self.map = map
		self.contents = [None] * map.floors
		for i in range( map.floors ):
			self.contents[i] = [None] * ( map.slices )

	def set_clock ( self, year=0, month=0, day=0, hour=0, minute=0 ):
		self.clock = {'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute}
		self.adjust_clock()

	def clock_tick ( self ):
		"""
		Increment the game clock by one tick.
		"""
		self.clock['minute'] = self.clock['minute'] + TICK_MINUTES
		self.adjust_clock()

	def adjust_clock ( self ):
		"""
		Adjusts the clock to a valid state by pushing numbers up the chain.
		"""
		if self.clock['minute'] >= MINUTES_PER:
			self.clock['minute'] = 0
			self.clock['hour'] = self.clock['hour'] + 1
			if self.clock['hour'] > HOURS_PER:
				self.clock['hour'] = 1
				self.clock['day'] = self.clock['day'] + 1
				if self.clock['day'] > DAYS_PER:
					self.clock['day'] = 1
					self.clock['month'] = self.clock['month'] + 1
					if self.clock['month'] > MONTHS_PER:
						self.clock['month'] = 1
						self.clock['year'] = self.clock['year'] + 1