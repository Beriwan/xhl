# -*- coding: utf-8 -*-
import json
import re
import time
from datetime import datetime

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from xhl.db import Mysql
from xhl.items import *


class XiohuluSpider(scrapy.Spider):
    name = 'xhl_detail'
    allowed_domains = ['www.xioahulu.com']
    start_urls = ['http://www.xioahulu.com/']

    url_anchor_price = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_price_tyrants?plat_id={plat}&room_id={roomid}&t={time}'
    url_source_gname = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_source_gname_range?plat_id={plat}&room_id={roomid}&t={time}'
    url_price_list = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_price_list?plat_id={plat}&room_id={roomid}&t={time}'
    url_anchor_timeline = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_timeline_range?plat_id={plat}&room_id={roomid}&t={time}'
    url_anchor_other = 'http://www.xiaohulu.com/anchor2/details/?plat={plat}&roomid={roomid}'

    custom_settings = {
        'CONCURRENT_REQUESTS': 150,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 50,
        # 'LOG_LEVEL' : 'INFO'
        # 'DOWNLOAD_TIMEOUT': 30,
        # 'DOWNLOADER_MIDDLEWARES': {'xhl.middlewares.MyproxisSpiderMidleware': 125, },
        'ITEM_PIPELINES': {'xhl.pipelines.XhlPipeline': 300, },
    }

    mysql = Mysql()
    def start_requests(self):
        mysql = Mysql()
        sql = 'SELECT DISTINCT plat,roomid FROM rank_history WHERE plat and roomid is not NULL AND ranktype != \'水军榜\' AND ranktype != \'土豪榜\''
        for item in mysql.get_two(sql):
            plat = item[0]
            roomid = item[1]
            yield Request(self.url_anchor_other.format(plat=plat, roomid=roomid),meta={'plat':plat,'roomid':roomid,'num':2},callback=self.others)
            time = ''
            yield Request(url=self.url_anchor_price.format(plat=plat,roomid=roomid,time=time),meta={'time': time,'plat':plat,'roomid':roomid},callback=self.rich_gift)
            yield Request(self.url_source_gname.format(plat=plat, roomid=roomid, time=time),meta={'time': time,'plat':plat,'roomid':roomid},callback=self.preferences)
            yield Request(self.url_price_list.format(plat=plat, roomid=roomid, time=time),meta={'time': time,'plat':plat,'roomid':roomid,'num':1},callback=self.price_list)
            # for time in ['w', 'm']:
            #     yield Request(self.url_anchor_timeline.format(plat=plat, roomid=roomid, time=time),meta={'time': time,'plat':plat,'roomid':roomid},callback=self.timeline)
        mysql.close_db()

    def rich_id(self,list):
        sql = "replace into rich_id(roomid,plat,name)values(%s,%s,%s)"
        # # print(sql)
        self.mysql.insert_sql_many(sql,list)

    def price_list(self,response): #礼物活跃排行榜
        if response.meta['num'] == 1:
            if response == []:
                yield Request(self.url_price_list.format(plat=response.meta['plat'], roomid=response.meta['roomid'], time=response.meta['time']),
                              meta={'time': response.meta['time'], 'plat': response.meta['plat'], 'roomid': response.meta['roomid'],}, callback=self.price_list)
            else:
                item = XhlItem()
                list_price = []
                text = response.text[:-1] + ',' + response.text[-1:]
                result = re.findall("({.*?}),", text)
                if len(result) != 0:
                    for ns in result:
                        n = json.loads(ns)
                        rich_set = (n['from_id'], n['platform_id'], n['from_name'])
                        list_price.append(rich_set)
                    self.rich_id(list_price)
                if response.meta['time'] == '':
                    time = 't'
                else:
                    time = response.meta['time']
                item['roomid'] = response.meta['roomid']
                item['plat'] = response.meta['plat']
                item['ranktype'] = '礼物活跃排行榜'
                item['ranktime'] = time
                item['detail'] = response.text.replace('\\u', '\\\\u').replace('\'', '\\\'')
                item['Crawltime'] = datetime.now().strftime('%Y-%m-%d')
                yield item
                # sql = 'insert into ' + self.mysql.get_sql_sentence(anchor_table, message)
                # print(sql)
                # self.mysql.insert_one(sql)
        else:
            item = XhlItem()
            list_price = []
            text = response.text[:-1]+','+ response.text[-1:]
            result = re.findall("({.*?}),", text)
            if len(result) != 0:
                for ns in result:
                    n = json.loads(ns)
                    rich_set = (n['from_id'],n['platform_id'],n['from_name'])
                    list_price.append(rich_set)
                self.rich_id(list_price)
            if response.meta['time'] == '':
                time = 't'
            else:
                time = response.meta['time']
            item['roomid'] = response.meta['roomid']
            item['plat'] = response.meta['plat']
            item['ranktype'] = '礼物活跃排行榜'
            item['ranktime'] = time
            item['detail']=response.text.replace('\\u','\\\\u').replace('\'','\\\'')
            item['Crawltime'] = datetime.now().strftime('%Y-%m-%d')
            yield item
            # sql = 'insert into ' + self.mysql.get_sql_sentence(anchor_table, message)
            # print(sql)
            # self.mysql.insert_one(sql)

    def rich_gift(self, response):  #送礼土豪
        item = XhlItem()
        if response.meta['time'] == '':
            time = 't'
        else:
            time = response.meta['time']
        item['roomid'] = response.meta['roomid']
        item['plat'] = response.meta['plat']
        item['ranktype'] = '送礼土豪'
        item['ranktime'] = time
        item['detail'] = response.text.replace('\\u', '\\\\u').replace('\'', '\\\'')
        item['Crawltime'] = datetime.now().strftime('%Y-%m-%d')
        yield item

    def preferences(self, response):  #土豪偏好
        item = XhlItem()
        if response.meta['time'] == '':
            time = 't'
        else:
            time = response.meta['time']
        item['roomid'] = response.meta['roomid']
        item['plat'] = response.meta['plat']
        item['ranktype'] = '土豪偏好'
        item['ranktime'] = time
        item['detail'] = response.text.replace('\\u', '\\\\u').replace('\'', '\\\'')
        item['Crawltime'] = datetime.now().strftime('%Y-%m-%d')
        yield item

    def timeline(self, response):  #土豪活跃时段
        item = XhlItem()
        if response.meta['time'] == '':
            time = 't'
        else:
            time = response.meta['time']
        item['roomid'] = response.meta['roomid']
        item['plat'] = response.meta['plat']
        item['ranktype'] = '土豪活跃时段'
        item['ranktime'] = time
        item['detail'] = response.text.replace('\\u', '\\\\u').replace('\'', '\\\'')
        item['Crawltime'] = datetime.now().strftime('%Y-%m-%d')
        yield item

    def get_table(self,index, response, timestr, data, dict):
        key = 'case{index}'.format(index=index)
        text = 'case {index}:(.*?)obj.str '.format(index=index)
        try:
            table1 = re.search(text, response.text, re.S).group(1).strip()
            dict[key] = timestr.search(table1).group(1).strip().replace('\"', '') + ',' + data.search(table1).group(
                1).strip().replace('\"', '')
        except Exception:
            with open('detail.txt', 'a+') as f:
                f.write(response.url + '\n')
                f.write(str(index))
            dict[key] = ''




    def others(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        achievements = soup.select('.container .a_card_r2')
        list = []
        for achieve in achievements:  # 单场最高成就
            for i in range(0, len(achieve.select('dl dd p'))):
                list.append(achieve.select('dl dd p')[i].string.strip())
        # print(list)
        rankindexs = soup.select('.a_card_r1.a_card_r3 .rank_j li i')
        indexs = []
        for rankindex in rankindexs:  # 主播指数排名
            indexs.append(rankindex.get_text().strip())
        # print(indexs)
        r_gift = soup.select('.cb_left5_r dl dd')  # 最新收取送礼列表
        gift_list = []
        for item in r_gift:
            if item.get_text().strip() != '':
                gift_list.append(item.get_text().strip().replace('\u200e', '').replace('\u202d', ''))
            if item.select('img'):
                gift_list.append(item.select('img')[0]['src'])
        # print(gift_list)
        dict = {}
        timestr = re.compile('obj.timestr =(.*?);')
        data = re.compile('obj.data =(.*?);')
        for i in range(3, 17):
            self.get_table(i, response, timestr, data, dict)
        # print(json.dumps(dict))
        anchor = soup.select('.a_card_left ul li')
        anchor_list = []  #主播个人信息
        for item in anchor[:-1]:
            if item.get_text().strip() != '':
                anchor_list.append(item.get_text().strip())
            if item.select('img'):
                anchor_list.append(item.select('img')[0]['src'])
        # print(anchor_list)
        item = otherItem()
        item['roomid'] = response.meta['roomid']
        item['plat'] = response.meta['plat']
        item['anchor'] = str(anchor_list).replace('\'', '\\\'')
        item['achieve'] = str(list).replace('\'', '\\\'')
        item['rankindex'] = str(indexs).replace('\'', '\\\'')
        item['Crawltime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['gift'] = str(gift_list).replace('\'', '\\\'')
        item['table'] = json.dumps(dict)
        if item['anchor'] == []:
            with open('detail.txt', 'a+') as f:
                f.write(response.url + '\n')
        else:
            yield item

