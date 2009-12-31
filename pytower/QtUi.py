# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import QtUiWidgets as Widgets

if __name__ == "__main__":
	print "No Direct Invocation"
	exit()

def show_main_menu ( rq, sq ):
	app = QtGui.QApplication( [] )
	mm = Widgets.main_menu( rq, sq )
	mm.show()
	QtCore.QObject.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
	app.exec_()