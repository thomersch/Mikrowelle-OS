import json
import sys

if sys.version_info < (3, 0, 0):
	from codecs import open

def build_index(posts, path):
	index = []
	for post in posts:
		index.append({
			"episode": post["episode"],
			"date": post["date"],
			"title": post["title"],
			"subtitle": post["subtitle"],
			"content": post["content"]
		})
		
	with open(path, "a+", encoding="utf-8") as f:
		json.dump(index, f)

