from time import sleep, time
from optparse import OptionParser

parser = OptionParser()
parser.add_option( "-f", "--framesize", dest="FRAME_SIZE", default=5,
                  help="Game time frame size, in minutes", metavar="FRAME_SIZE", action="store", type="int")
parser.add_option("-s", "--sleep", dest="SLEEP", default=0.1,
                  help="Real time length of a frame, in seconds", metavar="SECONDS", action="store", type="float")

(opts, args) = parser.parse_args()

t = [ 0, 0, 0 ]
s = time()
f = 0
while True:
	f = f + 1
	t[2] = t[2] + opts.FRAME_SIZE
	if t[2] >= 60:
		t[1] = t[1] + 1
		t[2] = 0
	if t[1] >= 24:
		t[0] = t[0] + 1
		t[1] = 0
		print "Completed a day ( %d frames, %d GT minutes per frame )" % ( f, opts.FRAME_SIZE )
		print "RT Seconds Elapsed: %d - %f sleep per frame, total should be %d" % ( time() - s, opts.SLEEP, opts.SLEEP * f )
		s = time()
		f = 0
	print "%d, %02d:%02d" % ( t[0], t[1], t[2] )
	sleep( opts.SLEEP )
