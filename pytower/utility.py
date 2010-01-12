# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

import sys

def FullPath ( relpath ):
	"""
	Turns a relative path into a full path.  This only works from a file, not from
	the interactive prompt.
	"""
	return str( sys.path[0] ) + '/' + relpath