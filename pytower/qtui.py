# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
import constants

class main_menu ( QtGui.QWidget ):
	def __init__ ( self, rq, sq, parent=None ):
		QtGui.QWidget.__init__( self, parent )
		self.rq = rq
		self.sq = sq

		self.new_game = QtGui.QPushButton( "New Game" )
		QtCore.QObject.connect( self.new_game, QtCore.SIGNAL( "clicked()" ), self.do_new_game )

		self.quit = QtGui.QPushButton( "Quit" )
		QtCore.QObject.connect( self.quit, QtCore.SIGNAL( "clicked()" ), self.do_quit )

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget( self.new_game, 1 )
		vbox.addWidget( self.quit, 1 )

		self.setLayout( vbox )
		self.resize( 250, 10 )
		self.setWindowTitle('pyTower - Main Menu')
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

	def send_message ( self, message ):
		self.sq.put_nowait( message )

	def do_new_game ( self ):
		self.send_message( { 'instruction': 'NEWGAME' } )

	def do_quit ( self ):
		self.send_message( { 'instruction': 'QUIT' } )
		self.hide()
		self.emit( QtCore.SIGNAL( "quit()" ) )

def show_main_menu ( rq, sq ):
	app = QtGui.QApplication( sys.argv )
	mm = main_menu( rq, sq )
	mm.show()
	QtCore.QObject.connect( mm, QtCore.SIGNAL( "quit()" ), app.quit )
	app.exec_()