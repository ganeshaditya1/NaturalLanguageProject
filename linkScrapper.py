import xml.etree.ElementTree as ET
import re, sys, os, pickle
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



