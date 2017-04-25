import xml.etree.ElementTree as ET
import re, sys, os, pickle, string
import mwparserfromhell


def generateParsedArticles():
	tree = ET.parse('data/wikidump.xml')
	articlesWithout = {}
	articlesWith = {}
	i = 0
	for page in tree.iterfind('page'):
			title = page.iterfind('title').next().text
			if(":" not in title):
				content = page.iterfind('revision/text').next().text
				if content:
					wikicode = mwparserfromhell.parse(content)
					articlesWithout[title] = wikicode.strip_code()
					content = string.replace(content, "[[", "$$$$")
					content = string.replace(content, "]]", "$$$$")
					wikicode = mwparserfromhell.parse(content)
					articlesWith[title] = wikicode.strip_code()

				if(i%100 == 0):
					print str(i) + "\n"
				i = i + 1

	pickle.dump(articlesWithout, open("data/parsedArticles.pk", "w"))
	pickle.dump(articlesWith, open("data/parsedArticlesWith.pk", "w"))
