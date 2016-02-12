# -*- coding: utf-8 -*-
import scrapy


class CrawlSpider(scrapy.Spider):
    name = "crawl"
    allowed_domains = ["syllableCounter"]
    start_urls = (
        'http://www.syllableCounter/',
    )

    def parse(self, response):
        pass
