# -*- coding: utf-8 -*-

from pytower.menu import Menus
from multiprocessing import Process, Queue

sq = Queue()
rq = Queue()

menus = Menus( 'qt' )

p = Process( target=menus.in_game_menu, args=( sq, rq ) )
p.start()
p.join()

try:
	while True:
		print rq.get_nowait()
except:
	print "All Done"
