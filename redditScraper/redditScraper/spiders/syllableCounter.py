# -*- coding: utf-8 -*-
import logging
import operator
import json
import sys
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

baseUrl = 'http://www.syllablecount.com/syllables/'

class SyllableCounterSpider(CrawlSpider):
	name = "syllableCounter"
	wordDictionary ={}
	allowed_domains = ["www.syllablecount.com"]
	start_urls = []
	rules = [
		Rule(LinkExtractor(
    		allow= None),
    		callback='parse',
    		follow=False)
	]

	def start_requests(self):
		with open('wordCount.json') as data_file:    
			data = json.load(data_file)

		for word in data:
			self.start_urls.append(baseUrl+word)

		return super(SyllableCounterSpider, self).start_requests()

	def parse(self,response):
		word = response.url.replace('http://www.syllablecount.com/syllables/', '')
		syllable = self.extractSyllableOfWord(response)
		self.addToWordDictionary(word, syllable)

	def extractSyllableOfWord(self, response):
		syllableExtract = response.xpath('//p[@id="ctl00_ContentPane_paragraphtext"]/b/text()').extract()
		syllable = None
		if syllableExtract[0]:
			syllable = int((syllableExtract[0])[0])
		return syllable

	def addToWordDictionary(self, word, syllable):
		wordCharacteristic = {'partOfSpeech' : None, 'syllables' : None, 'associations': None, 'sentiment':None}
		wordCharacteristic['syllables'] = syllable
		self.wordDictionary[word] = wordCharacteristic

	def closed(self,reason):
		jsonFile = open('wordDictionary.json', 'w')
		print 'HERE'
		print >>jsonFile, json.dumps(self.wordDictionary, sort_keys=True, indent=4, separators=(',',": "))
		jsonFile.close()