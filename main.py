import functions
import config
import cPickle as pickle
import time
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


functions.LoadGlobalTags()

with open(config.global_tags_file, 'rb') as input:
	g =  pickle.load(input)

functions.WriteWikiPages(g)


#r = functions.find_in_tags(ODP, "health")
#for a in r:
#	print a

#with open(config.objects_file, 'rb') as input:
#	ODP =  pickle.load(input)
#	k = 0
#	j = 0
#for o in ODP:
#	print str(o.url) + " " + str(o.lang)
#	for tag in o.tags:
#		k += 1
#		if ([int(tag.name[i]) for i in range(0,len(tag.name)) if tag.name[i].encode('utf-8').isdigit()] == []) and (len(tag.name)>3):
#			#time.sleep(.2)
#			j += 1
#			tag.set_meaning_2(o.lang)		
#	print str(k) + " " + str(j)

#	with open(config.objects_file, 'wb') as output:
#		pickle.dump(ODP, output, -1)
#	

