# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

VERSION = '0.1'

# DONT CHANGE THESE
FLOOR_HEIGHT = 40
SLICE_WIDTH = 10

# You can change these for more play space.
FLOORS = 110
SLICES = 300

# This is just visible area, you can change it
WINDOW_HEIGHT = 600 # 15 Floors
WINDOW_WIDTH = 800 # 80 slices

# 1px in mini == 10px full
MINI_HEIGHT = ( FLOOR_HEIGHT * FLOORS ) / 10
MINI_WIDTH = SLICES

IPQUEUE_SLEEP = 100
FRAME_LENGTH = 0.10