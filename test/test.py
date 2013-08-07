# -*- coding: utf-8 -*-

import shutil
import os
import sys
import imp

def test():
	# set up directory
	if os.path.exists("./tmp/"):
		shutil.rmtree("./tmp/")
	os.mkdir("tmp")

	# copy mikrowelle os system files
	shutil.copy("../webgen.py", "./tmp/")
	shutil.copy("../settings.json", "./tmp/")
	shutil.copytree("../templates/", "./tmp/templates/")
	shutil.copytree("../util/", "./tmp/util/")
	shutil.copytree("./audio/", "./tmp/audio/")

	# changing to tmp directory, simulating working environment
	os.chdir("./tmp/")
	sys.path.append("./")
	import webgen

	# I am a firestarter! Let's go!
	webgen.run()

	# check if the files are there
	pub = ["001.html", "index.html", "m4a.xml", "mp3.xml", "opus.xml"]
	if not os.path.exists("./posts/001.json"):
		print("[ERROR] No post created.")

	for p in pub:
		if p not in os.listdir("./pub/"):
			print("[ERROR] Missing %s" % p)

	os.chdir("../")


if __name__ == "__main__":
	test()