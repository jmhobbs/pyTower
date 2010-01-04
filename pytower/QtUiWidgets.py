# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, Qt
import Constants
import Messages

if __name__ == "__main__":
	print "No Direct Invocation"
	exit()

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
		self.send_message( Messages.Message( Messages.NEWGAME ) )
		self.hide()
		self.emit( QtCore.SIGNAL( "quit()" ) )

	def do_quit ( self ):
		self.send_message( Messages.Message( Messages.QUIT ) )
		self.hide()
		self.emit( QtCore.SIGNAL( "quit()" ) )

	def do_about ( self ):
		dialog = QtGui.QDialog()
		dialog.setWindowTitle( "pyTower - About" )
		l = QtGui.QLabel( "pyTower\nVersion " + Constants.VERSION + "\nhttp://github.com/jmhobbs/pyTower" )
		v = QtGui.QVBoxLayout()
		v.addWidget( l, 1 )
		dialog.setLayout( v )
		dialog.exec_()

class in_game_menu ( MenuDialog ):
	def __init__ ( self, rq, sq, parent=None ):
		MenuDialog.__init__( self, rq, sq, 'pyTower Menu',  parent )

		self.resize( 250, 10 )

		quit = QtGui.QPushButton( "Quit" )
		QtCore.QObject.connect( quit, QtCore.SIGNAL( "clicked()" ), self.do_quit )
		about = QtGui.QPushButton( "About" )
		QtCore.QObject.connect( about, QtCore.SIGNAL( "clicked()" ), self.do_about )

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget( quit, 1 )
		vbox.addWidget( about, 1 )

		self.setLayout( vbox )

	def do_quit ( self ):
		self.send_message( Messages.Message( Messages.QUIT ) )
		self.hide()
		self.emit( QtCore.SIGNAL( "quit()" ) )

	def do_about ( self ):
		dialog = QtGui.QDialog()
		dialog.setWindowTitle( "pyTower - About" )
		l = QtGui.QLabel( "pyTower\nVersion " + Constants.VERSION + "\nhttp://github.com/jmhobbs/pyTower" )
		v = QtGui.QVBoxLayout()
		v.addWidget( l, 1 )
		dialog.setLayout( v )
		dialog.exec_()