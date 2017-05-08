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
	baseUrl = "https://simple.wikipedia.org/w/api.php?"
	basicParameters = {'action': 'query', 'format': 'json', 'utf8': ''}
	searchUrl = basicParameters.copy()
	searchUrl['list'] = 'search'
	try:
		searchUrl['srsearch'] = word.encode('utf-8')
		searchUrl['srlimit'] = 20
		finalSearchUrl = baseUrl + urllib.urlencode(searchUrl)
		searchResultsJson = requests.get(finalSearchUrl)
		searchResultsArray = json.loads(searchResultsJson.text)
		if "query" in searchResultsArray:
			results = searchResultsArray["query"]["search"]
			data = []
			for result in results:
				title = result["title"]
				'''
				summaryUrl = basicParameters.copy()
				summaryUrl['prop'] = 'extracts'
				summaryUrl['exintro'] = ''
				summaryUrl['explaintext'] = ''
				summaryUrl['titles'] = title.encode('utf-8')
				summaryUrlFinal = baseUrl + urllib.urlencode(summaryUrl)
				summaryJson = requests.get(summaryUrlFinal)
				summaryArray = json.loads(summaryJson.text)
				'''
				data.append(title)
			return data
		else:
			return []
	except Exception as e:
		return []


	
