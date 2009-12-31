# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
import constants

class main_menu ( QtGui.QWidget ):
	def __init__ ( self, rq, sq, parent=None ):
		QtGui.QWidget.__init__( self, parent )
		self.rq = rq
		self.sq = sq
		self.label = QtGui.QLabel( 'Hello pyTower User!' )
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget( self.label )
		self.setLayout( hbox )
		self.resize( 400, 20 )
		self.setWindowTitle('pyTower Qt4 User Interface')
		self.ctimer = QtCore.QTimer()
		QtCore.QObject.connect( self.ctimer, QtCore.SIGNAL( "timeout()" ), self.check_queue )
		self.ctimer.start( constants.IPQUEUE_SLEEP )

	def check_queue ( self ):
		try:
			x = self.rq.get_nowait()
			self.label.setText( x )
			self.sq.put_nowait( "quit" )
		except:
			return


def show_main_menu ( rq, sq ):
	app = QtGui.QApplication( sys.argv )
	mm = main_menu( rq, sq )
	mm.show()
	app.exec_()