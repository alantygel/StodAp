# StodAp
Semantic Tags for Open DAta Portals

The StodAp Project aims to build a central semantic tag server to help organizing and linking Open Data Portals. It is composed by 2 parts:

## Media Wiki ##

The tag server is an instance of Media Wiki run with the Semantic Media Wiki extension. In this server, every tag, dataset and portal becomes a wiki/semantic resource, and thus can be interconnected. This dataset can also be downloaded as RDF.

## CKAN Extension ##

The CKAN Extension makes the connection between an Open Data Portal and the tag central server, and provides sugestions of related databases from other portals.

## Architecture ##

![StodAp Client Server Architecture](clientserver.jpg "StodAp Client Server Architecture")

## Dependencies
pip install python-Levenshtein
pip install numpy
