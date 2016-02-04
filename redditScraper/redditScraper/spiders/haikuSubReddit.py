# -*- coding: utf-8 -*-
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger('mycustomlogger')

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
            logger.info(title)
            title = title.replace(',','')
            title = title.replace('?','')
            title = title.replace('.','')
            logger.info(title)
            mylist = title.split("/")
            
            for lineNumber, line in enumerate(mylist): 
                wordList = line.split(" ")

                logger.info("Line Number %d" % lineNumber)
                for wordNumber, word in enumerate(wordList): 
                    logger.info("%d: %s" % (wordNumber,word))


