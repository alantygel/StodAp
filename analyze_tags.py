##########################################################
#This scripts walks through several CKAN instances given by the CKAN instances project (https://github.com/ckan/ckan-instances/blob/gh-pages/config/instances.json) and collects information about the portals, the datasets, and tags. Data are stored as objects of the class Open Data Portal.

#This script outputs a file that is suitable to be inserted in a (semantic) media wiki instance.
##########################################################

import urllib2
import urllib
import json
import pprint
import cPickle as pickle

class OpenDataPortal:
	def __init__(self, url, name, num_of_tags, num_of_packages):
		self.url = url
		self.name = name
		self.tags = []
		self.matching_tags = []
		self.num_of_tags = num_of_tags
		self.num_of_packages = num_of_packages
		self.datasets_tags = []

	def __repr__(self):
		return repr(self.url)

	def add_tag(self, tag, count):
		self.tags.append(Tag(tag,count,self))

	def add_dataset_tag(self, dataset, tag):
		self.datasets_tags.append(DatasetTag(dataset,tag))
		
	def add_matching_tag(self, tag):
		self.matching_tags.append(tag)

	def show_matching_tags(self, out_file):
		for tag in self.matching_tags:
			out_file.write( tag.name.encode('utf-8') + ';' + tag.ODP.name.encode('utf-8') + '\n')

	def load_tags(self):
		"get all tags from a CKAN website and count the occurences"
		response = False
		try:		
			response = urllib2.urlopen(self.url + '/api/3/action/tag_list')
		except:
			1 == 1
		if response: 
			try: 
				response_dict = json.loads(response.read())	
				result = response_dict['result']
			except:
				1 == 1
			for j in range(0,len(result)):
				response2 = False
				try:				
					response2 = urllib2.urlopen(self.url + '/api/3/action/package_search?fq=tags:"' + urllib2.quote(result[j].encode('UTF-8')) + '"\n')
				except:
					1 == 1
				if response2:
					response_dict2 = json.loads(response2.read())	
					result2 = response_dict2['result']
					self.add_tag(result[j],str(result2['count']))
					for d in response_dict2['result']['results']:
						self.add_dataset_tag(d['name'],result[j])

					#out_file.write(self.name + ';' + result[j].encode('utf-8') + ';' + str(result2['count']).encode('utf-8') + '\n')
					#print self.name.encode('utf-8') + ';' + result[j].encode('utf-8') + ';' + str(result2['count']).encode('utf-8') + '\n'
	
	def show_tags(self):
		print sorted(self.tags, key=lambda tag:tag.count, reverse=True)

	#verifies for coincident tags between two ODPs
	def match_tags(self, ODP):
		match_matrix = [[0 for x in range(len(self.tags))] for x in range(len(ODP.tags))] 
		for t in range(0,len(self.tags)):
			for t_other in range(0,len(ODP.tags)):
				if self.tags[t].name == ODP.tags[t_other].name:
					self.add_matching_tag(ODP.tags[t_other])


class DatasetTag:
	def __init__(self, dataset, tag):
		self.dataset = dataset
		self.tag = tag

	def __repr__(self):
		return repr((self.dataset, self.tag))


class Tag:
	def __init__(self, name, count,ODP):
		self.name = name
		self.count = count
		self.ODP = ODP

	def __repr__(self):
		return repr((self.name, self.count))

def LoadODPs():
	"Reads the instance files, and initialize a list of ODP objects"
	instances_file = 'instances.json'
	ODP = []

	with open(instances_file, 'r') as f:
		instances = json.loads(f.read())

	for i in instances:
		try: 
			response = urllib2.urlopen(i['url'] + '/api/3/action/tag_list')
			response_pkg = urllib2.urlopen(i['url'] + '/api/3/action/package_list')
		except:
	#		print "Could not connect"
			response = 0
		if response:
			try:		
				response_dict = json.loads(response.read())	
				result = response_dict['result']

				response_dict_pkg = json.loads(response_pkg.read())	
				packages = response_dict_pkg['result']

				ODP.append(OpenDataPortal(i['url'], i['title'], len(result), len(packages)))
				#print i['title'] + ';' + i['url'] + ';' + str(len(result)) + ';' + str(len(packages))
	#			break
			except:
				print i['title'] + ';' + i['url'] + ';' + 'No API'	
			
		else:
			print i['title'] + ';' + i['url'] + ';' + 'No API'
	

	with open('ODP.pkl', 'wb') as output:
		pickle.dump(ODP, output, -1)

def LoadODPTags():
	"loop through all CKAN featured websites and load tags and number of occurences to object"

	with open('ODP.pkl', 'rb') as input:
		 ODP =  pickle.load(input)
	
#	ODP = [OpenDataPortal('http://dados.contraosagrotoxicos.org', 'Agro', 1, 1)]

	for o in ODP:
		if o.tags == []:
			#print 'Loading tags from ' + o.url
			o.load_tags()
			with open('ODP.pkl', 'wb') as output:
				pickle.dump(ODP, output, -1)
		#else:
			#print o.url + ' tags already loaded'

def ShowODPTags():

	with open('ODP.pkl','rb') as input:
		ODP = pickle.load(input)

	for o in ODP:
		print o.name + ' ' + o.tags[0].name
		#o.show_tags();

def WriteWikiPages():
	"write ODP pages"

	with open('ODP.pkl', 'rb') as input:
		ODP =  pickle.load(input)

	pages_ODP = open('wiki_portal.txt', 'wb')

	for o in ODP:
		pages_ODP.write('Portal:' + o.url.encode('utf-8') + '\n')
		pages_ODP.write('--ENDTITLE--\n\n')

		pages_ODP.write('Here comes the descritpion \n\n')

 		pages_ODP.write('== Tags == \n\n')

		for t in o.tags:
			pages_ODP.write('{{#set: [[tags:taggedBy::Tag:' + t.name.encode('utf-8') + ']]}}\n')
			pages_ODP.write('* [[Tag:' + t.name.encode('utf-8') + ']]\n')

		pages_ODP.write('== Datasets ==\n\n')

		#pages_ODP.write('{{#ask: [[datasetBelongTo::Portal:' + o.url.encode('utf-8') + ']]}}\n')
		pages_ODP.write('--ENDPAGE--\n\n')

	pages_ODP.close

	pages_ODP = open('wiki_tag.txt', 'wb')

	for o in ODP:

		for t in o.tags:
			pages_ODP.write('Tag:' + t.name.encode('utf-8') + '\n')
			pages_ODP.write('--ENDTITLE--\n\n')

	 		pages_ODP.write('== Portals == \n\n')

			#pages_ODP.write('{{#ask: [[tags:taggedBy::Tag:' + t.name.encode('utf-8') + ']]}}\n')

			#pages_ODP.write('== Datasets ==\n\n')

			pages_ODP.write('--ENDPAGE--\n\n')

	pages_ODP.close


def WriteTagsCSV():
	with open('ODP.pkl', 'rb') as input:
		ODP =  pickle.load(input)

	tags_ODP = open('tags.csv', 'wb')

	for o in ODP:
		for t in o.tags:
			tags_ODP.write(o.url.encode('utf-8') + ';' + t.name.encode('utf-8') + ';' + str(t.count).encode('utf-8') + '\n')
	
	tags_ODP.close

def WritePortalsCSV():
	with open('ODP.pkl', 'rb') as input:
		ODP =  pickle.load(input)

	portals_ODP = open('portals.csv', 'wb')

	for o in ODP:
		portals_ODP.write(o.url.encode('utf-8') + ';' + str(o.num_of_tags).encode('utf-8') + ';' + str(o.num_of_packages).encode('utf-8') + '\n')

	portals_ODP.close

def CalculateStats():
	with open('ODP.pkl', 'rb') as input:
		ODP =  pickle.load(input)

	print 'Number of portals: ' + str(len(ODP))

	x = 0; y = 0
	for o in ODP:
		x = x + o.num_of_tags
		y = y + o.num_of_packages
	print 'Number of tags: ' , str(x)
	print 'Number of packages: ' , str(y)

	all_tags, unique_tags = CalculateUniqueTags()

	print 'Number of loaded tags: ' , str(len(all_tags))
	print 'Number of unique tags: ' , str(len(unique_tags))

def CalculateUniqueTags():
	with open('ODP.pkl', 'rb') as input:
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

	with open('ODP.pkl', 'rb') as input:
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

#CalculateStats()
#LoadODPs()
#LoadODPTags()
#ShowODPTags()
#WriteWikiPages()


#ODP = OpenDataPortal('http://dados.contraosagrotoxicos.org', 'Agro', 1, 1)
#ODP.load_tags()



