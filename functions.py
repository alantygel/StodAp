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
import numpy
import lib
from unidecode import unidecode
import Levenshtein

def LoadODPs():
	"Reads the instance files, and initialize a list of ODP objects"

	ODP = []

	with open(config.instances_file, 'r') as f:
		instances = json.loads(f.read())

	print 'Number of instances: ' + str(len(instances))

	for i in instances:
		if 'url-api' in i:
			url = i['url-api']
		else:
			url = i['url']

		try: 
			response = lib.urlopen_with_retry(url + '/api/3/action/tag_list')
			response_pkg = lib.urlopen_with_retry(url + '/api/3/action/package_list')
		except:
			#print "Could not connect"
			response = 0
		if response:
			try:		
				response_dict = json.loads(response.read())	
				result = response_dict['result']

				response_dict_pkg = json.loads(response_pkg.read())	
				packages = response_dict_pkg['result']

				ODP.append(model.OpenDataPortal(url, i['title'], len(result), len(packages)))
				#print i['title'] + ';' + i['url'] + ';' + str(len(result)) + ';' + str(len(packages))

			except:
				print i['title'] + ';' + url + ';' + 'No API 1'	
			
		else:
			print i['title'] + ';' + url + ';' + 'No API 2'
	

	with open(config.objects_file, 'wb') as output:
		pickle.dump(ODP, output, -1)

def LoadODPData():
	"loop through all portals in ODP and load data - tags, dataset, tagging"

	with open(config.objects_file, 'rb') as input:
		 ODP =  pickle.load(input)

	for o in ODP:
		if len(o.tags) == 0:
			print "process" + o.url
			o.load_data()
			with open(config.objects_file, 'wb') as output:
				pickle.dump(ODP, output, -1)
		else:
			print o.url + "already processed"

def CalculateStats():
	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	print 'Number of portals: ' + str(len(ODP))

	x = 0; y = 0; z = 0; ld = 0;
	tags_per_ds = []
	tags_with_meaning = []
	tags = []
	datasets = []
	for o in ODP:
		if o.num_of_tags == len(o.tags):
			x = x + o.num_of_tags
			y = y + o.num_of_packages
			z = z + len(o.tagging)	
			ld = ld + len(o.datasets)
			tags_per_ds.append(o.tags_per_dataset_mean())
			tags_with_meaning.append(o.tags_with_meaning())
			tags.append(o.num_of_tags)
			datasets.append(o.num_of_packages)
#		else:
#			print "Diff: " + o.url + ": " + str(o.num_of_tags) + " - " + str(len(o.tags))

	tags = numpy.array(tags);
	datasets = numpy.array(datasets);

	print 'Number of tags: ' , str(x)
	print 'Average tag number: ' + str(tags.mean()) + '+/-' + str(tags.std())
	print 'Number of datasets: ' , str(y)
	print 'Average dataset number: ' + str(datasets.mean()) + '+/-' + str(datasets.std())

	all_tags, unique_tags = CalculateUniqueTags()

	print 'Number of loaded taggings: ' , str(z)
	print 'Number of loaded tags: ' , str(len(all_tags))
	print 'Number of loaded datasets: ' , str(ld)
	print 'Number of loaded unique tags: ' , str(len(unique_tags))

	tags_per_ds = numpy.array(tags_per_ds);
	tags_with_meaning = numpy.array(tags_with_meaning);		

	print "------"
	print("Tags per dataset (av.): %.2f" % tags_per_ds.mean())
	print("Tags per dataset (max): %.2f" % tags_per_ds.max())
	print("Tags per dataset (min): %.2f" % tags_per_ds.min())
	print "------"
	print("Tags with meaning (av.): %.2f" % tags_with_meaning.mean())
	print("Tags with meaning (max): %.2f" % tags_with_meaning.max())
	print("Tags with meaning (min): %.2f" % tags_with_meaning.min())

	tg = 0
	N = 0
	no_groups =0
	ds_group = []
	for o in ODP:
		if len(o.groups) > 0:
			tg += len(o.groups)
			N += 1
			for g in o.groups:
				if g.n_datasets > 0:
					ds_group.append(g.n_datasets)
		else:
			no_groups += 1
	
	ds_group = numpy.array(ds_group);

	print "------"
	print 'Number of groups: ' , str(tg)
	print 'ODP without groups: ' , str(no_groups)
	print 'Groups / ODP: ' , str(tg/float(N))
	print 'Datasets / Group: ' , ds_group.mean()



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

	mfile_m = open('percentage_over_' + str(N) + '_merged.m', 'w')
	mfile_m.write ('tags_over_n_merged = ['  + '\n')

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

		av_reuse = sum(map(lambda z: z.count, ODP[o].tags))/float(len(ODP[o].tags))

		tags_over_n_perc.append(res)
		mfile.write (str(tags_over_n) + ' ' + str(res) + " " + str(av_reuse) +'\n')

		# merge similar tags
		alltags = []
		odp = ODP[o]	
		for t in odp.tags:
			alltags.append(model.AllTags(t.name,odp.url,t.count,odp.lang))
		alltags = sorted(alltags,key=lambda x: x.name)

		k = 0
		print odp.url
		while k < len(alltags)-1:
			if (unidecode(alltags[k].name.lower()) == unidecode(alltags[k+1].name.lower())):
				alltags[k].count += alltags[k+1].count
				alltags.remove(alltags[k+1])
				k -= 1		
			k += 1
			#print str(k) + " " + str(len(list))

		tags_over_n = 0
		for t in alltags:
			if int(t.count) > N:
				tags_over_n += 1
		if len(alltags) != 0:
			res2 = float(tags_over_n)/float(len(alltags))
		else:		
			res2 = 0

		av_reuse_m = sum(map(lambda z: z.count, alltags))/float(len(alltags))
		print av_reuse_m

		mfile_m.write (str(tags_over_n) + ' ' + str(res2) +  " " + str(av_reuse_m) + '\n')

	mfile.write ('];')
	mfile.close()

	mfile_m.write ('];')
	mfile_m.close()

	tags_over_n_perc = sorted (tags_over_n_perc)
	return tags_over_n_perc	

def WriteODPCSV():

	with open(config.objects_file, 'rb') as input:
                ODP =  pickle.load(input)


	csv_file = open(config.objects_file + '.csv', 'w')
	csv_file.write("Name ; URL ; Number of Tags ; Very similar tags ; Number of Packages; Tags per dataset (mean) ; Tags with meaning\n")
		
	for k in range(0,len(ODP)):
		o = ODP[k]
		sim = Similarity_ODP(k)
		csv_file.write(o.name.encode('utf-8') + ";"+ o.url.encode('utf-8') + ";" + str(o.num_of_tags).encode('utf-8') + ";" + str(sim) + ";"+ str(o.num_of_packages).encode('utf-8') + ";" + str(o.tags_per_dataset_mean()).encode('utf-8') + ";" + str(o.tags_with_meaning()).encode('utf-8') + "\n")
	
	csv_file.close()	

def WriteTagsCSV():

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	csv_file = open(config.objects_file + '.tags.csv', 'w')

	csv_file.write("URL ; Tag ; Count ; Meanings\n")
		
	for k in range(0,len(ODP)):
		o = ODP[k]
		for t in o.tags:
			csv_file.write(o.url.encode('utf-8') + ";" + t.name.encode('utf-8') + ";" + str(t.count))
			for m in t.meanings:
				csv_file.write(";" + m)
			csv_file.write("\n")				

	csv_file.close()	
	
def MostUsedTags():

	with open(config.objects_file, 'rb') as input:
                ODP =  pickle.load(input)

	csv_file = open(config.objects_file + '.most_used_tags.csv', 'w')
	csv_file.write("Tags ; URLs ; Count (times) ; Count (ODPs) \n")
			
	alltags = []	

	for o in ODP:
		for t in o.tags:
			alltags.append(model.AllTags(t.name,o.url,t.count,o.lang))


	alltags = sorted(alltags,key=lambda x: x.name)

	all_unique = [alltags[0]]
	s = 0
	for k in range(0,len(alltags)-1):
		if (unidecode(alltags[k].name.lower()) != unidecode(alltags[k+1].name.lower())):
			all_unique.append(alltags[k+1])
			s += 1
		else:
			if alltags[k].url != alltags[k+1].url:
				all_unique[s].global_count += 1
				all_unique[s].url.append(alltags[k+1].url)
				if alltags[k].lang != alltags[k+1].lang:
					all_unique[s].lang += ";" + alltags[k+1].lang
			all_unique[s].count += alltags[k+1].count

	all_unique = sorted(all_unique,key=lambda x: x.global_count, reverse = True)

	for t in all_unique:
		#url = ' '.join(t.url).encode('utf-8')
		#csv_file.write(t.name.encode('utf-8') + ";" + str(url) + ";" + str(t.count) + ";" + str(t.global_count) + "\n")
		csv_file.write(t.name.encode('utf-8') + ";" + ";" + str(t.count) + ";" + str(t.global_count) + "\n")	
	csv_file.close()
	return alltags, all_unique

def TagsDistribution():

	mfile = open('tags_distibution.m', 'w')

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	k = 0;
	for o in ODP:
		if len(o.tags) > 0:
			k += 1
			mfile.write('tags_distibution{' + str(k) +  '} = [\n')
			for t in o.tags:
				mfile.write(str(t.count) + '\n')
			mfile.write('];\n')

	mfile.close()

def TagsPerDataset():

	mfile = open('tags_perdataset.m', 'w')

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	k = 0;
	for o in ODP:
		if len(o.datasets) > 0:
			k += 1
			mfile.write('tags_per_dataset{' + str(k) +  '} = [\n')
			for d in o.datasets:
				mfile.write(str(d.number_of_tags) + '\n')
			mfile.write('];\n')

	mfile.close()
def Similarity():

	mfile = open('similarity.m', 'w')

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	k = 0
	for o in ODP:
		m = o.similarity_matrix()
		return
		k +=1
		s = 0
		mfile.write('similarity{' + str(k) +  '} = [\n')	
		for i in range(0,len(o.tags)):
			for j in range(0,len(o.tags)):
				if m[i][j] == 1:
					s += 1
		
		mfile.write(str(s) +  '] \n')	
				

#		for i in range(0,len(o.tags)):
#			for j in range(0,len(o.tags)):
#				mfile.write(str(m[i][j]) + ' ')	
#			mfile.write('\n')	
#		mfile.write('];\n')
	mfile.close()

def Similarity2(method = 'naive'):

	mfile = open('similarity_' + method + '.m', 'w')

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)


	mfile.write('similarity = [\n')	
	for o in ODP:
		s = 0
		srtd = sorted(map(lambda z: z.name.encode('utf-8'), o.tags),key=str.lower)
		for i in range(1,len(o.tags)):
			if method == 'naive':
				if unidecode(srtd[i].lower()) == unidecode(srtd[i-1].lower()):
					#print o.tags[i].name.encode('utf-8') + " " + o.tags[j].name.encode('utf-8')
					s +=1
			else:
				if Levenshtein.distance(unidecode(srtd[i].lower()),unidecode(srtd[i-1].lower())) < 3:
					s +=1					
				
		
		mfile.write(o.url + " " + str(s) + ' ' + str(float(s)/len(o.tags)) + " " + str(len(o.tags)) + '\n')	
		print o.name
	mfile.write('];\n')				

#		for i in range(0,len(o.tags)):
#			for j in range(0,len(o.tags)):
#				mfile.write(str(m[i][j]) + ' ')	
#			mfile.write('\n')	
#		mfile.write('];\n')
	mfile.close()

def Similarity_ODP(odp):
	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	s = 0
	o = ODP[odp]
	srtd = sorted(map(lambda z: z.name.encode('utf-8'), o.tags),key=str.lower)
	for i in range(1,len(o.tags)):
		if unidecode(srtd[i].lower()) == unidecode(srtd[i-1].lower()):
					#print o.tags[i].name.encode('utf-8') + " " + o.tags[j].name.encode('utf-8')
			s +=1
	
	
	return s

def LoadGlobalTags():
	'''	
	This function creates an array of AllTags. Each element is the name of a tag, and stores the urls where it is used, including translated versions. 
	This array is the used to generate a wiki page.
	'''
	print "#step 1: get most used tags"	
	all_tags, most_used = MostUsedTags()

	print "#step 2: start the Global Tags Dataset"	
	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	global_tags = []

	for i in range(0,200):
		G = model.GlobalTag(most_used[i].name)
		local_tags = find_in_tags(ODP,most_used[i].name)
		for l in local_tags:		
			G.local_tags.append(l)
		global_tags.append(G)

	print "#step 3: find the tags meanings"
	import rdflib
	from rdflib import URIRef
	from rdflib import Graph
	means = URIRef("http://lexvo.org/ontology#means")
	seeAlso = URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso")
	translation = URIRef("http://lexvo.org/ontology#translation")
	literal_form = URIRef("http://www.w3.org/2008/05/skos-xl#literalForm")

	for global_tag in global_tags:	
		g = Graph()
		parse = True	
		try:
			g.parse("http://www.lexvo.org/data/term/" + global_tag.lang + "/" + urllib.quote(global_tag.label.encode('utf-8').lower()))
		except:
			parse = False

		if parse:
			for s,p,o in g.triples((None,means,None)):
				global_tag.resources.append(str(o))

			for s,p,o in g.triples((None,seeAlso,None)):
				global_tag.resources.append(str(o))


	print "#step 4: find the tags in other idioms"	
	
	for global_tag in global_tags:	
		g = Graph()
		parse = True	
		try:
			g.parse("http://www.lexvo.org/data/term/" + global_tag.lang + "/" + urllib.quote(global_tag.label.encode('utf-8').lower()))
		except:
			parse = False

		if parse:
			for s,p,o in g.triples((None,translation,None)):
				#TODO UGLY - Dont do this!!!
				translated = str(o).split("/")[len(str(o).split("/"))-1]
				translated = urllib.unquote(translated).decode('utf8') 
				print global_tag.label + " === " + translated
#				raw_input("Press Enter to continue...")

				tags = find_in_tags(ODP,translated.encode('utf8'))
				for t in tags: 
					global_tag.local_tags.append(t)

		with open(config.global_tags_file, 'wb') as output:
			pickle.dump(global_tags, output, -1)


#	print "----------"	
#	for global_tag in global_tags:
#		print global_tag.label
#		for l in global_tag.local_tags:
#			print l
#		for r in global_tag.resources:
#			print r

#		print "----------"

	return global_tags

def find_in_tags(ODP, name):
	result = []
	for o in ODP:
		for t in o.tags:
			if t.name.lower() == name.lower():
				result.append(model.LocalTag(t.name,o.url, t.count, o.lang))
	return result				

def WriteWikiPages():
	
	with open(config.global_tags_file, 'rb') as input:
		global_tags = pickle.load(input)

	pages_ODP = open(config.wiki_out_file, 'wb')

	for g in global_tags:
		
		pages_ODP.write(g.label + '\n\n')
		pages_ODP.write('--ENDTITLE--\n')

		pages_ODP.write('{{Global Tag\n')
		
		if g.description:
			pages_ODP.write('|1=' + g.description.encode('utf-8') + '\n')
		pages_ODP.write('|2=' + str(g.resources_print()) + '\n')
		pages_ODP.write('|3=' + g.local_tags_print().encode('utf-8') + '\n')
		pages_ODP.write('|4=' + g.related_print() + '\n')
		pages_ODP.write('}}' + '\n')

		pages_ODP.write('--ENDPAGE--\n\n')


def SignificanceOfTagsWithMeaning():
	
	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)

	N = 0;	n = 0;	S = 0;	s = 0; x = 0 ; X = 0; z = 0 ; Z = 0
	for o in ODP:
		for tag in o.tags:
			N += tag.count
			n += 1
			if ([int(tag.name[i]) for i in range(0,len(tag.name)) if tag.name[i].encode('utf-8').isdigit()] == []) and (len(tag.name)>3):
				if tag.meanings != []:	
					S +=tag.count
					s += 1
				else:
					Z +=tag.count
					z += 1
			else:
				x +=1
				X += tag.count

	print "With meaning (perc): " + str(s/float(n)*100)
 	print "Not analysed (perc): " + str(x/float(n)*100)
 	print "No meaning (perc): " + str(z/float(n)*100)

 	print "With meaning (sig): " + str(S/float(N)*100)
 	print "Not analysed (sig): " + str(X/float(N)*100)
 	print "No meaning (sig): " + str(Z/float(N)*100)

def ListCooccurences():

	with open(config.objects_file, 'rb') as input:
		ODP =  pickle.load(input)
	
	for o in ODP:
		for t in o.tags:
			print "Tag: " + t.name
			for c in t.cooccurences:
					for tt in o.tags:
						if c == tt.tag_id:
							print ">> " + tt.name
							break
	




