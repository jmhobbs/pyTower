# -*- coding: utf-8 -*-

import Globals
import Constants

def addFloorSlice ( rect ):
	if Globals.cash - Constants.FLOOR_SLICE_COST > 0: # Can we afford it?
		if rect[0] >= Constants.FLOORS - Constants.DIRT_FLOORS - 1 or Globals.game_map[rect[0]+1][rect[1]] != None:
			Globals.cash = Globals.cash - Constants.FLOOR_SLICE_COST
			Globals.game_map[rect[0]][rect[1]] = 0
			return True
	return False