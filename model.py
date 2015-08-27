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



	def load_data(self):
		"get all tags from a CKAN website and count the occurences"
		tag_list = False

		#get tags
		try:		
			tag_list_response = urllib2.urlopen(self.url + '/api/3/action/tag_list?all_fields=True')
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
			dataset_list_response = urllib2.urlopen(self.url + '/api/3/action/package_list')
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
					dataset_response = urllib2.urlopen(self.url + '/api/3/action/package_search?fq=name:"' + urllib2.quote(dataset.encode('UTF-8')) + '"')
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

	def __repr__(self):
		return repr(self.name)

	def set_count(self, count):
		self.count = count

class Tagging:
	def __init__(self, tag, dataset):
		self.tag_id = tag['id']
		self.dataset_id = dataset['id']	
