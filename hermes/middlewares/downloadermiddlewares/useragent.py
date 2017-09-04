import random

# from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from defaults import USER_AGENT


class HermesUserAgentMiddleware(object):
    def __init__(self):
        self.ua = USER_AGENT

    @property
    def user_agent(self):
        user_agent_list = [ua for ua_list in USER_AGENT.values() for ua in ua_list]
        return random.choice(user_agent_list)

    def process_request(self, request, spider):
        """ `UserAgentMiddleware` class execute order:
         1.`parity_platform.middlewares.downloadermiddleware.useragent.UserAgentMiddleware`
         2.`scrapy.downloadermiddlewares.useragent.UserAgentMiddleware`
            
        """
        request.headers['User-Agent'] = self.user_agent
        # print 'parity user agent:', request.headers
