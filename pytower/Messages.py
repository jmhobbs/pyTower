# -*- coding: utf-8 -*-

# Forcing the use of these messages may seem restrictive, but it lets us have a defined protocol set.
QUIT = 0
NEWGAME = 1

MESSAGES = ( 'QUIT', 'NEWGAME' )

class Message ():
	def __init__ ( self, instruction ):
		self.instruction = instruction

	def __str__ ( self ):
		s = "<pytower.Messages.Message> - " + MESSAGES[self.instruction] + " { "
		for key in self.__dict__.keys():
			s = s + "'" + key + "': '" + str( self.__dict__[key] ) + "', "
		return s + "}"