import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent


class HermesUserAgentMiddleware(object):
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        """ `UserAgentMiddleware` class execute order:
         1.`parity_platform.middlewares.downloadermiddleware.useragent.UserAgentMiddleware`
         2.`scrapy.downloadermiddlewares.useragent.UserAgentMiddleware`
            
        """
        request.headers['User-Agent'] = self.ua.random
        # print 'parity user agent:', request.headers
