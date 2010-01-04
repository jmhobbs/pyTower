import yaml
from pprint import pprint
f = open( 'objects/office/default_office/object.yaml' )
dm = yaml.load( f )
f.close()
for i in dm['object']['sprites']:
	print i
pprint( dm )
