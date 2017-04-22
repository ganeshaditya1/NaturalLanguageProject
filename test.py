import requests
import json
import html2text
import urllib

"""
url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Albert%20Einstein&utf8=&format=json'
data = requests.get(url)
masterArray = json.loads(data.text)
results = masterArray["query"]["search"]
for item in results:
	title = item["title"]
	wordsInTitle = title.split(" ")
	urlSafeTitle = "%20".join(wordsInTitle)
	print urlSafeTitle
plainText = html2text.html2text(text)
print(plainText)"""
"""https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=Stack%20Overflow"""


def getDisambiguations(word):
	baseUrl = "https://en.wikipedia.org/w/api.php?"
	basicParameters = {'action': 'query', 'format': 'json'}
	searchUrl = basicParameters.copy()
	searchUrl['list'] = 'search'
	searchUrl['srsearch'] = word
	searchUrl['utf8'] = ''
	finalSearchUrl = baseUrl + urllib.urlencode(searchUrl)
	searchResultsJson = requests.get(finalSearchUrl)
	print finalSearchUrl


getDisambiguations('Albert Einstein')

	
