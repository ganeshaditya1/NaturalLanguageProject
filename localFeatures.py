import xml.etree.ElementTree as ET
import re, sys, os, pickle
import mwparserfromhell

class localFeatures:
	def __init__(self):
		return



	def cropAround(self, start, end, text):
		'''
		leftLen = start - 50 if (start - 50) >= 0 else 0
		rightLen = end + 50 if (end + 50) < len(text) else len(text) - 1
		'''
		leftLen = start - 200 if (start - 200) >= 0 else 0
		rightLen = end + 200 if (end + 200) < len(text) else len(text) - 1
		left = text[leftLen:start]
		left = mwparserfromhell.parse(left).strip_code()
		right = text[end:rightLen]
		right = mwparserfromhell.parse(right).strip_code()
		start = len(left)-1
		end = 0

		leftLen = start - 50 if (start - 50) >= 0 else 0
		rightLen = end + 50 if (end + 50) < len(right) else len(right) - 1
		return mwparserfromhell.parse(left[leftLen:] + " " + right[:rightLen])
	def getContext(self):
		tree = ET.parse('data/wikidump.xml')
		results = {}
		for page in tree.iterfind('page'):
			title = page.iterfind('title').next().text
			content = page.iterfind('revision/text').next().text
			if content:
				for m in re.finditer(r'\[\[(.*)\]\]', content):
					link = m.group(1)
					if(':' not in link):
						if('|' in link):
							link = link[:link.index('|')]
						context = self.cropAround(m.start(0) - 2, m.end(0) + 2, content)
						if title not in results:
							results[title] = []
						results[title].append(context)
		pickle.dump(results, open('data/linkContexts.pk', 'w'))
		return results

A = localFeatures()
A.getContext()