# -*- coding: utf-8 -*-

from pytower.menus import Menus
from multiprocessing import Queue

sq = Queue()
rq = Queue()

menus = Menus( 'qt', sq, rq )
menus.main_menu()
menus.in_game_menu()
menus.join()

try:
	while True:
		print rq.get_nowait()
except:
	print "All Done"
