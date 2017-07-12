# -*- coding: utf-8 -*-

REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': '',
    'db': 0
}

SETTINGS_KEY = 'settings:{}'
START_URLS_KEY = 'start_urls:{}'

MONGO_CONF = {
    'conf_table': {
        'host': '127.0.0.1',
        'port': 27017,
        'database': 'wizard',
        'collection': 'settings'
    }
}
