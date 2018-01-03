# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import pandas as pd

class Scrapy1Pipeline(object):
    def process_item(self, item, spider):
        return item

class TocsvPipeline(object):
    def __init__(self):
        self.df = pd.DataFrame(columns=['ranking', 'movie_name', 'score', 'score_num'])
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        self.df = self.df.append(dict(item), ignore_index=True)
        return item

    def spider_closed(self, spider):
        self.df.to_csv('wahaha.csv')
        print('====> save csv file to wahaha.csv')
