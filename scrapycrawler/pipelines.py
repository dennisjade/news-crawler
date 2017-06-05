# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import logging

from pymongo.errors import ConnectionFailure

class MongoDBPipeline(object):

    collection_name = 'news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'isentia')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
      
        try:
          # The ismaster command is cheap and does not require auth.
          self.client.admin.command('ismaster')
          logging.info('Mongo client connected:'+self.mongo_uri)
        except Exception as e:
          print e.__doc__
          print 'message:' + e.message
          print e

    def close_spider(self, spider):
        logging.info('Closing MongoDB connection')
        self.client.close()

    def process_item(self, item, spider):
        logging.debug('Trying to insert/update to MongoDb: ',dict(item))
        try:
          self.db[self.collection_name].update({'url': item['url']}, dict(item), upsert=True)
          logging.info("News item added to MongoDB database!")
        except Exception as e:  
          print e.__doc__
          print('message:'+e.message)
          print e

        return item



