# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy_webdriver.http import WebdriverRequest


class AccessCounterSpider(BaseSpider):
    """ access counter.
    """
    name = 'access_counter'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com']

    def __init__(self, *args, **kwargs):
        super(AccessCounterSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """ main method
        """
        yield WebdriverRequest(response.url, callback=self._spider_page, method="GET")

    def _spider_page(self, response):
        """ scraping page
        """
        yield response.action_request()
