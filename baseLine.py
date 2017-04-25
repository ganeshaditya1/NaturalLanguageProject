from linkScrapper import *
class baseLine:
	def __init__(self):
		self.linkData = computeLinks()

	def popularity(self):
		results = {}
		for title in self.linkData:
			for outLink in self.linkData[title][1]:
				if outLink not in results:
					results[outLink] = 0
				results[outLink] += 1
		return results