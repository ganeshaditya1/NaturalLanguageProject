import xml.etree.ElementTree as ET
import re, sys, os, pickle, string
import mwparserfromhell
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class localFeatures:
	def __init__(self):
		self.contexts = pickle.load(open("data/linkContexts.pk", "r"))
		self.articles = pickle.load(open("data/parsedArticles.pk", "r"))
		return
	def text2text(self, text1, title):
		text1 = self.parsedText
		text2 = self.articles[title]
		vocab = text1 + " " + text2
		vect = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word', stop_words='english', vocabulary=list(set(vocab.split())))
		v1 = vect.fit_transform([text1])
		v2 = vect.fit_transform([text2])
		return cosine_similarity(v1, v2)[0][0]

	def text2context(self, text, title):
		text = self.parsedText
		text1 = self.joinedContexts
		vocab = text1 + text
		vect = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word', stop_words='english', vocabulary=list(set(vocab.split())))
		sum = np.array([])
		v1 = vect.fit_transform([text])
		for context in self.contexts[title]:
			v2 = vect.fit_transform([context])
			sum = np.append(sum, cosine_similarity(v1, v2)[0][0])
		return np.average(sum)

	def __contextExtractor__(self, text, start, end):
		left = text[:start]
		right = text[end:]
		final = left + " " + right
		wikicode = mwparserfromhell.parse(final)
		return wikicode.strip_code()

	def context2text(self, text, link, start, end):
		text1 = self.context
		text2 = self.articles[link]
		vocab = text1 + " " + text2
		vect = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word', stop_words='english', vocabulary=list(set(vocab.split())))
		v1 = vect.fit_transform([text1])
		v2 = vect.fit_transform([text2])
		return cosine_similarity(v1, v2)[0][0]

	def context2context(self, text, link, start, end):
		text1 = self.context
		text2 = self.joinedContexts
		vocab = text1 + " " + text2
		vect = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word', stop_words='english', vocabulary=list(set(vocab.split())))		
		sum = np.array([])
		v1 = vect.fit_transform([text1])
		for context in self.contexts[link]:
			v2 = vect.fit_transform([context])
			sum = np.append(sum, cosine_similarity(v1, v2)[0][0])
		return np.average(sum)

	def compute(self, text, link, start, end):
		if link in self.contexts:
			self.context = self.__contextExtractor__(text, start, end)
			wikicode = mwparserfromhell.parse(text)
			self.parsedText = wikicode.strip_code()
			self.joinedContexts = " ".join(self.contexts[link])
			return [self.text2text(text, link), self.text2context(text, link), self.context2text(text, link, start, end), self.context2context(text, link, start, end)]
		return None
'''
import pickle
A = pickle.load(open("data/parsedArticles.pk", "r"))
s = localFeatures()
print(s.compute(open("s", "r").read(), "Cancer", 558, 582))
print(s.compute(open("s", "r").read(), "Cuba", 558, 582))
print(s.compute(open("s", "r").read(), "Microsoft", 558, 582))
'''
