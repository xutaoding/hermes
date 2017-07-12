# -*- coding: utf-8 -*-

import os.path
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hermes.spiders.wizard import WizardSpider


def test_waizard_spider():
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(WizardSpider)
    crawler.start()


if __name__ == '__main__':
    pass
