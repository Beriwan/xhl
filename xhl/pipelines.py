# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from xhl.db import Mysql
from xhl.items import *


class XhlPipeline(object):

    def __init__(self):
        self.mysql = Mysql()

    def close_spider(self,spider):
        self.mysql.close_db()

    def process_item(self, item, spider):
        if isinstance(item, XhlItem):
            sql_tb_wdetail = 'replace into ' + self.mysql.get_sql_sentence('anchor_test', item)
            # print(sql_tb_wdetail)
            self.mysql.insert_one(sql_tb_wdetail)
        elif isinstance(item, otherItem):
            sql_tb_wdetail = 'replace into ' + self.mysql.get_sql_sentence('anchor_detail', item)
            # print(sql_tb_wdetail)
            self.mysql.insert_one(sql_tb_wdetail)

        return item
