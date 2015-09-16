import functions
import config
import cPickle as pickle

functions.LoadODPs()
#functions.LoadODPData()
#functions.WriteWikiPages()
#functions.CalculateStats()
#functions.TagsOverN(2)

#with open(config.objects_file, 'rb') as input:
#	ODP =  pickle.load(input)

#for o in ODP:
#	for tag in o.tags:
#		print "-------------------"
#		print tag.name		
#		tag.set_meaning()		
#		for m in tag.meanings:
#			print m

#with open(config.objects_file, 'wb') as output:
#	pickle.dump(ODP, output, -1)

