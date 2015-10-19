# Tag Analysis of Open Data Portals

This repository holds the code of a Tag Analysis of Open Data Portals. It was used to generate data for the paper Towards Cleaning-up Open Data Portals: A Metadata Reconciliation Approach, which is currently under review for ICSC2016.

## Description
The objective of this script is:

1) Collect the tags of Open Data Portals using 

2) Analyze Data.

To reproduce the results described in the paper, run the Analysis module using data previously. If you collect data again, results will differ because site are frequently updated.

### Data Collection

The data collection is done in the following order:
#### functions.LoadODPs()
Fill the OpenDataPortal class with the portals pointed by https://github.com/ckan/ckan-instances/blob/gh-pages/config/instances.json.

#### functions.LoadODPData()
Go trough each ODP and load the tags and other informations described by the model.

### Data Analysis

###functions.CalculateStats()
Prints general statistics.

####functions.TagsOverN(n)
Prints the number of tags used more than n times. Generates mfiles.

####functions.WriteWikiPages()
Writes the pages to be uploaded in http://stodap.org.

####functions.TagsDistribution()
Writes the distribution of tags among the portal. Generates mfiles.

####functions.TagsPerDataset()
Writes the distribution of tags per datasets in each portal. Generates mfiles.

####functions.Similarity2(method)
Calculates the similarity between tags a same portal.

####functions.WriteTagsCSV()
Writes CSV file with all tags.

####functions.MostUsedTags()
Writes CSV file with most used tags among the ODPs.

####functions.LoadGlobalTags()
Load the Global Tags, to be written in the Tag Server.

####functions.GroupStats()
Prints the statistics about groups.

####functions.SignificanceOfTagsWithMeaning()
Prints the proportion of tags connected to semantic resources, in absoulte number and weighted by usage.

## Dependencies
Levenshtein, numpy,unidecode, urllib2, urllib, json, pprint, cPickle as pickle, rdflib, pycountry

## Related Work
http://stodap.org/
https://github.com/alantygel/ckanext-tagmanager
https://github.com/alantygel/ckanext-semantictags
