##########################################################
#This scripts walks through several CKAN instances given by the CKAN instances project (https://github.com/ckan/ckan-instances/blob/gh-pages/config/instances.json) and collects information about the portals, the datasets, and tags. Data are stored as objects of the class Open Data Portal.

#This script outputs a file that is suitable to be inserted in a (semantic) media wiki instance.
##########################################################

global DEBUG
DEBUG = True

global objects_file
objects_file = 'ODP3.pkl'

global global_tags_file
global_tags_file = 'GlobalTags.pkl'

global wiki_out_file
wiki_out_file = 'wiki_portal.txt'

global instances_file
#instances_file = 'instances.json'
instances_file = 'instances_debug.json'
#instances_file = 'instances_test.json'

global groups_file
groups_file = 'groups.pkl'
