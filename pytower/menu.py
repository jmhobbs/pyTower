# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

class Menus ():
	def __init__ ( self, style ):
		self.style = style
		if 'qt' == style:
			global QtCore
			global QtGui
			global ui
			from PyQt4 import QtCore, QtGui
			import ui.qt as ui
		else:
			raise RuntimeError( 'Invalid menu style: ' + str( style ) )

	def main_menu ( self, rx, tx ):
		"""
		Show the main menu, for new game, load game, etc.
		"""
		if self.style == 'qt':
			self.qt_main_menu( rx, tx )

	def in_game_menu ( self, rx, tx ):
		"""
		Show the in-game menu, for choosing cursors, showing values, etc.
		"""
		if self.style == 'qt':
			self.qt_in_game_menu( rx, tx )

	########## Qt Specific ##########
	def qt_main_menu ( self, rx, tx ):
		app = QtGui.QApplication( [] )
		mm = ui.main_menu( rx, tx )
		mm.show()
		mm.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
		app.exec_()

	def qt_in_game_menu ( self, rx, tx ):
		app = QtGui.QApplication( [] )
		mm = ui.in_game_menu( rx, tx )
		mm.show()
		mm.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
		app.exec_()