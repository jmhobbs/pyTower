# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

# Forcing the use of these messages may seem restrictive, but it lets us have a defined protocol set.
QUIT = 0 # Quit the game immediately
NEW_GAME = 1 # Start a new game, immediately
PAUSE = 2 # Pause the game time
PLAY = 3 # Resume the game time
SET_CURSOR = 4 # Set the cursor to specified. Keys: cursor
NOTIFY_TIME = 5 # Used to pass game time between processes. Keys: time
NOTIFY_CASH = 6 # Used to pass game cash between processes Keys: cash
NOTIFY_POPULATION = 7 # Used to pass game population between processes Keys: population
MAPS = 8 # Used to send the list of maps over to the ui. Keys: maps
OBJECTS = 9 # Used to send the list of objects over to the ui. Keys: objects

MESSAGES = ( 'QUIT', 'NEW_GAME', 'PAUSE', 'PLAY', 'SET_CURSOR', 'NOTIFY_TIME', 'NOTIFY_CASH', 'NOTIFY_POPULATION', 'MAPS', 'OBJECTS' )

class Message ():
	def __init__ ( self, instruction, attrs=None ):
		self.instruction = instruction
		try:
			for key,value in attrs.items():
				setattr( self, key, value )
		except AttributeError:
			pass

	def __str__ ( self ):
		s = "<pytower.Messages.Message> - " + MESSAGES[self.instruction] + " { "
		for key in self.__dict__.keys():
			s = s + "'" + key + "': '" + str( self.__dict__[key] ) + "', "
		return s + "}"