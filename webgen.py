# -*- coding: utf-8 -*-

__version__ = (1, 2, 0)
__author__ = "Thomas Skowron (thomersch)"

import rssgen
import codecs
import os
import json
import shutil
import sys
from datetime import datetime
import distutils.dir_util as du

import markdown
from jinja2 import FileSystemLoader, Environment

def getsettings():
	with codecs.open("./settings.json", "r", encoding="utf-8") as f:
		settings = json.loads(f.read())
	return settings

def jsontransform(settings):
	"""
		jsontransform() transforms auphonic input files into post files
		that can be read by the generate() method
	"""

	filefolder = settings["filefolder"]

	if not os.path.exists(filefolder):
		print("[INFO] No media in %s found." % filefolder)
		os.mkdir(filefolder)

	for fn in os.listdir(filefolder):
		if fn.endswith(".json") and not os.path.exists(os.path.join("./posts/", fn)):
			with open("{}{}".format(filefolder, fn)) as f:
				h = json.loads(f.read())
				o = {}
				# get all the metadata!
				o["episode"] = h["metadata"]["track"]
				o["title"] = h["metadata"]["title"]
				o["content"] = markdown.markdown(h["metadata"]["summary"])
				o["subtitle"] = markdown.markdown(h["metadata"]["subtitle"])
				o["date"] = h["change_time"]
				o["humandate"] = datetime.strptime(o["date"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y")
				o["filename"] = h["output_basename"]
				o["duration"] = h["length_timestring"]
				o["chapters"] = h["chapters"]
				j = json.dumps(o, sort_keys=True, indent=4, separators=(',', ': '))
				
				# write converted file to post storage folder
				if not os.path.exists("./posts/"):
					os.mkdir("./posts/")
				with codecs.open("./posts/{}.json".format(o["episode"]), "a+", encoding="utf-8") as e:
					e.write(j)

def generate(settings):
	# mime type mapping
	mimetypes = {
		"mp3": "audio/mpeg",
		"m4a": "audio/x-m4a",
		"opus": "audio/opus"
	}

	# settings mapping                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
	tplfolder = settings["tplfolder"]
	baseurl = settings["baseurl"]
	filefolder = settings["filefolder"]
	publish = settings["publish"]
	formats = settings["feeds"]

	# create output folder
	if os.path.exists("./tmp_output/"):
		shutil.rmtree("./tmp_output/")
	os.mkdir("tmp_output")

	# load template files
	jenv = Environment(loader=FileSystemLoader(tplfolder))
	index_template = jenv.get_template("index.tpl")
	single_template = jenv.get_template("single.tpl")

	# search content
	posts = []
	if not os.path.exists("./posts/"):
		print("[INFO] No posts found.")
		os.mkdir("./posts/")

	for filename in sorted(os.listdir("./posts/"), reverse=True):
		with codecs.open("./posts/%s" % filename, "r", encoding="utf-8") as f:
			# read data from json
			p = json.loads(f.read())
			posts.append(p)
			# write individual pages for posts
			with codecs.open("./tmp_output/%s.html" % p["episode"],
				"a+", encoding="utf-8") as w:
				w.write(single_template.render(post=p, settings=settings, feeds=formats))

	# write index.html with all posts
	with codecs.open("./tmp_output/index.html", "a+", encoding="utf-8") as f:
		f.write(index_template.render(posts=posts, settings=settings, feeds=formats))

	# generate feed_description
	for fmt in formats:
		elements = []
		for post in posts:
			filesize = os.path.getsize("{}{}.{}".format(filefolder, post["filename"], fmt))
			mime = mimetypes[fmt]

			elements.append(
				{
					"title": post["title"],
					"link": "{}{}.html".format(baseurl, post["episode"]),
					"description": post["content"],
					"guid": "{}{}.html.{}".format(baseurl, post["episode"], post["date"]),
					"pubdate": datetime.strptime(post["date"], "%Y-%m-%dT%H:%M:%S.%fZ"),
					"enclosure": {
						"url": "{}{}.{}".format(settings["audio_base_url"], post["filename"], fmt),
						"length": filesize,
						"type": mime
					},
					"chapters": post["chapters"]
				}
			)

		channel = {
			"title": settings["feed_title"].format(fmt),
			"link": settings["feed_link"],
			"description": settings["feed_description"],
			"author": settings["author"],
			"artwork": settings["artwork_url"]
		}
		with open("./tmp_output/{}.xml".format(fmt), "a+") as f:
			f.write(rssgen.generate(channel=channel, elements=elements, settings=settings))

	# copy from temp to production and remove tmp
	du.copy_tree("./tmp_output", publish)
	shutil.rmtree("./tmp_output/")

def run():
	settings = getsettings()
	jsontransform(settings)
	generate(settings)

if __name__ == "__main__":
	if sys.version_info >= (2,7,0):
		run()
	else:
		print("[ERROR] Your python interpreter version is too old. Required: 2.7")