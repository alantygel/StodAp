#!/usr/bin/python
# -*- coding: utf-8 -*-

import functions
import config
import cPickle as pickle

#functions.CalculateStats()
#functions.GroupStats()	
#functions.TagsOverN(1)
#functions.TagsDistribution()
#functions.TagsPerDataset()
#functions.Similarity2('naive')
#functions.WriteTagsCSV()
#functions.GetLanguage()
#functions.MostUsedTags()
#functions.LoadGlobalTags()

#functions.SignificanceOfTagsWithMeaning()
#functions.WriteWikiPages()



with open(config.objects_file, 'rb') as input:
	ODP =  pickle.load(input)

ODP = ODP[1]
tag = ODP.tags[130]

print tag.name

cooccurences = []
datasets = []
for tg in ODP.tagging:
	if tg.tag_id == tag.tag_id:
		datasets.append(tg)

for dt in datasets:
	for tg in ODP.tagging:
		if dt.dataset_id == tg.dataset_id:
			cooccurences.append(tg.tag_id)

for co in cooccurences:
	for t in ODP.tags:
		if co == t.tag_id:
			print t.name
			break
