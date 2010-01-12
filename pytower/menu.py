# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

from PyQt4 import QtCore, QtGui
import QtUiWidgets as Widgets

def show_main_menu ( rq, sq ):
	app = QtGui.QApplication( [] )
	mm = Widgets.main_menu( rq, sq )
	mm.show()
	QtCore.QObject.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
	app.exec_()

def show_in_game_menu ( rq, sq ):
	app = QtGui.QApplication( [] )
	mm = Widgets.in_game_menu( rq, sq )
	mm.show()
	QtCore.QObject.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
	app.exec_()