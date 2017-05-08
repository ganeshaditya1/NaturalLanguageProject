from wikiInterface import *
from os import listdir
from localFeatures import *
from ranking import *
import re
import numpy as np
import time

def getWeights(location):
	listOfFiles = [f for f in listdir(location)]
	X = None
	Y = None
	local = localFeatures()

	for fileid, file in enumerate(listOfFiles):
		print str(fileid) + " Done"
		if fileid > 1000:
			break
		content = open(location + "/" + file).read()
		for r in re.finditer("\[\[(.*)\]\]", content):
			text = r.group(1)
			link = text
			if "|" in text:
				link = text[:text.index("|")]
				text = text[text.index("|"):]
			disambiguations = getDisambiguations(text)
			start = r.start()
			end = r.end()
			for item in disambiguations[:5]:
				s = local.compute(content, item, start, end)
				if s is not None:
					if X is None:
						X = np.array(s)
					else:
						X = np.vstack((X, np.array(s)))
					s1 = 0
					if item == link:
						s1 = 1
					if Y is None:
						Y = np.array([s1, fileid])
					else:
						Y = np.vstack((Y, np.array([s1, fileid])))
	ranker = RankSVM()
	ranker.fit(X, Y)
	return ranker.getWeights()

if __name__ == "__main__":
	print(getWeights("data/WikipediaSample/OriginalTextsWithAnnotations"))



