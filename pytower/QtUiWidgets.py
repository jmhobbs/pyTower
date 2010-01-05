# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, Qt
from Queue import Empty
import Constants
import Messages
import locale

if __name__ == "__main__":
	print "No Direct Invocation"
	exit()

def about ( obj ):
	QtGui.QMessageBox.about( obj, "pyTower - About", "pyTower " + Constants.VERSION + "\n\nCopyright 2010, John Hobbs\nhttp://github.com/jmhobbs/pyTower" )

class MenuDialog ( QtGui.QWidget ):
	def __init__ ( self, rq, sq, title=None, parent=None ):
		QtGui.QWidget.__init__( self, parent )

		self.rq = rq
		self.sq = sq

		if str == type( title ):
			self.setWindowTitle( 'pyTower - ' + title )
		else:
			self.setWindowTitle( 'pyTower' )

		self.setWindowIcon( QtGui.QIcon( 'resources/icon.16x16.png' ) )

		self.timer = QtCore.QTimer()
		QtCore.QObject.connect( self.timer, QtCore.SIGNAL( "timeout()" ), self.check_messages )
		self.timer.start( Constants.IPQUEUE_SLEEP )

	def closeEvent ( self, event ):
		event.ignore();

	def send_message ( self, message ):
		self.sq.put_nowait( message )

	def check_messages ( self ):
		try:
			while True:
				x = self.rq.get_nowait()
				print "UI - RX:", x
		except:
			return

class main_menu ( MenuDialog ):
	def __init__ ( self, rq, sq, parent=None ):
		MenuDialog.__init__( self, rq, sq, 'Main Menu',  parent )

		self.resize( 250, 10 )

		new_game = QtGui.QPushButton( "New Game" )
		QtCore.QObject.connect( new_game, QtCore.SIGNAL( "clicked()" ), self.do_new_game )
		quit = QtGui.QPushButton( "Quit" )
		QtCore.QObject.connect( quit, QtCore.SIGNAL( "clicked()" ), self.do_quit )
		about = QtGui.QPushButton( "About" )
		QtCore.QObject.connect( about, QtCore.SIGNAL( "clicked()" ), self.do_about )

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget( new_game, 1 )
		vbox.addWidget( quit, 1 )
		vbox.addWidget( about, 1 )

		self.setLayout( vbox )

	def do_new_game ( self ):
		self.send_message( Messages.Message( Messages.NEW_GAME ) )
		self.hide()
		self.emit( QtCore.SIGNAL( "quit()" ) )

	def do_quit ( self ):
		self.send_message( Messages.Message( Messages.QUIT ) )
		self.hide()
		self.emit( QtCore.SIGNAL( "quit()" ) )

	def do_about ( self ):
		about( self )

class in_game_menu ( MenuDialog ):
	def __init__ ( self, rq, sq, parent=None ):
		MenuDialog.__init__( self, rq, sq, 'pyTower Menu',  parent )

		locale.setlocale( locale.LC_ALL, '' )

		self.resize( 250, 10 )

		quit = QtGui.QPushButton( "Quit" )
		QtCore.QObject.connect( quit, QtCore.SIGNAL( "clicked()" ), self.do_quit )
		about = QtGui.QPushButton( "About" )
		QtCore.QObject.connect( about, QtCore.SIGNAL( "clicked()" ), self.do_about )

		self.time_label = QtGui.QLabel( '' )
		self.cash_label = QtGui.QLabel( '' )
		self.population_label = QtGui.QLabel( '' )

		hbox = QtGui.QHBoxLayout()

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget( self.time_label )
		vbox.addWidget( self.cash_label )
		vbox.addWidget( self.population_label )
		vbox.addLayout( hbox )
		vbox.addWidget( quit, 1 )
		vbox.addWidget( about, 1 )

		cursor_button = QtGui.QPushButton( QtGui.QIcon( 'resources/in_game_menu/cursor.png' ), '' )
		QtCore.QObject.connect( cursor_button, QtCore.SIGNAL( "clicked()" ), self.set_cursor )
		self.pause_button = QtGui.QPushButton( QtGui.QIcon( 'resources/in_game_menu/pause.png' ), '' )
		QtCore.QObject.connect( self.pause_button, QtCore.SIGNAL( "clicked()" ), self.play_pause )
		hbox.addWidget( cursor_button )
		hbox.addWidget( self.pause_button )

		self.paused = False

		self.setLayout( vbox )

	def check_messages ( self ):
		try:
			while True:
				x = self.rq.get_nowait()
				if Messages.NOTIFY_TIME == x.instruction:
					self.time_label.setText( "%02d:%02d - Day %d, Month %d, Year %d" % ( x.time[3], x.time[4], x.time[2], x.time[1], x.time[0] ) )
				elif Messages.NOTIFY_CASH == x.instruction:
					self.cash_label.setText( locale.currency( x.cash, grouping=True ) )
				elif Messages.NOTIFY_POPULATION == x.instruction:
					self.population_label.setText( str( x.population ) )
				else:
					print "UI - RX:", x
		except Empty:
			return

	def set_cursor ( self ):
		m = Messages.Message( Messages.SET_CURSOR )
		m.cursor = None
		self.send_message( m )

	def play_pause ( self ):
		if self.paused:
			self.pause_button.setIcon( QtGui.QIcon( 'resources/in_game_menu/pause.png' ) )
			self.send_message( Messages.Message( Messages.PLAY ) )
			self.paused = False
		else:
			self.pause_button.setIcon( QtGui.QIcon( 'resources/in_game_menu/play.png' ) )
			self.send_message( Messages.Message( Messages.PAUSE ) )
			self.paused = True

	def do_quit ( self ):
		self.send_message( Messages.Message( Messages.QUIT ) )
		self.hide()
		self.emit( QtCore.SIGNAL( "quit()" ) )

	def do_about ( self ):
		about( self )
