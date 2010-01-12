# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

from multiprocessing import Process, Queue
from Queue import Empty

class Menus ():
	def __init__ ( self, style, rx, tx ):
		self.menus = []
		self.style = style
		self.rx = rx
		self.tx = tx
		if 'qt' == style:
			global QtCore
			global QtGui
			global ui
			from PyQt4 import QtCore, QtGui
			import ui.qt as ui
		else:
			raise RuntimeError( 'Invalid menu style: ' + str( style ) )

	def join ( self ):
		for menu in self.menus:
			menu.join()

	def main_menu ( self ):
		"""
		Show the main menu, for new game, load game, etc.
		"""
		if self.style == 'qt':
			p = Process( target=self.qt_main_menu )
			p.start()
			self.menus.append( p )

	def in_game_menu ( self ):
		"""
		Show the in-game menu, for choosing cursors, showing values, etc.
		"""
		if self.style == 'qt':
			p = Process( target=self.qt_in_game_menu )
			p.start()
			self.menus.append( p )

	########## Qt Specific ##########
	def qt_main_menu ( self ):
		app = QtGui.QApplication( [] )
		mm = ui.main_menu( self.rx, self.tx )
		mm.show()
		mm.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
		app.exec_()

	def qt_in_game_menu ( self ):
		app = QtGui.QApplication( [] )
		mm = ui.in_game_menu( self.rx, self.tx )
		mm.show()
		mm.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
		app.exec_()