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
	chan = etree.Element("channel")

	# feed elements
	fe = {}

	fe["title"] = etree.Element("title")
	fe["title"].text = channel["title"]

	fe["link"] = etree.Element("link")
	fe["link"].text = channel["link"]
	
	fe["description"] = etree.Element("description")
	fe["description"].text = channel["description"]

	fe["lastBuildDate"] = etree.Element("lastBuildDate")
	fe["lastBuildDate"].text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

	fe["generator"] = etree.Element("generator")
	fe["generator"].text = "Mikrowelle OS"

	fe["author"] = etree.Element("author")
	fe["author"].text = channel["author"]

	fe["it_author"] = etree.Element("{%s}author" % namespaces["itunes"])
	fe["it_author"].text = channel["author"]

	fe["it_logo"] = etree.Element("{%s}image" % namespaces["itunes"], href=channel["artwork"])
	fe["it_logo"].text = channel["artwork"]

	fe["logo"] = etree.Element("logo")
	fe["logo"].text = channel["artwork"]

	# append all items (feed data)
	for x, etree_element in fe.iteritems():
		chan.append(etree_element)

	# podcast episodes ("items" in rss terms)
	for element in elements:
		# episode elements
		ee = {}
		curitem = etree.Element("item")

		ee["title"] = etree.Element("title")
		ee["title"].text = element["title"]

		ee["link"] = etree.Element("link")
		ee["link"].text = element["link"]

		ee["description"] = etree.Element("description")
		ee["description"].text = etree.CDATA(element["description"])

		ee["guid"] = etree.Element("guid", isPermaLink="false")
		ee["guid"].text = element["guid"]

		ee["pubdate"] = etree.Element("pubDate")
		if isinstance(element["pubdate"], str) or isinstance(element["pubdate"], unicode):
			ee["pubdate"].text = element["pubdate"]
		else:
			ee["pubdate"].text = element["pubdate"].strftime("%a, %d %b %Y %H:%M:%S +0000")

		if "artwork" not in element:
			# take image/artwork from channel
			ee["it_image"] = etree.Element("{%s}image" % namespaces["itunes"], href=channel["artwork"])
		else:
			ee["it_image"] = etree.Element("{%s}image" % namespaces["itunes"], href=element["artwork"])

		if isinstance(element["enclosure"]["length"], int):
			element["enclosure"]["length"] = str(element["enclosure"]["length"])
		ee["enclosure"] = etree.Element("enclosure", url=element["enclosure"]["url"], length=element["enclosure"]["length"], type=element["enclosure"]["type"])

		encodedurl = urllib.quote(element["link"])
		encodedtitle = urllib.quote(element["title"].encode('utf8'))
		ee["flattr"] = etree.Element("{%s}link" % namespaces["atom"], rel="payment", href=settings["flattrlink"].format(encodedurl, encodedtitle), type="text/html")

		# append item elements
		for x, etree_element in ee.iteritems():
			curitem.append(etree_element)

		# append item to channel
		chan.append(curitem)

	r.append(chan)

	return(etree.tostring(r, xml_declaration=True, pretty_print=True, encoding="utf-8"))