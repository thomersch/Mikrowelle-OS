# -*- coding: utf-8 -*-

from lxml import etree
from datetime import datetime
import urllib
import sys

def generate(channel, elements, settings):
	namespaces = {
	"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
	"atom": "http://www.w3.org/2005/Atom"
	}

	n = etree.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
	r = etree.Element("rss", version="2.0", nsmap=namespaces)
	r.append(etree.Element("channel"))
	r[0].append(etree.Element("title"))
	r[0].append(etree.Element("link"))
	r[0].append(etree.Element("description"))
	r[0].append(etree.Element("lastBuildDate"))
	r[0].append(etree.Element("generator"))
	r[0].append(etree.Element("author"))
	r[0].append(etree.Element("{%s}author" % namespaces["itunes"]))
	r[0].append(etree.Element("{%s}image" % namespaces["itunes"], href=channel["artwork"]))
	r[0].append(etree.Element("logo"))
	r[0][0].text = channel["title"]
	r[0][1].text = channel["link"]
	r[0][2].text = channel["description"]
	r[0][3].text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
	r[0][4].text = "Mikrowelle OS"
	r[0][5].text = r[0][6].text = channel["author"]
	r[0][8].text = channel["artwork"]

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