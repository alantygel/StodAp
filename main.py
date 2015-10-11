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


#functions.LoadGlobalTags()

#with open(config.global_tags_file, 'rb') as input:
#	g =  pickle.load(input)

#for gg in g:
#	print '"' + gg.label + '"'

#functions.WriteWikiPages(g)


#r = functions.find_in_tags(ODP, "health")
#for a in r:
#	print a

with open(config.objects_file, 'rb') as input:
	ODP =  pickle.load(input)

#with open("ODP3.pkl.bkp2", 'rb') as input:
#	ODPb =  pickle.load(input)

#for k in range(0,len(ODP)):
#	o = 0
#	ob = 0
#	for t in range(0,len(ODP[k].tags)):
#		o += len(ODP[k].tags[t].meanings)
# 		ob += len(ODPb[k].tags[t].meanings)
#	print str(k) + " " + str(ODP[k].url) + " " + str(o) + " " + str(ob)
k = -1
for o in ODP:
	k += 1
	print str(o.url)
	if 	k > 19:
		o.set_language()
		for tag in o.tags:
			if ([int(tag.name[i]) for i in range(0,len(tag.name)) if tag.name[i].encode('utf-8').isdigit()] == []) and (len(tag.name)>3):
				time.sleep(.02)
				tag.set_meaning_2(o.lang)		

		with open(config.objects_file, 'wb') as output:
			pickle.dump(ODP, output, -1)
	

