# -*- coding: utf-8 -*-
import logging
import operator
import json
import sys
from unidecode import unidecode
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger('mycustomlogger')
wordDictionary = {}
symbolList = {',','?','.','"','!',';','[',']','*',' -','- ', '(', ')'}
replaceUnicodeList = { u'\u2019':'′' }

class HaikuSubRedditSpider(CrawlSpider):
    name = "haikuSubReddit"
    allowed_domains = ["www.reddit.com"]
    start_urls = ['http://www.reddit.com/r/haiku/'] 
    rules = [
    	Rule(LinkExtractor(
    		allow=['/r/haiku/\?count=\d*&after=\w*']),
    		callback='parse_start_url',
    		follow=True)
    ]

    def parse_start_url(self, response):
        titles = response.xpath('//a[contains(@class, "title")]/text()').extract()
        for title in (titles):
            title = unidecode(title)
            title = title.lower()
            for symbol in symbolList:
                title = title.replace(symbol,'')

            mylist = title.split("/")
            
            for lineNumber, line in enumerate(mylist): 
                wordList = line.split(" ")

                for wordNumber, word in enumerate(wordList):
                    word = word.replace(' ','') 
                    if word != '':
                        if word in wordDictionary:
                            wordDictionary[word] += 1
                        else:
                            wordDictionary[word] = 1

    def closed(self,reason):
        jsonFile = open('wordCount.json', 'w')
        print >>jsonFile, json.dumps(wordDictionary, sort_keys=True, indent=4, separators=(',',": "))


