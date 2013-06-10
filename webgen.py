# -*- coding: utf-8 -*-

__version__ = (1, 1, 0)
__author__ = "Thomas Skowron (thomersch)"

import rssgen
import codecs
import os
import json
import shutil
import distutils.dir_util as du
import time
import markdown
from datetime import datetime
from jinja2 import Template, FileSystemLoader, Environment

with codecs.open("./settings.json", "r", encoding="utf-8") as f:
	settings = json.loads(f.read())

tplfolder = settings["tplfolder"]
baseurl = settings["baseurl"]
filefolder = settings["filefolder"]
publish = settings["publish"]
formats = settings["feeds"]

def jsontransform():
	for fn in os.listdir(filefolder):
		if fn.endswith(".json"):
			with open("{}{}".format(filefolder, fn)) as f:
				h = json.loads(f.read())
				o = {}
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
				with codecs.open("./posts/{}.json".format(o["episode"]), "a+", encoding="utf-8") as e:
					e.write(j)
			os.rename("{}{}".format(filefolder, fn), "{}{}.txt".format(filefolder, fn))

def generate():
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
	for filename in os.listdir("./posts/"):
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
			if fmt == "mp3":
				mime = "audio/mpeg"
			elif fmt == "opus":
				mime = "audio/opus"
			elif fmt == "m4a":
				mime = "audio/x-m4a"

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
					}
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
			f.write(rssgen.generate(channel=channel, elements=elements))

	# copy from temp to production and remove tmp
	du.copy_tree("./tmp_output", publish)
	shutil.rmtree("./tmp_output/")

if __name__ == "__main__":
	jsontransform()
	generate()