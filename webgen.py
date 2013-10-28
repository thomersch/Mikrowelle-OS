# -*- coding: utf-8 -*-

__version__ = (1, 2, 5)
__author__ = "Thomas Skowron (thomersch)"

import util.rssgen as rssgen
from util.progressbar import AnimatedProgressBar

import sys
import os
import json
import shutil
from datetime import datetime
import distutils.dir_util as du

import markdown
from jinja2 import FileSystemLoader, Environment

if sys.version_info < (3, 0, 0):
	from codecs import open

def getsettings():
	with open("./settings.json", "r", encoding="utf-8") as f:
		settings = json.loads(f.read())
	return settings


def _writeJsonData(filefolder, fn):
	with open("{}{}".format(filefolder, fn), encoding="utf-8") as f:
		h = json.loads(f.read())
		o = {}
		# get all the metadata!
		o["episode"] = h["metadata"]["track"]
		o["title"] = h["metadata"]["title"]
		o["content"] = markdown.markdown(h["metadata"]["summary"])
		o["subtitle"] = markdown.markdown(h["metadata"]["subtitle"])
		o["date"] = h["change_time"]
		o["humandate"] = datetime.strptime(
			o["date"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y")
		o["filename"] = h["output_basename"]
		o["duration"] = h["length_timestring"]
		o["chapters"] = h["chapters"]
		j = json.dumps(o, sort_keys=True, indent=4, separators=(',', ': '))
		
		# write converted file to post storage folder
		if not os.path.exists("./posts/"):
			os.mkdir("./posts/")
		episode_file_name = "./posts/{}".format(fn)
		with open(episode_file_name, "a+", encoding="utf-8") as e:
			e.write(j)


def _getJsonFileList(filefolder):
	def filterFile(fn):
		if fn.endswith(".json") and not os.path.exists(os.path.join("./posts/", fn)):
			return True
		
	return [fn for fn in os.listdir(filefolder) if filterFile(fn)]


def _getElements(posts, settings, format):
	filefolder = settings["filefolder"]
	baseurl = settings["baseurl"]

	# mime type mapping
	mimetypes = {
		"mp3": "audio/mpeg",
		"m4a": "audio/x-m4a",
		"opus": "audio/opus"
	}

	elements = []
	for post in posts:
		filesize = os.path.getsize("{}{}.{}".format(filefolder, post["filename"], format))
		mime = mimetypes[format]
		episode_link = "{}{}.html".format(baseurl, post["episode"])
		guid = "{}{}.html.{}".format(baseurl, post["episode"], post["date"])

		elements.append(
			{
				"title": post["title"],
				"link": episode_link,
				"description": post["content"],
				"guid": guid,
				"pubdate": datetime.strptime(post["date"], "%Y-%m-%dT%H:%M:%S.%fZ"),
				"enclosure": {
					"url": "{}{}.{}".format(settings["audio_base_url"], post["filename"], format),
					"length": filesize,
					"type": mime
				},
				"chapters": post["chapters"]
			}
		)

	return elements


def jsontransform(settings):
	"""
		jsontransform() transforms auphonic input files into post files
		that can be read by the generate() method
	"""

	filefolder = settings["filefolder"]

	if not os.path.exists(filefolder):
		print("[INFO] No media in %s found." % filefolder)
		os.mkdir(filefolder)

	filelist = _getJsonFileList(filefolder)
	if filelist == []:
		progresslength = 1
	else:
		progresslength = len(filelist)*2

	global progress
	progress = AnimatedProgressBar(end=progresslength, width=60)

	for fn in filelist:
		_writeJsonData(filefolder, fn)
		progress + 1
		progress.show_progress()


def generate(settings):
	# settings mapping
	tplfolder = settings["tplfolder"]
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
		with open("./posts/%s" % filename, "r", encoding="utf-8") as f:
			# read data from json
			p = json.loads(f.read())
			posts.append(p)
			# write individual pages for posts
			with open("./tmp_output/%s.html" % p["episode"],
				"a+", encoding="utf-8") as w:
				w.write(single_template.render(post=p, settings=settings, feeds=formats, index_page=False))
				progress + 1
				progress.show_progress()


	# write index.html with all posts
	index_file_content = index_template.render(posts=posts, settings=settings, feeds=formats, index_page=True)

	with open("./tmp_output/index.html", "a+", encoding="utf-8") as f:
		f.write(index_file_content)


	# generate feed_description
	for fmt in formats:
		elements = _getElements(posts, settings, fmt)

		channel = {
			"title": settings["feed_title"].format(fmt),
			"link": settings["feed_link"],
			"description": settings["feed_description"],
			"author": settings["author"],
			"artwork": settings["artwork_url"]
		}
		with open("./tmp_output/{}.xml".format(fmt), "wb") as f:
			f.write(rssgen.generate(channel=channel, elements=elements, settings=settings))

	# copy from temp to production and remove tmp
	du.copy_tree("./tmp_output", publish)
	shutil.rmtree("./tmp_output/")


def run():
	settings = getsettings()
	jsontransform(settings)
	generate(settings)


if __name__ == "__main__":
	if sys.version_info >= (2, 7, 0):
		print("Running Mikrowelle OS {}.{}.{}".format(__version__[0], __version__[1], __version__[2]))
		run()
	else:
		print("[ERROR] Your python interpreter version is too old. Required: 2.7")
