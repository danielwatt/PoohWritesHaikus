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
	allowed_domains = ["www.syllablecount.com"]
	start_urls = [
		'http://www.syllablecount.com/syllables/Interest'
	]
	rules = [
		Rule(LinkExtractor(
    		allow=['/r/haiku/\?count=\d*&after=\w*']),
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
		print word
		