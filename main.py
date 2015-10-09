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
#functions.WriteTagsCSV()
#functions.GetLanguage()
#functions.MostUsedTags()
#functions.LoadGlobalTags()


with open(config.global_tags_file, 'rb') as input:
	g =  pickle.load(input)

functions.WriteWikiPages(g)

#with open(config.objects_file, 'rb') as input:
#	ODP =  pickle.load(input)

#r = functions.find_in_tags(ODP, "health")

#for a in r:
#	print a
#for o in ODP:
#	print str(o.url) + " " + str(o.lang)
#	for tag in o.tags:
#		if [int(strj[i]) for i in range(0,len(tag.name)) if tag.name[i].isdigit()] == []:
#		tag.set_meaning_2(lang)		

#with open(config.objects_file, 'wb') as output:
#	pickle.dump(ODP, output, -1)
	

