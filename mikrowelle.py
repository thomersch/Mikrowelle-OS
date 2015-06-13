# -*- coding: utf-8 -*-

__version__ = (1, 3, 3)
__author__ = "Thomas Skowron (thomersch)"

import util.rssgen as rssgen
import util.search as search
from util.progressbar import AnimatedProgressBar
from util.mime_types import mimetypes

import sys
import os
import json
import shutil
import math
from datetime import datetime
import distutils.dir_util as du

import markdown
from jinja2 import FileSystemLoader, Environment

if sys.version_info < (3, 0, 0):
	from codecs import open

POST_PATH = "posts/"
TMP_PATH = "tmp_output/"

def get_settings():
	with open("settings.json", "r", encoding="utf-8") as f:
		settings = json.loads(f.read())
	return settings


def get_posts():
	posts = []
	if not os.path.exists(POST_PATH):
		print("[INFO] No posts found.")
		os.mkdir(POST_PATH)

	for filename in sorted(os.listdir(POST_PATH), reverse=True):
		with open(POST_PATH+"%s" % filename, "r", encoding="utf-8") as f:
			# read data from json
			p = json.loads(f.read())
			posts.append(p)
			
	return posts


def write_post(post, settings, single_template, progress=None):
	formats = settings["feeds"]

	# write individual page for post
	with open(TMP_PATH + "%s.html" % post["episode"],
		"a+", encoding="utf-8") as w:
		w.write(single_template.render(post=post, settings=settings, feeds=formats, index_page=False))
		if progress is not None:
			progress + 1
			progress.show_progress()


def _write_json_data(filefolder, fn):
	with open("{}{}".format(filefolder, fn), encoding="utf-8") as f:
		h = json.loads(f.read())

		# get all the metadata!
		o = {
			"episode": h["metadata"]["track"],
			"title": h["metadata"]["title"],
			"content": markdown.markdown(h["metadata"]["summary"]),
			"subtitle": markdown.markdown(h["metadata"]["subtitle"]),
			"date": h["change_time"],
			#TODO: make date format string configurable
			"humandate": datetime.strptime(h["change_time"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y"),
			"humanduration": datetime.strptime(h["length_timestring"], "%H:%M:%S.%f").strftime("%H:%M"),
			"filename": h["output_basename"],
			"duration": h["length_timestring"],
			"chapters": h["chapters"]
		}
		j = json.dumps(o, sort_keys=True, indent=4, separators=(',', ': '))

		# write converted file to post storage folder
		if not os.path.exists(POST_PATH):
			os.mkdir(POST_PATH)
		episode_file_name = POST_PATH + "{}".format(fn)
		with open(episode_file_name, "a+", encoding="utf-8") as e:
			e.write(j)


def _get_json_file_list(filefolder):
	def filterFile(fn):
		if fn.endswith(".json") and not os.path.exists(os.path.join(POST_PATH, fn)):
			return True

	return [fn for fn in os.listdir(filefolder) if filterFile(fn)]


def _get_elements(posts, settings, format):
	filefolder = settings["filefolder"]
	baseurl = settings["baseurl"]

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


def _generate_index_pages(posts, settings, formats, index_template):
	posts_on_page = settings.get("posts_on_page", None)
	cur_page = 0
	if posts_on_page is not None:
		while cur_page*posts_on_page < len(posts):
			page_posts = posts[posts_on_page*cur_page:posts_on_page*(cur_page+1)]
			if cur_page == 0:
				filename = TMP_PATH+"index.html"
			else:
				filename = TMP_PATH+"index.%i.html" % cur_page

			with open(filename, "a+", encoding="utf-8") as f:
				if (cur_page + 1)*posts_on_page >= len(posts):
					next = None
				else:
					next = cur_page+1
				if cur_page > 0:
					prev = cur_page-1
				else:
					prev = None
				f.write(index_template.render(posts=page_posts, settings=settings, feeds=formats, index_page=True, prev=prev, next=next))
			cur_page += 1

	else:
		# write index.html with all posts
		with open(TMP_PATH+"index.html", "a+", encoding="utf-8") as f:
			f.write(index_template.render(posts=posts, settings=settings, feeds=formats, index_page=True))

def _generate_archive_page(posts, settings, formats, archive_template):
	with open(TMP_PATH+"archive.html", "a+", encoding="utf-8") as f:
		f.write(archive_template.render(posts=posts, settings=settings, feeds=formats))

def json_transform(settings):
	"""
		json_transform() transforms auphonic input files into post files
		that can be read by the generate() method
	"""

	filefolder = settings["filefolder"]

	if not os.path.exists(filefolder):
		print("[INFO] No media in %s found." % filefolder)
		os.mkdir(filefolder)

	filelist = _get_json_file_list(filefolder)
	if filelist == []:
		progresslength = 1
	else:
		progresslength = len(filelist)*2

	global progress
	progress = AnimatedProgressBar(end=progresslength, width=60)

	for fn in filelist:
		_write_json_data(filefolder, fn)
		progress + 1
		progress.show_progress()


def generate(settings):
	# settings mapping
	tplfolder = settings["tplfolder"]
	publish = settings["publish"]
	formats = settings["feeds"]

	# create output folder
	if os.path.exists(TMP_PATH):
		shutil.rmtree(TMP_PATH)
	os.mkdir(TMP_PATH)

	# load template files
	jenv = Environment(loader=FileSystemLoader(tplfolder))
	index_template = jenv.get_template("index.tpl")
	single_template = jenv.get_template("single.tpl")
	archive_template = jenv.get_template("archive.tpl")
	if os.path.exists(os.path.join(tplfolder, "style.css")):
		shutil.copy(os.path.join(tplfolder, "style.css"), os.path.join(TMP_PATH, "style.css"))

	# get posts from files
	posts = get_posts()

	# write posts with templates
	for post in posts:
		write_post(post, settings, single_template, progress)

	_generate_index_pages(posts, settings, formats, index_template)
	_generate_archive_page(posts, settings, formats, archive_template)

	# generate feed_description
	for fmt in formats:
		elements = _get_elements(posts, settings, fmt)

		channel = {
			"title": settings["feed_title"].format(fmt),
			"link": settings["baseurl"],
			"feedinterval": settings["feedinterval"],
			"description": settings["feed_description"],
			"author": settings["author"],
			"artwork": settings["artwork_url"]
		}

		with open(TMP_PATH + "{}.xml".format(fmt), "wb") as f:
			f.write(rssgen.generate(channel=channel, elements=elements, settings=settings))

	# build search 
	search.build_index(posts, TMP_PATH + "episode_index.json")

	# copy from temp to production and remove tmp
	du.copy_tree(TMP_PATH[:-1], publish)
	shutil.rmtree(TMP_PATH)


def run():
	settings = get_settings()
	json_transform(settings)
	generate(settings)
	print("") # new line


if __name__ == "__main__":
	if sys.version_info >= (2, 7, 0):
		print("Running Mikrowelle OS {}.{}.{}".format(__version__[0], __version__[1], __version__[2]))
		run()
	else:
		print("[ERROR] Your python interpreter version is too old. Required: 2.7")
