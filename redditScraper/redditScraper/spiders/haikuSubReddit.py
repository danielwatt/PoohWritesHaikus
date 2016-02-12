# -*- coding: utf-8 -*-
import logging
import operator
import json
import sys
from wordnik import *
from unidecode import unidecode
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# Wordnik
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '65e27e829c6d8f4fed2830d67920fd1cabeed6b98014734f1'
client = swagger.ApiClient(apiKey, apiUrl)


logger = logging.getLogger('mycustomlogger')
wordHistogram = {}
symbolList = {',','?','.','"','!',';','[',']','*',' -','- ', '(', ')'}
wordDictionary = {}

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

    def start_requests(self):
        with open('wordCount.json') as data_file:    
            data = json.load(data_file)

        # wordApi = WordApi.WordApi(client)
        # for word in data:    
        #     syllables = wordApi.getHyphenation(word,
        #                              useCanonical=True)
        #     wordCharacteristic = {'partOfSpeech' : None, 'syllables' : None, 'associations': None, 'sentiment':None}
        #     if syllables:
        #         wordCharacteristic['syllables'] = len(syllables)
        #         wordDictionary[word] = wordCharacteristic
        #         print '%s : %d' %(word,len(syllables))
        
        # jsonFile = open('wordDictionary.json', 'w')
        # print 'were here'
        # print >>jsonFile, json.dumps(wordDictionary, sort_keys=True, indent=4, separators=(',',": "))
        # jsonFile.close()


        
        return super(HaikuSubRedditSpider, self).start_requests()


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
                    if word and word[0] is "'":
                        word = word[1:]

                    if word and word[len(word)-1] is "'":
                        word = word[:len(word)-2]

                    if word:
                        if word in wordHistogram:
                            wordHistogram[word] += 1
                        else:
                            wordHistogram[word] = 1

    def closed(self,reason):
        jsonFile = open('wordCount.json', 'w')
        print >>jsonFile, json.dumps(wordHistogram, sort_keys=True, indent=4, separators=(',',": "))
        jsonFile.close()

