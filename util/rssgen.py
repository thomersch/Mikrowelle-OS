# -*- coding: utf-8 -*-

from lxml import etree
from lxml.etree import CDATA
from datetime import datetime
import sys

if sys.version_info < (3, 0, 0):
	from urllib import quote as urlquote
else:
	from urllib.parse import quote as urlquote

def _chapters(element, namespaces):
	xml_chapters = etree.Element("{%s}chapters" % namespaces["psc"], version="1.2")

	for chapter in element["chapters"]:
		xml_chapters.append(
			etree.Element("{%s}chapter" % namespaces[u"psc"], start=chapter[u"start"],
			title=chapter[u"title"], href=chapter[u"url"])
		)

	return xml_chapters


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

	fe["ttl"] = etree.Element("ttl")
	fe["ttl"].text = channel["feedinterval"]

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

	fe["language"] = etree.Element("language")
	fe["language"].text = settings.get("language", "de-de")

	cat = settings.get("category", None)
	if isinstance(cat, str) or isinstance(cat, unicode):
		fe["it_category"] = etree.Element("{%s}category" % namespaces["itunes"], text=cat)

	if "artwork" in channel:
		fe["it_logo"] = etree.Element("{%s}image" % namespaces["itunes"], href=channel["artwork"])
		fe["logo"] = etree.Element("logo")
		fe["logo"].text = channel["artwork"]

	if "explicit" in channel:
		fe["explicit"] = etree.Element("{%s}explicit" % namespaces["itunes"])
		if channel["explicit"] == True:
			fe["explicit"].text = "yes"
		else:
			fe["explicit"].text = "clean"

	# append all items (feed data)
	for x, etree_element in fe.items():
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
		ee["description"].text = CDATA(element["description"])

		ee["guid"] = etree.Element("guid", isPermaLink="false")
		ee["guid"].text = element["guid"]

		ee["pubdate"] = etree.Element("pubDate")
		if isinstance(element["pubdate"], datetime):
			ee["pubdate"].text = element["pubdate"].strftime("%a, %d %b %Y %H:%M:%S +0000")
		else:
			ee["pubdate"].text = element["pubdate"]

		if "artwork" in element or "artwork" in channel:
			if "artwork" in element:
				ee["it_image"] = etree.Element("{%s}image" % namespaces["itunes"], href=element["artwork"])
			else:
				# take image/artwork from channel
				ee["it_image"] = etree.Element("{%s}image" % namespaces["itunes"], href=channel["artwork"])
			ee["image"] = ee["it_image"]

		if isinstance(element["enclosure"]["length"], int):
			element["enclosure"]["length"] = str(element["enclosure"]["length"])
		ee["enclosure"] = etree.Element("enclosure", url=element["enclosure"]["url"], length=element["enclosure"]["length"], type=element["enclosure"]["type"])

		encodedurl = urlquote(element["link"])
		encodedtitle = urlquote(element["title"].encode('utf8'))
		ee["flattr"] = etree.Element("{%s}link" % namespaces["atom"], rel="payment", href=settings["flattrlink"].format(encodedurl, encodedtitle), type="text/html")

		if element["chapters"] != []:
			ee["chapters"] = _chapters(element, namespaces)

		# append item elements
		for x, etree_element in ee.items():
			curitem.append(etree_element)

		# append item to channel
		chan.append(curitem)

	r.append(chan)

	return(etree.tostring(r, xml_declaration=True, pretty_print=True, encoding="utf-8"))
