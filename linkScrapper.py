import xml.etree.ElementTree as ET
import re, sys, os, pickle

def computeLinks():
	return pickle.load(open('data/linksData.pk', "r"))
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

			links = set(re.findall(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', content))
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

