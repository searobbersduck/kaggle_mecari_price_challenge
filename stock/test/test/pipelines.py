# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import pandas as pd


class TestPipeline(object):
    def __init__(self):
        self.file = codecs.open('csdn_semantics.json', 'w', encoding='utf-8')
        self.df = pd.DataFrame(columns=['ranking', 'movie_name', 'score', 'score_num'])


    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.df = self.df.append(dict(item), ignore_index=True)
        self.df.to_csv('movies.csv')
        return item

    def spider_closed(self, spider):
        print(len(self.df))
        print('=====================================================================')
        self.df.to_csv('movies.csv')
        self.file.close()

