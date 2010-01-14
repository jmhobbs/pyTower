# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

from constants import *

def addFloorSlice ( rect, game ):
	if game.cash - FLOOR_SLICE_COST > 0: # Can we afford it?
		if rect[0] >= game.map.floors - game.map.dirt_floors - 1 or game.contents[rect[0]+1][rect[1]] != None:
			game.cash = game.cash - FLOOR_SLICE_COST
			game.contents[rect[0]][rect[1]] = 0
			return True
	return False