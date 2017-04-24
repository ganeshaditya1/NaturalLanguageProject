from linkScrapper import *
import math
class globalFeatures:
	def __init__(self):
		self.linkData = computeLinks()
	def PMI(self, t1, t2):
		if(not t1 or not t2):
			return
		L1 = float(len(t1))
		L2 = float(len(t2))
		W = float(len(self.linkData))
		intersection = float(len(t1.intersection(t2)))
		return (intersection/W)/((L1/W) * (L2/W))

	def NGD(self, t1, t2):
		if(not t1 or not t2):
			return
		L1 = float(len(t1))
		L2 = float(len(t2))
		W = float(len(self.linkData))
		intersection = float(len(t1.intersection(t2)))
		return (math.log(max(L1, L2)) - math.log(intersection))/(math.log(W) - math.log(min(L1, L2)))
	def compute(self, t1, t2):
		t1In = self.linkData[t1][0]
		t2In = self.linkData[t2][0]		
		t1Out = self.linkData[t1][1]
		t2Out = self.linkData[t2][1]
		if(t1 not in t2In or t2 not in t1In):
			return [0, 0, 0, 0]
		else:
			inLinksPMI = self.PMI(t1In, t2In)
			inLinksNGD = self.NGD(t1In, t2In)
			outLinksPMI = self.PMI(t1Out, t2Out)
			outLinksNGD = self.NGD(t1Out, t2Out)
			def avg(a, b):
				return (a + b)/2
			return [avg(inLinksNGD, inLinksPMI), avg(outLinksNGD, outLinksPMI),  max(inLinksPMI, inLinksNGD), max(outLinksPMI, outLinksNGD)]




