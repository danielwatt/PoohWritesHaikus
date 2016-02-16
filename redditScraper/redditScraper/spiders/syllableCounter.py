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
	currentWord = None

	def start_requests(self):
		with open('wordCount.json') as data_file:    
			data = json.load(data_file)

		for word in data:
			item = {}
			item['word'] = word
			tempWord = word.replace("'",'')
			request = scrapy.Request(baseUrl+tempWord, self.parse_Item)
			request.meta['item']=item
			yield request

		# return super(SyllableCounterSpider, self).start_requests()

	def parse_Item(self,response):
		print response.url
		item = response.meta['item']
		word = item['word']
		syllables = self.extractSyllableOfWord(response)
		self.addToWordDictionary(word,syllables)
		return item
		

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