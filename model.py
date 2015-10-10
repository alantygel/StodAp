##########################################################
#This scripts walks through several CKAN instances given by the CKAN instances project (https://github.com/ckan/ckan-instances/blob/gh-pages/config/instances.json) and collects information about the portals, the datasets, and tags. Data are stored as objects of the class Open Data Portal.

#This script outputs a file that is suitable to be inserted in a (semantic) media wiki instance.
##########################################################

import urllib2
import urllib
import json
import pprint
import cPickle as pickle
import Levenshtein
import lib




class OpenDataPortal:
	def __init__(self, url, name, num_of_tags, num_of_packages):
		self.url = url
		self.name = name
		self.num_of_tags = num_of_tags
		self.num_of_packages = num_of_packages
		#self.matching_tags = []
		self.tags = []
		self.datasets = []
		self.tagging = []


	def __repr__(self):
		return repr(self.url)

	def add_tag(self, tag):
		self.tags.append(Tag(tag))

	def set_tag_count(self):
		for tag in self.tags:
			taggging_tag = [tagging.tag_id for tagging in self.tagging if tagging.tag_id == tag.tag_id]
			tag.set_count(len(taggging_tag))

	def add_dataset(self, dataset):
		self.datasets.append(Dataset(dataset))

	def add_tagging(self, tag, dataset):
		self.tagging.append(Tagging(tag, dataset))

	def tags_per_dataset_mean (self):
		if  len(self.datasets) > 0:
			ret = float(reduce (lambda x,y: x + y, map(lambda z: z.number_of_tags, self.datasets))) / len (self.datasets)
		else:
			ret = 0
		return ret

	def tags_with_meaning (self):
		res = 0
		for t in self.tags:
			if hasattr(t, 'meanings'):
				if t.meanings != []:
					res += 1
			else:
				print "no meaning"
		if len(self.tags) > 0:
			ret = res/float(len(self.tags))
		else:
			ret = 0
		return ret

	def similarity_matrix (self):
		T = len(self.tags)
		matrix = [[0 for x in range(T)] for x in range(T)]
		for t in range(0,T-1):
		    for s in range(t,T-1):
		        if s != t:
		            matrix[s][t] = Levenshtein.distance(self.tags[t].name,self.tags[s].name)
		return matrix


	def load_data(self):
		"get all tags from a CKAN website and count the occurences"
		tag_list = False

		#get tags
		try:		
			tag_list_response = lib.urlopen_with_retry(self.url + '/api/3/action/tag_list?all_fields=True')
		except:
			1 == 1
		if tag_list_response: 
			try: 
				tag_list_dict = json.loads(tag_list_response.read())	
				tag_list = tag_list_dict['result']
			except:
				1 == 1
			for tag in tag_list:
				self.add_tag(tag)

		#get datasets
		try:		
			dataset_list_response = lib.urlopen_with_retry(self.url + '/api/3/action/package_list')
		except:
			1 == 1

		if dataset_list_response: 
			try: 
				dataset_list_dict = json.loads(dataset_list_response.read())	
				dataset_list = dataset_list_dict['result']
			except:
				1 == 1
			for dataset in dataset_list:
				dataset_response = 0
				try:		
					dataset_response = lib.urlopen_with_retry(self.url + '/api/3/action/package_search?fq=name:"' + urllib2.quote(dataset.encode('UTF-8')) + '"')
				except:
					1 == 1
				if dataset_response: 
					try: 
						dataset_dict = json.loads(dataset_response.read())	
						dataset_allfields = dataset_dict['result']['results'][0]
						self.add_dataset(dataset_allfields)						

						for tag in dataset_allfields['tags']:
							self.add_tagging(tag, dataset_allfields)
					except:
						1 == 1
		#set tag count
		self.set_tag_count()


	def set_language(self):
		import pycountry

		try:
			response = lib.urlopen_with_retry(self.url + '/api/3/action/status_show')
		except:
			response = 0

		if response:

			response_dict = json.loads(response.read())	
			code_1 = response_dict['result']['locale_default']
		
			if code_1:
				lang = str(code_1[0]) + str(code_1[1])
				code_3 = pycountry.languages.get(iso639_1_code=lang).iso639_3_code
			else:
				code_3 = 'eng'

			self.lang = code_3
			#print code_1 + "; " + code_3
			return code_3
			#ODP.append(model.OpenDataPortal(url, i['title'], len(result), len(packages)))

class Dataset:
	def __init__(self, dataset):
		self.name = dataset['title']
		self.dataset_id = dataset['id']
		self.number_of_tags = len(dataset['tags'])

	def __repr__(self):
		return repr(self.name)

class Tag:
	def __init__(self, tag):
		self.name = tag['name']
		self.tag_id = tag['id']
		self.set_meaning()

	def __repr__(self):
		return repr(self.name)

	def set_count(self, count):
		self.count = count

	def set_meaning(self):

		try:
			self.meanings = []
			req = urllib2.Request('http://spotlight.dbpedia.org/rest/annotate?text=' + urllib.quote(self.name.encode('utf-8')), headers = {'Accept' : 'application/json'})	
			contents = json.loads(lib.urlopen_with_retry(req).read())

			if len(contents) == 7:
	#			if isinstance(contents['annotation']['surfaceForm'], list):
				for m in contents['Resources']:
						self.meanings.append(m['@URI'])
				#else:
				#	print "here"
				#	self.meanings.append('http://dbpedia.org/page/' + contents['annotation']['surfaceForm']['resource']['@uri'].encode('utf-8'))
		except:
			1 == 1

	def set_meaning_2(self,lang):

		import rdflib
		from rdflib import URIRef
		from rdflib import Graph
		means = URIRef("http://lexvo.org/ontology#means")
		seeAlso = URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso")

		g = Graph()
		parse = True		
		try:
			#print "http://www.lexvo.org/data/term/" + lang + "/" + urllib.quote(self.name.encode('utf-8'))
			g.parse("http://www.lexvo.org/data/term/" + lang + "/" + urllib.quote(self.name.encode('utf-8')))
		except:
			parse = False

		self.meanings = []
		if parse:
			#out = self.name.encode('utf-8')

			if (None, seeAlso, None) in g:
				#print "See Also found!"
				for s,p,o in g.triples((None,seeAlso,None)):
					#print o
					#out = out + ";" + o.encode('utf-8')
					self.meanings.append(o.encode('utf-8'))

			if (None, means, None) in g:
				#print "Meaning found!"
				for s,p,o in g.triples((None,means,None)):
					#print o
					#out = out + ";" + o.encode('utf-8')
					self.meanings.append(o.encode('utf-8'))
		#print out
		#print self.meanings

class Tagging:
	def __init__(self, tag, dataset):
		self.tag_id = tag['id']
		self.dataset_id = dataset['id']	

class AllTags:
	def __init__(self,name,url,count, lang):
		self.name = name
		self.url = [url]
		self.count = count
		self.global_count = 1
		self.lang = lang

class GlobalTag:
	def __init__(self,label):
		self.label = label
		self.description = None
		self.resources = []
		self.local_tags = []
		self.lang = "eng" #the global tag shall always be in english
		self.related = None

	def resources_print(self):
		out = ""
		for r in self.resources:
			out += str(r) + ","
		return out

	def local_tags_print(self):
		out = ""
		self.local_tags = list(set(self.local_tags))
		for r in self.local_tags:
			out += r.url + "/dataset?tags=" + r.name + ", " 
		return out

	def related_print(self):
		out = ""
#		for r in self.related:
#			out += str(r) + ","
		return out


class LocalTag:
	def __init__(self,name,url,count, lang):
		self.name = name
		self.url = url
		self.count = count
		self.lang = lang
	def __repr__(self):		
		return self.name + "-" + self.url + "-" + str(self.count) + "-" + self.lang	
	def __eq__(self, other):
		return self.url == other.url
	def __hash__(self):
		return hash(('url', self.url))
