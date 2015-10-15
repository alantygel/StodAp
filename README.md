# Tag Analysis of Open Data Portals

This repository holds the code of a Tag Analysis of Open Data Portals. It was used to generate data for the paper XXX, which is currently under review for ICSC2016.

## Description ##
The objective of this script is:
1) Collect the tags of Open Data Portals using CKAN;
2) Analyze Data.

### Data Collection ###

The data collection is done in the following order:
1) functions.LoadODPs()
Fill the OpenDataPortal class with the portals pointed by https://github.com/ckan/ckan-instances/blob/gh-pages/config/instances.json.

2) functions.LoadODPData()
Go trough each ODP and load the tags and other informations described by the model.

### Data Analysis ###

1) functions.CalculateStats()
Prints general statistics.

#functions.WriteWikiPages()
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


## Dependencies
Levenshtein, numpy,unidecode, urllib2, urllib, json, pprint, cPickle as pickle, rdflib

## Related Work
http://stodap.org/
https://github.com/alantygel/ckanext-tagmanager
https://github.com/alantygel/ckanext-semantictags
