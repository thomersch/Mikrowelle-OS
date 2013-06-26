# -*- coding: utf-8 -*-

from lxml import etree
from datetime import datetime
import urllib
import sys

def generate(channel, elements, settings):
	namespaces = {
	"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
	"atom": "http://www.w3.org/2005/Atom",
	"psc": "http://podlove.org/simple-chapters"
	}

	r = etree.Element("rss", version="2.0", nsmap=namespaces)
	r.append(etree.Element("channel"))

	# feed data
	fd = {}

	fd["title"] = etree.Element("title")
	fd["title"].text = channel["title"]

	fd["link"] = etree.Element("link")
	fd["link"].text = channel["link"]
	
	fd["description"] = etree.Element("description")
	fd["description"].text = channel["description"]

	fd["lastBuildDate"] = etree.Element("lastBuildDate")
	fd["lastBuildDate"].text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

	fd["generator"] = etree.Element("generator")
	fd["generator"].text = "Mikrowelle OS"

	fd["author"] = etree.Element("author")
	fd["author"].text = channel["author"]

	fd["it_author"] = etree.Element("{%s}author" % namespaces["itunes"])
	fd["it_author"].text = channel["author"]

	fd["it_logo"] = etree.Element("{%s}image" % namespaces["itunes"], href=channel["artwork"])
	fd["it_logo"].text = channel["artwork"]

	fd["logo"] = etree.Element("logo")
	fd["logo"].text = channel["artwork"]

	# append all items (feed data)
	for x, etree_element in fd.iteritems():
		r[0].append(etree_element)

	# podcast episodes ("items" in rss terms)
	for element in elements:
		r[0].append(etree.Element("item"))
		curitem = r[0][len(r[0])-1]
		curitem.append(etree.Element("title"))
		curitem[0].text = element["title"]

		curitem.append(etree.Element("link"))
		curitem[1].text = element["link"]

		curitem.append(etree.Element("description"))
		curitem[2].text = etree.CDATA(element["description"])

		curitem.append(etree.Element("pubDate"))
		if isinstance(element["pubdate"], str) or isinstance(element["pubdate"], unicode):
			curitem[3].text = element["pubdate"]
		else:
			curitem[3].text = element["pubdate"].strftime("%a, %d %b %Y %H:%M:%S +0000")


		curitem.append(etree.Element("guid", isPermaLink="false"))
		curitem[4].text = element["guid"]

		if "artwork" not in element:
			curitem.append(etree.Element("{%s}image" % namespaces["itunes"], href=channel["artwork"]))
		else:
			curitem.append(etree.Element("{%s}image" % namespaces["itunes"], href=element["artwork"]))

		if isinstance(element["enclosure"]["length"], int):
			element["enclosure"]["length"] = str(element["enclosure"]["length"])
		curitem.append(etree.Element("enclosure", url=element["enclosure"]["url"], length=element["enclosure"]["length"], type=element["enclosure"]["type"]))

		encodedurl = urllib.quote(element["link"])
		encodedtitle = urllib.quote(element["title"].encode('utf8'))
		curitem.append(etree.Element("{%s}link" % namespaces["atom"], rel="payment", href=settings["flattrlink"].format(encodedurl, encodedtitle), type="text/html"))



	return(etree.tostring(r, pretty_print=True, encoding="utf-8"))