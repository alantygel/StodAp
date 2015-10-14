#!/usr/bin/python
# -*- coding: utf-8 -*-

import functions
import model
import config
import cPickle as pickle
import time
#functions.LoadODPs()
#functions.LoadODPData()
#functions.WriteWikiPages()
#functions.CalculateStats()
#functions.TagsOverN(1)

#functions.TagsDistribution()
#functions.TagsPerDataset()
#functions.Similarity2('naive')
#functions.WriteTagsCSV()
#functions.GetLanguage()
#functions.MostUsedTags()
#functions.LoadGlobalTags()
#functions.GroupStats()
#functions.SignificanceOfTagsWithMeaning()

#with open(config.global_tags_file, 'rb') as input:
#	g =  pickle.load(input)

#for gg in g:
#	print '"' + gg.label + '"'
#	for ggg in gg.local_tags:
#		print ">>>" + ggg.url + " " + ggg.name



#with open(config.objects_file, 'rb') as input:
#        ODP =  pickle.load(input)

#with open("ODP3.pkl-12-10manha", 'rb') as input:
#        ODPb =  pickle.load(input)

#x = 0
#for k in range(0,len(ODP)):
#        a = sum(map(lambda z: len(z.meanings), ODP[k].tags))
#        b = sum(map(lambda z: len(z.meanings), ODPb[k].tags))
#        print str(k) + " " + ODP[k].url + " " + str(a) + " " + str(b)




#with open(config.objects_file, 'rb') as input:
#	ODP =  pickle.load(input)
#r = functions.find_in_tags(ODP, "education")
#for a in r:
#	print a

#with open(config.objects_file, 'rb') as input:
#	ODP =  pickle.load(input)

#groups = []
#for o in ODP:
#	print o.url
#	oo = model.OpenDataPortal(o.url, o.name, None, None)
#	oo.load_groups()
#	groups.append(oo)
#	print ">>>> " + str(len(oo.groups))
#	
#	with open(config.groups_file, 'wb') as output:
#		pickle.dump(groups, output, -1)


#r = functions.find_in_tags(ODP,"saúde")
#print len(r)

#r = functions.find_in_tags(ODP,"Saude")
#print len(r)

#with open("ODP3.pkl.bkp2", 'rb') as input:
#	ODPb =  pickle.load(input)

#for k in range(0,len(ODP)):
#	o = 0
#	ob = 0
#	for t in range(0,len(ODP[k].tags)):
#		o += len(ODP[k].tags[t].meanings)
# 		ob += len(ODPb[k].tags[t].meanings)
#	print str(k) + " " + str(ODP[k].url) + " " + str(o) + " " + str(ob)
#k = -1
#for o in ODP:
##	k += 1
#	print str(o.url)
#	try:
#		print o.lang
#	except:
#		if o.url == "http://portal.openbelgium.be":
#			o.lang = None
#		if o.url == "http://datosabiertos.ec":
#			o.lang = "esp"
#		if o.url == "http://udct-data.aigid.jp":
#			o.lang = "jpn"
#		if o.url == "http://data.wu.ac.at":
#			o.lang = "deu"
#	if 	k > 19:
#		o.set_language()
#		for tag in o.tags:
#			if ([int(tag.name[i]) for i in range(0,len(tag.name)) if tag.name[i].encode('utf-8').isdigit()] == []) and (len(tag.name)>3):
#				time.sleep(.02)
#				tag.set_meaning_2(o.lang)		

#		with open(config.objects_file, 'wb') as output:
#			pickle.dump(ODP, output, -1)
#	


#import rdflib
#from rdflib import URIRef
#from rdflib import Graph
#import urllib2
#import urllib

#means = URIRef("http://lexvo.org/ontology#means")
#seeAlso = URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso")
#abstract = URIRef("http://dbpedia.org/ontology/abstract")
#with open(config.global_tags_file, 'rb') as input:
#	global_tags =  pickle.load(input)

#for tag in global_tags:
#	g = Graph()
#	parse = True		
#	try:
#		#print "http://www.lexvo.org/data/term/" + lang + "/" + urllib.quote(self.name.encode('utf-8'))
#		g.parse("http://dbpedia.org/data/" + urllib.quote(tag.label.capitalize().encode('utf-8')))
#	except:
#		parse = False
#	
#	print urllib.quote(tag.label.capitalize().encode('utf-8'))

#	if parse:
#		#out = self.name.encode('utf-8')
#		
#		for s,p,o in g.triples((None,abstract,None)):
#			if o.language == "en":			
#				#print o
#				tag.description = o

#with open(config.global_tags_file, 'wb') as output:
#	pickle.dump(global_tags, output, -1)



functions.WriteWikiPages()
