# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo import IndexModel, ASCENDING
from WebHub.items import PornVideoItem


class PornhubMongoDBPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient(host="localhost", port=27017)
        db = clinet["Video"]
        self.PhRes = db["Data"]
        idx = IndexModel([('link_url', ASCENDING)], unique=True)
        self.PhRes.create_indexes([idx])
        # if your existing DB has duplicate records, refer to:
        # https://stackoverflow.com/questions/35707496/remove-duplicate-in-mongodb/35711737

    def process_item(self, item, spider):
        print('MongoDBItem', item)
        """ 判断类型 存入MongoDB """
        if isinstance(item, PornVideoItem):
            print('PornVideoItem True')
            try:
                self.PhRes.update_one({'link_url': item['link_url']}, {'$set': dict(item)}, upsert=True)
            except Exception:
                pass
        return item
