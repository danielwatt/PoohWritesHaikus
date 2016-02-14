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

class HaikuSubRedditSpider(CrawlSpider):
    name = "haikuSubReddit"
    allowed_domains = ["www.reddit.com"]
    start_urls = ['http://www.reddit.com/r/haiku/'] 
    wordDictionary = {}
    rules = [
    	Rule(LinkExtractor(
    		allow=['/r/haiku/\?count=\d*&after=\w*']),
    		callback='parse_start_url',
    		follow=True)
    ]

    def start_requests(self):
        with open('wordDictionary.json') as data_file:     
            self.wordDictionary = json.load(data_file)
            print 'Size of wordDict: %d' %(len(self.wordDictionary))
        return super(HaikuSubRedditSpider, self).start_requests()


    def parse_start_url(self, response):
        titles = response.xpath('//a[contains(@class, "title")]/text()').extract()
        for title in (titles):
            isHaiku = True
            title = unidecode(title)
            title = title.lower()
            for symbol in symbolList:
                title = title.replace(symbol,'')

            mylist = title.split("/")
            
            for lineNumber, line in enumerate(mylist): 
                wordList = line.split(" ")
                totalSyllables = 0

                for wordNumber, word in enumerate(wordList):

                    word = word.replace(' ','')
                    if word and word[0] is "'":
                        word = word[1:]

                    if word and word[len(word)-1] is "'":
                        word = word[:len(word)-2]

                    if word:
                        self.addToWordHistogram(word)
                        if word in self.wordDictionary:
                            totalSyllables += (self.wordDictionary[word])['syllables']
                            print totalSyllables


                if lineNumber is 0 or lineNumber is 2:
                    if totalSyllables is not 5:
                        isHaiku = False

                if lineNumber is 1:
                    if totalSyllables is not 7:
                        isHaiku = False
            if isHaiku:
                print title
            else:
                print 'The following is not a haiku /n %s' %(title)



    def addToWordHistogram(self, word):
        if word in wordHistogram:
            wordHistogram[word] += 1
        else:
            wordHistogram[word] = 1
            
    def closed(self,reason):
        jsonFile = open('wordCount.json', 'w')
        print >>jsonFile, json.dumps(wordHistogram, sort_keys=True, indent=4, separators=(',',": "))
        jsonFile.close()

