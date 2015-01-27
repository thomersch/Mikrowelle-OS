# -*- coding: utf-8 -*-

import shutil
import os
import sys
import imp

def test():
	test_root = os.path.split(os.path.abspath(__file__))[0]
	print(test_root)
	mw_root = os.path.join(test_root, "..")
	tmp_path = os.path.join(test_root, "tmp/")
	print(tmp_path)

	# set up directory
	if os.path.exists(os.path.join(test_root, "tmp/")):
		# clean up old tests
		shutil.rmtree(os.path.join(test_root, "tmp/"))
	os.mkdir(os.path.join(test_root, "tmp/"))

	# copy mikrowelle os system files
	shutil.copy(os.path.join(mw_root, "mikrowelle.py"), tmp_path)
	shutil.copy(os.path.join(mw_root, "settings.default.json"), os.path.join(tmp_path, "settings.json"))
	shutil.copytree(os.path.join(mw_root, "templates/"), os.path.join(tmp_path, "templates/"))
	shutil.copytree(os.path.join(mw_root, "util/"), os.path.join(tmp_path, "util/"))
	shutil.copytree(os.path.join(test_root, "audio/"), os.path.join(tmp_path, "audio/"))

	# changing to tmp directory, simulating working environment
	os.chdir(tmp_path)
	sys.path.append(".")
	import mikrowelle

	# I am a firestarter! Let's go!
	mikrowelle.run()

	# check if the files are there
	pub = ["001.html", "index.html", "m4a.xml", "mp3.xml", "opus.xml"]
	if not os.path.exists("posts/001.json"):
		print("[ERROR] No post created.")

	for p in pub:
		if p not in os.listdir("pub/"):
			print("[ERROR] Missing %s" % p)

	os.chdir(test_root)


if __name__ == "__main__":
	test()