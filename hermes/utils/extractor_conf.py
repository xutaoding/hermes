# -*- coding: utf-8 -*-

""" The module extract spider config that configured on web terminal
    Basic spider conf kile:
        {
            # Control scrapy spider settings
            "scry_conf": {
                "COOKIES_ENABLED": False,
                ""DOWNLOAD_DELAY: 0
                ...
            },

            # Crawler web element settings
            "elements_conf": {
                "starter_urls": ["http://item.jd.com"],

                "goto_urls": "[#main-urls > a",],              # 从该页面的所要跳转到下一个页面的链接
                "pagination": ["div.next-pagination > a",],    # 该页面的翻页链接
                meta_field1: [field1_css_path, ],
                meta_field2: [field2_css_path, ],

                # 上一个页面经跳转链接(goto_urls)到该页面的信息
                "goto_next":{
                    "goto_urls": ["div.box.item > span > a",],     # 从该页面的所要跳转到下一个页面的链接
                    "pagination": ["div.next-pagination > a",]，   # 该页面的翻页链接
                    meta_field1: [field1_css_path, ],
                    meta_field2: [field2_css_path, ],

                    # 上一个页面经跳转链接(goto_urls)到该页面的信息
                    "goto_next": {
                        ...
                    }
                }
            },

            # Login or other Request Headers settings
            "request_conf": {
                "Cookie": "jssionid=ashdkhaskj;_username=12849fgsjk;",
                "Upgrade-Insecure-Requests": "1",
                ...
            }
        }

"""

from copy import deepcopy
from scrapy.utils.project import get_project_settings


class ExtractorConf(object):
    def __init__(self, spider_conf):
        self.base_conf = spider_conf

    @property
    def scrapy_settings(self):
        settings = {}
        scy_settings = get_project_settings()
        scrapy_settings = deepcopy(self.base_conf.get('scry_conf', {}))

        for scy_key, scy_val in scrapy_settings.iteritems():
            if scy_key not in scy_settings:
                continue

            settings[scy_key] = scy_val

        return settings

    @property
    def elements_settings(self):
        return {}

    @property
    def request_settings(self):
        return {}




