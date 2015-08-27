import functions
import config
import cPickle as pickle

functions.LoadODPs()
functions.LoadODPData()
functions.WriteWikiPages()
functions.CalculateStats()
#functions.TagsOverN(2)

#with open(config.objects_file, 'rb') as input:
#	ODP =  pickle.load(input)

#ODP[0].set_tag_count()

#for tag in ODP[0].tags:
#	print tag.name + ' - ' + str(tag.count)
