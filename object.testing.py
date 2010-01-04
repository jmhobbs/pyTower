import yaml
import os
from pprint import pprint

for root, dirs, files in os.walk( 'objects/' ):
	for file in files:
		if file == 'object.yaml':
			print '---- Found: ' + root + '/' + file + ' ----'
			f = open( root + '/' + file )
			dm = yaml.load( f )
			f.close()
			pprint( dm )
