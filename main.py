import functions
import config
import cPickle as pickle

#functions.LoadODPs()
#functions.LoadODPData()
#functions.WriteWikiPages()
#functions.CalculateStats()
#functions.TagsOverN(2)

#functions.TagsDistribution()
#functions.TagsPerDataset()
#functions.Similarity2()
#functions.WriteCSV()
#functions.GetLanguage()
with open(config.objects_file, 'rb') as input:
	ODP =  pickle.load(input)

for o in ODP:
	lang = o.get_language()	
	print str(o.url) + " " + str(lang)
	for tag in o.tags:
		tag.set_meaning_2(lang)		

	with open(config.objects_file, 'wb') as output:
		pickle.dump(ODP, output, -1)

