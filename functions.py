##########################################################
#This scripts walks through several CKAN instances given by the CKAN instances project (https://github.com/ckan/ckan-instances/blob/gh-pages/config/instances.json) and collects information about the portals, the datasets, and tags. Data are stored as objects of the class Open Data Portal.

#This script outputs a file that is suitable to be inserted in a (semantic) media wiki instance.
##########################################################
import config
import model

import urllib2
import urllib
import json
import pprint
import cPickle as pickle

def LoadODPs():
	"Reads the instance files, and initialize a list of ODP objects"

	ODP = []

	with open(config.instances_file, 'r') as f:
		instances = json.loads(f.read())

	for i in instances:
		try: 
			response = urllib2.urlopen(i['url'] + '/api/3/action/tag_list')
			response_pkg = urllib2.urlopen(i['url'] + '/api/3/action/package_list')
		except:
			print "Could not connect"
			response = 0
		if response:
			try:		
				response_dict = json.loads(response.read())	
				result = response_dict['result']

				response_dict_pkg = json.loads(response_pkg.read())	
				packages = response_dict_pkg['result']

				ODP.append(model.OpenDataPortal(i['url'], i['title'], len(result), len(packages)))
				#print i['title'] + ';' + i['url'] + ';' + str(len(result)) + ';' + str(len(packages))

			except:
				print i['title'] + ';' + i['url'] + ';' + 'No API 1'	
			
		else:
			print i['title'] + ';' + i['url'] + ';' + 'No API 2'
	

	with open(config.objects_file, 'wb') as output:
		pickle.dump(ODP, output, -1)

def LoadODPData():
	"loop through all portals in ODP and load data - tags, dataset, tagging"

	with open(config.objects_file, 'rb') as input:
		 ODP =  pickle.load(input)

	for o in ODP:
		o.load_data()
		with open(config.objects_file, 'wb') as output:
			pickle.dump(ODP, output, -1)
		
def WriteWikiPages():
	"write wiki pages - Tagging, Tag, Portal and Dataset"

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	pages_ODP = open(config.wiki_out_file, 'wb')

	for o in ODP:
		# write portal page
		pages_ODP.write('Portal:' + o.name.encode('utf-8') + '\n\n')
		pages_ODP.write('--ENDTITLE--\n\n')

		pages_ODP.write('Type: [[rdf:Type :: tagont:ServiceDomain]]			\n\n')
 		pages_ODP.write('== Taggings == \n\n')

		pages_ODP.write('{{#ask: 											\n\n')
		pages_ODP.write('  [[rdf:type :: tags:RestrictedTagging]]				\n\n')
		pages_ODP.write('  [[tagont:hasServiceDomain :: Portal:' + o.name.encode('utf-8') + ']]		\n\n')
		pages_ODP.write('  |?tags:associatedTag								\n\n')
		pages_ODP.write('}}													\n\n')
		pages_ODP.write('--ENDPAGE--\n\n')

		# write tagging pages
		for t in o.tagging:
			tag_name = [tag.name for tag in o.tags if tag.tag_id == t.tag_id]
			dataset_name = [dataset.name for dataset in o.datasets if dataset.dataset_id == t.dataset_id]

			pages_ODP.write('Tagging:' + t.tag_id + '-' + t.dataset_id + '\n\n')
			pages_ODP.write('--ENDTITLE--\n\n\n')
			pages_ODP.write('Type: [[rdf:type :: tags:RestrictedTagging]]	\n\n')
			pages_ODP.write('Tagged Resource: [[tags:taggedResource :: Dataset:' + dataset_name[0].encode('utf-8') + ']]	\n\n')
			pages_ODP.write('Tagged Domain: [[tagont:hasServiceDomain :: Portal:' + o.name + ']]		\n\n')
			#pages_ODP.write('Meaning: {{#set: moat:tagMeaning=http://sws.geonames.org/3408096/}} [http://sws.geonames.org/3408096/ http://sws.geonames.org/3408096/]
			pages_ODP.write('Tag: [[tags:associatedTag :: Tag:' + tag_name[0].encode('utf-8') + ']]	\n\n')
			pages_ODP.write('--ENDPAGE--\n\n\n')

		# write dataset pages
		for d in o.datasets:
			pages_ODP.write('Dataset:' + d.name.encode('utf-8') + '\n\n')
			pages_ODP.write('--ENDTITLE--\n\n\n')
			pages_ODP.write('Type: [[rdf:type :: StodAp:Dataset]]	\n\n')

	 		pages_ODP.write('== Tags == \n\n')
			pages_ODP.write('{{#ask: 											\n\n')
			pages_ODP.write('  [[rdf:type :: tags:RestrictedTagging]]				\n\n')
			pages_ODP.write('  [[tagont:taggedResource :: Dataset:' + d.name.encode('utf-8') + ']]		\n\n')
			pages_ODP.write('  |?tags:associatedTag=Tag								\n\n')
			pages_ODP.write('}}													\n\n')

			pages_ODP.write('== Related Datasets == \n\n')
			#TODO all datasets with the same tags

			pages_ODP.write('--ENDPAGE--\n\n\n')
		# write tags pages
		for t in o.tags:
			pages_ODP.write('Tag:' + t.name.encode('utf-8') + '\n\n')
			pages_ODP.write('--ENDTITLE--\n\n')
			pages_ODP.write('Type: [[rdf:type::tags:Tag]]	\n\n')

			pages_ODP.write('== Meanings == \n\n')

			pages_ODP.write('{{#ask: \n\n')
			pages_ODP.write('  [[rdf:type :: tags:RestrictedTagging]]\n\n')
			pages_ODP.write('  [[tags:associatedTag :: Tag:' + t.name.encode('utf-8') + ']]\n\n')
			pages_ODP.write('  |?moat:tagMeaning\n\n')
			pages_ODP.write('}}\n\n')


			pages_ODP.write('== Datasets and Portals == \n\n')

			pages_ODP.write('{{#ask: \n\n')
			pages_ODP.write('  [[rdf:type::tags:RestrictedTagging]]\n\n')
			pages_ODP.write('  [[tags:associatedTag :: Tag:' + t.name.encode('utf-8') + ']]\n\n')
			pages_ODP.write('  |?tags:taggedResource \n\n')
			pages_ODP.write('  |?tagont:hasServiceDomain\n\n')
			pages_ODP.write('}} \n\n')
			pages_ODP.write('--ENDPAGE--\n\n')


	pages_ODP.close

def CalculateStats():
	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	print 'Number of portals: ' + str(len(ODP))

	x = 0; y = 0; z = 0;
	for o in ODP:
		x = x + o.num_of_tags
		y = y + o.num_of_packages
		z = z + len(o.tagging)	

	print 'Number of tags: ' , str(x)
	print 'Number of packages: ' , str(y)
	print 'Number of taggings: ' , str(z)

	all_tags, unique_tags = CalculateUniqueTags()

	print 'Number of loaded tags: ' , str(len(all_tags))
	print 'Number of unique tags: ' , str(len(unique_tags))

def CalculateUniqueTags():
	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	all_tags = []
	unique_tags = []

	for o in ODP:
		for t in o.tags:
			all_tags.append(str(t.name.encode('utf-8')))

	srtd = sorted(all_tags,key=str.lower)

	unique_tags.append(srtd[0].lower().strip())

	for t in srtd:
		if t.lower().strip() != unique_tags[len(unique_tags)-1]:
			unique_tags.append(t.lower().strip())

	return all_tags, unique_tags

def TagsOverN(N):

	mfile = open('percentage_over_' + str(N) + '.m', 'w')
	mfile.write ('tags_over_n = ['  + '\n')

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	tags_over_n_perc = []
	for o in range(0,len(ODP)):
		tags_over_n = 0
		for t in ODP[o].tags:
			if int(t.count) > N:
				tags_over_n += 1
		if len(ODP[o].tags) != 0:
			res = float(tags_over_n)/float(len(ODP[o].tags))
		else:		
			res = 0

		tags_over_n_perc.append(res)
		mfile.write (str(o) + ' ' + str(res) + '\n')

	mfile.write ('];')
	mfile.close()
	tags_over_n_perc = sorted (tags_over_n_perc)
	return tags_over_n_perc	


