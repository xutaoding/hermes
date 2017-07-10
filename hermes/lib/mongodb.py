# -*- coding: utf-8 -*-

import logging
import types

import pymongo

mongo_log = logging.getLogger(__name__)


class MongoClient(object):
    def __init__(self, host='localhost', port=27017, database=None, collection=None, **kwargs):
        self.host = host
        self.port = port
        self.db = database
        self.table = collection

        if self.db is None or self.table is None:
            raise ValueError('Key-Word arguments: Lack of `database` and `collection`')

        self.__client = None
        self.__options = kwargs

    def __connect(self):
        try:
            if self.__client is None:
                self.__client = pymongo.MongoClient(self.host, self.port, **self.__options)

            self.__database = self.__client[self.db]
            self.__collection = self.__database[self.table]
        except Exception as e:
            mongo_log.info('Connect mongo<{} {}> failed: [{}]'.format(self.host, self.port, e))

    def get(self, q_kw=None, *args, **kwargs):
        """ Only find one document """
        self.__connect()
        return self.__collection.find_one(q_kw, *args, **kwargs)

    def query(self, q_kw=None, fields=None, sort_by=None, use_iterators=True, *args, **kwargs):
        """ Find a set of document with condition
            Sometimes because of memory, cause `MemoryError` exception
         """
        if not isinstance(sort_by, (tuple, types.NoneType)):
            raise TypeError('meth: query, `sort_by` keyword type error')

        if not isinstance(fields, dict):
            raise TypeError('meth: query, `fields` keyword type error')

        self.__connect()

        skip = kwargs.pop('skip', 0)
        limit = kwargs.pop('limit', 0)  # 0 hint to get overall document

        args = (q_kw, ) + args
        kwargs['projection'] = fields
        sort_by = sort_by or [('_id', pymongo.DESCENDING)]

        cursor = self.__collection.find(*args, **kwargs).sort(sort_by)

        if use_iterators:
            return cursor.skip(skip).limit(limit)
        return [doc for doc in cursor]

    def distinct(self, key, *args, **kwargs):
        self.__connect()
        return self.__collection.distinct(key, *args, **kwargs)

    def insert(self, doc_or_docs, **kwargs):
        self.__connect()

        if isinstance(doc_or_docs, dict):
            document = doc_or_docs
            return self.__collection.insert_one(document, **kwargs)

        if isinstance(doc_or_docs, (list, tuple)):
            documents = doc_or_docs
            return self.__collection.insert_many(documents, **kwargs)

        raise ValueError('meth: insert, type of `doc_or_docs` error')

    def update(self, q_kw, doc_or_docs, **kwargs):
        """ Update documents by condition to mongo """
        self.__connect()

        if isinstance(doc_or_docs, dict):
            document = doc_or_docs
            return self.__collection.update_one(q_kw, document, **kwargs)

        if isinstance(doc_or_docs, (list, tuple)):
            documents = doc_or_docs
            return self.__collection.update_many(q_kw, documents, **kwargs)

        raise ValueError('meth: update, type of `doc_or_docs` error')

    def delete(self, q_kw, **kwargs):
        self.__connect()

        return self.__collection.remove(q_kw, **kwargs)

    def close(self):
        try:
            self.__client.close()
        except AttributeError:
            pass

        self.__client = None


if __name__ == '__main__':
    # coll = NoSQLMongo('localhost', 27017, 'taobao', 'jd_shuid')
    coll = NoSQLMongo('localhost', 27017, 'taobao', 'tmall')

    _q_kw = {"productAttr": {'$exists': False}}
    print coll.query(_q_kw).count()
    # for index, doc in enumerate(coll.query(_q_kw, skip=100 * 10)):
    #     print index

    # print coll.query(_q_kw, limit=10000).count(True)
    # print coll.query(_q_kw, skip=10000).count(True)
