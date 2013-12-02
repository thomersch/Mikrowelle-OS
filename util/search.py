search_head_tpl = """var idx = lunr(function ()
{
	this.field('title', { boost: 2 }),
	this.field('body'),
	this.field('chapters', { boost: 10 })
});
"""

search_chapter_tpl = """idx.add({
	"title": "%s",
	"body": "%s",
	"chapters": "%s",
	"id": "%s"
});
"""

def generate_search(posts, settings):
	with open("./tmp_output/search.js", "w", encoding="utf-8") as f:
		f.write(search_head_tpl)

		for post in posts:
			chapters = [c["title"] for c in post["chapters"]]
			f.write(search_chapter_tpl % (post["title"], post["content"], str(chapters), post["episode"]))
