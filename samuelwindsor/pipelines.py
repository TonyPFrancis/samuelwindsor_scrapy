# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class SamuelwindsorPipeline(object):
    def __init__(self):
        self.db = MongoClient('127.0.0.1').samuelwindsordata

    def process_item(self, item, spider):
        self.db.productinfo.insert(dict(item))
        return item
