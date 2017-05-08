from wikiInterface import *
from os import listdir
from localFeatures import *
from globalFeatures import *
from ranking import *
import re
import numpy as np
import time
from itertools import product, combinations

class trainAndTest:
	def __init__(self):
		self.lf = localFeatures()
		self.gf = globalFeatures()
	def pickACombo(self, disambi, content):
		results = {}
		firstItem = disambi[0]
		disambi = [[("Dummy", 0, 0)] if not i else i for i in disambi]
		for combi in product(*disambi):
			staleScore = 0
			for item in combi:
				if item[0] is not "Dummy":					
					staleScore += np.dot(np.array([-2.26840373, 0.57073083, 4.82051899, -2.66945871]), np.array(self.lf.compute(content, item[0], item[1], item[2])))

			combiScore = 0
			for (pair1, pair2) in combinations(combi, 2):
				if pair1[0] is not "Dummy" and pair2[0] is not "Dummy":
					combiScore += sum(self.gf.compute(pair1[0], pair2[0]))
			results[combi] = staleScore + combiScore
		s = sorted(results, key=results.get, reverse=True)
		print [a[0] for a in s[0]]
		return [a[0] for a in s[0]]


	def processAFile(self, file):
		content = open(file, "r").read()
		groundTruth = []
		disambi = []
		for r in re.finditer("\[\[(.*?)\]\]", content):
			croppedPart = r.group(1) 
			link = croppedPart
			text = croppedPart
			if "|" in croppedPart:
				link = croppedPart[:croppedPart.index("|")]
				text = croppedPart[croppedPart.index("|"):]

			if "|" in text:
				text = text[:text.index("|")]
			groundTruth.append((link, r.start(), r.end()))
			d = getDisambiguations(text)[:3]
			disambi.append(zip(d, [r.start()]*len(d), [r.end()]*len(d)))
		results = self.pickACombo(disambi, content)
		pureGroundTruths = [link for link,_,_ in groundTruth]
		print pureGroundTruths
		return sum([1 for mention1, mention2 in zip(results, pureGroundTruths) if mention1 == mention2])




if __name__ == "__main__":
	#print(trainAndTest().processAFile("data/WikipediaSample/OriginalTextsWithAnnotations/574"))
