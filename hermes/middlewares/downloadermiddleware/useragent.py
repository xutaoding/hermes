import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from defaults import USER_AGENT


class HermesUserAgentMiddleware(object):
    def __init__(self):
        self.user_agent = USER_AGENT

    def process_request(self, request, spider):
        """ `UserAgentMiddleware` class execute order:
         1.`parity_platform.middlewares.downloadermiddleware.useragent.UserAgentMiddleware`
         2.`scrapy.downloadermiddlewares.useragent.UserAgentMiddleware`
            
        """
        user_agent = random.choice(self.user_agent)

        if user_agent:
            request.headers.setdefault(b'User-Agent', user_agent)

        # print 'parity user agent:', request.headers
