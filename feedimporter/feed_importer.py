# -*- coding: utf-8 -*-
import sys
import os
import urllib
import shutil
from time import strftime, mktime
from email.utils import parsedate
from lxml import etree

__version__ = (0, 0, 1)
__author__ = "Thomas Skowron (thomersch)"

output_path = "./mikrowelle_import/"

def _getChannelInformation(xml_tree):
	pass


def _processOneEpisode(item, json_path, episode_number):
	pubDate = item.find(".//pubDate").text
	date = strftime("%Y-%m-%dT%H:%M:%S.000Z", parsedate(pubDate))
	filename = os.path.splitext(os.path.split(item.find(".//enclosure").attrib["url"])[1])[0]

	o = {
		"title": item.find(".//title").text,
		"description": item.find(".//description").text,
		"guid": item.find(".//guid"),
		"pubDate": pubDate,
		"date": date,
		"filename": filename,
		"episode": episode_number,
	}

	print o["title"]
	print o["pubDate"]
	print o["date"]
	print o["filename"]
	print "+++++"


def _processEpisodes(items):
	post_path = os.path.join(output_path, "posts")
	os.mkdir(post_path)

	# sort from old to new
	for number, item in enumerate(reversed(items)):
		episode_json_path = os.path.join(post_path, "%s.json" % (number+1))
		print episode_json_path
		_processOneEpisode(item, episode_json_path, episode_number)


def _getElements(xml_tree):
	items = xml_tree.findall(".//item")
	print("Processing %s episodes..." % len(items))
	_processEpisodes(items)
	

def readXML(xmlstring):
	xml_tree = etree.fromstring(xmlstring)
	_getChannelInformation(xml_tree)
	_getElements(xml_tree)
	print("Done.")
	print("#"*70)


def main():
	if len(sys.argv) < 2:
		print("Missing argument: feed_importer.py <FEEDURL/FEEDPATH>")
		sys.exit()

	if not os.path.exists(output_path):
		os.mkdir(output_path)
	else:
		shutil.rmtree(output_path)
		os.mkdir(output_path)

	if sys.argv[1].startswith("http"):
		feed_string = urllib.urlopen(sys.argv[1]).read()
	else:
		with open(sys.argv[1], "r") as f:
			feed_string = f.read()

	readXML(feed_string)


if __name__ == "__main__":
	print("#"*70)
	print("feed_importer.py v{}.{}.{}".format(__version__[0], __version__[1], __version__[2]))
	print("""The feed importer is work in progress, it may fail at any occasion.
If you encounter any problems, please report them on
https://github.com/thomersch/Mikrowelle-OS.
Thank you.""")
	print("#"*70)
	main()
