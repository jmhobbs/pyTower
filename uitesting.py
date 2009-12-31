# -*- coding: utf-8 -*-

import pytower.qtui as pytower_ui
from multiprocessing import Process, Queue

sq = Queue()
rq = Queue()

p = Process( target=pytower_ui.show_main_menu, args=( sq, rq ) )
p.start()
p.join()

try:
	while True:
		print rq.get_nowait()
except:
	print "All Done"