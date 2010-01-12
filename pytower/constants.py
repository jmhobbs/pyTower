# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

# This is just visible area, you can change it
WINDOW_FLOORS = 20
WINDOW_SLICES = 80

# This is the constant sleep between inter process queue checks. Mostly used in GUI
IPQUEUE_SLEEP = 100

# Floor ain't free (unless you change it here, cheater)
FLOOR_SLICE_COST = 500

# This is the minimum length in real time of a single game time tick. SA: TICK_MINUTES
TICK_REAL_TIME = 0.1

# This is how many game time minutes are in a clock tick. SA: TICK_REAL_TIME
TICK_MINUTES = 5
# How many game time minutes are in a game time hour?
MINUTES_PER = 60
# How many game time hours are in a game time day?
HOURS_PER = 24
# How many game time days are in a game time month?
DAYS_PER = 6
# How many game time months are in a game time year?
MONTHS_PER = 12

################### DONT CHANGE ANYTHING BELOW THIS LINE #######################

VERSION = '0.1'

BLACK = ( 0, 0, 0 )

# Rendering constants, translate stuff into pixels.
FLOOR_HEIGHT = 30
OBJECT_HEIGHT = 20
SLICE_WIDTH = 10

# Calculate useful constants based on map size
WINDOW_HEIGHT = WINDOW_FLOORS * FLOOR_HEIGHT
WINDOW_WIDTH = WINDOW_SLICES * SLICE_WIDTH
# TODO: Restore these
#CENTER = int( ( SLICES - WINDOW_SLICES ) / 2)
#BOTTOM = FLOORS - WINDOW_FLOORS - int( DIRT_FLOORS / 2 )
#MINI_HEIGHT = ( FLOOR_HEIGHT * FLOORS ) / 10
#MINI_WIDTH = SLICES