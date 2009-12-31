# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui

def showapp ():
	app = QtGui.QApplication( sys.argv )

	widget = QtGui.QLabel( 'Hello pyTower User!' )
	widget.resize( 250, 150 )
	widget.setWindowTitle('pyTower Qt4 User Interface')
	widget.show()

	sys.exit( app.exec_() )