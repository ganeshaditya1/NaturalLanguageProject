import xml.etree.ElementTree as ET
import re, sys, os, pickle, string
import mwparserfromhell

def computeLinks():
	tree = ET.parse('data/wikidump.xml')
	results = {}
	for page in tree.iterfind('page'):
		try:
			title = page.iterfind('title').next().text
			content = page.iterfind('revision/text').next().text
			inlinks = set()
			outlinks = set()
			if(title in results):
				inlinks = results[title][0]
				outlinks = results[title][1]

			wikicode = mwparserfromhell.parse(content)
			unfliteredLinks = wikicode.filter_wikilinks()
			links = set()
			for link in unfliteredLinks:
				link = link[2:len(link)-2]
				if(':' not in link):
					if('|' in link):
						links.add(link[:link.index('|')])
					else:
						links.add(link)


			for link in links:
				outlinks.add(link)
				if(link not in results):
					results[link] = [set(), set()]				
				results[link][0].add(title)
			if(inlinks or outlinks):
				results[title] = [inlinks, outlinks]
		except Exception as e:
		    exc_type, exc_obj, exc_tb = sys.exc_info()
		    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		    print(exc_type, fname, exc_tb.tb_lineno)
	pickle.dump(results, open('data/linksData.pk', 'w'))
	return results

class baseLine:
	def __init__(self):
		self.linkData = pickle.load(open("data/linksData.pk", "r"))

	def popularity(self):
		results = {}
		for title in self.linkData:
			for outLink in self.linkData[title][1]:
				if outLink not in results:
					results[outLink] = 0
				results[outLink] += 1
		pickle.dump(results, open("data/popularity.pk", "w"))
		return results

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

class contextGenerator:
	def __init__(self):
		return

	def cropAround(self, start, end, text):
		'''
		leftLen = start - 50 if (start - 50) >= 0 else 0
		rightLen = end + 50 if (end + 50) < len(text) else len(text) - 1
		'''
		left = string.replace(text[:start], "$$$$", "")
		right = string.replace(text[end:], "$$$$", "")
		start = len(left)
		end = 0
		leftLen = start - 50 if (start - 50) >= 0 else 0
		rightLen = end + 50 if (end + 50) < len(right) else len(right) - 1
		return left[leftLen:] + " " + right[:rightLen]

	def getContext(self):
		articlesList = pickle.load(open("data/parsedArticlesWith.pk", "r"))
		results = {}
		i = 0
		for title in articlesList:
			content = articlesList[title]
			for m in re.finditer(r'\$\$\$\$(.*)\$\$\$\$', content):
				link = m.group(0)
				if(':' not in link):
					if('|' in link):
						link = link[:link.index('|')]
					context = self.cropAround(m.start(0), m.end(0), content)
					if title not in results:
						results[title] = []
					results[title].append(context)
			if(i%100 == 0):
				print str(i) + "\n"
			i = i + 1
		pickle.dump(results, open('data/linkContexts.pk', 'w'))
		return results