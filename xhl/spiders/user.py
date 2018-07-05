# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy import Request

from xhl.db import Mysql


class UserSpider(scrapy.Spider):
    name = 'xhl_user'
    allowed_domains = ['www.xiaohulu.com']
    start_urls = ['http://www.xiaohulu.com/']

    url_gift = 'http://www.xiaohulu.com/test_spectator2/ajax_spec_price_range?t={time}&plat_id={plat}&from_id={roomid}'
    url_msg = 'https://www.xiaohulu.com/spectator2/ajax_spec_msg_range?t={time}&plat_id={plat}&from_id={roomid}'
    url_timeline = 'https://www.xiaohulu.com/spectator2/ajax_spec_price_period_range?t={time}&plat_id={plat}&from_id={roomid}'
    url_prefer = 'https://www.xiaohulu.com/spectator2/ajax_spec_source_gname_range?plat_id={plat}&from_id={roomid}'
    url_pug = 'https://www.xiaohulu.com/spectator2/ajax_spec_history?plat_id={plat}&from_id={roomid}'

    mysql = Mysql()
    custom_settings = {
        'CONCURRENT_REQUESTS': 60,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 30,
        # 'DOWNLOADER_MIDDLEWARES': {'xhl.middlewares.MyproxisSpiderMidleware': 125, }
        # 'LOG_LEVEL' : 'INFO'
        # 'ITEM_PIPELINES': {'xhl.pipelines.XhlPipeline': 300, },
    }



    def start_requests(self):
        mysql = Mysql()
        sql = 'SELECT * FROM `rich_id`'
        for item in mysql.get_two(sql):
            plat = item[1]
            roomid = item[0]
            yield Request(self.url_prefer.format(plat=plat, roomid=roomid), meta={'plat': plat, 'roomid': roomid},
                          callback=self.preferences)
            yield Request(self.url_pug.format(plat=plat, roomid=roomid), meta={'plat': plat, 'roomid': roomid},
                          callback=self.pug)
            for time in ['', 'm']:
                yield Request(url=self.url_gift.format(plat=plat, roomid=roomid, time=time),
                              meta={'time': time, 'plat': plat, 'roomid': roomid}, callback=self.gift)
                yield Request(self.url_msg.format(plat=plat, roomid=roomid, time=time),
                              meta={'time': time, 'plat': plat, 'roomid': roomid}, callback=self.msg)
                # yield Request(self.url_timeline.format(plat=plat, roomid=roomid, time=time),
                #               meta={'time': time, 'plat': plat, 'roomid': roomid}, callback=self.timeline)
        mysql.close_db()

    def parse(self, response):
        print(response.text)

    def gift(self, response):  # 礼物价值
        try:
            if response.meta['time'] == '':
                time = 't'
            else:
                time = response.meta['time']
            message = {
                'fromid': response.meta['roomid'],
                'plat': response.meta['plat'],
                'ranktype': '礼物价值趋势',
                'ranktime': time,
                'detail': response.text.replace('\\u', '\\\\u').replace('\'', '\\\''),
                'Crawltime': datetime.now().strftime('%Y-%m-%d'),
            }
            sql = 'replace into ' + self.mysql.get_sql_sentence('user_detail', message)
            print(sql)
            self.mysql.insert_one(sql)
        except Exception as e:
            with open('user.txt', 'a+') as f:
                f.write(response.url + '\n')
                f.write('error: %s \n' % e)

    def msg(self,response):  # 弹幕数量趋势
        if response.meta['time'] == '':
            time = 't'
        else:
            time = response.meta['time']
        message = {
            'fromid': response.meta['roomid'],
            'plat': response.meta['plat'],
            'ranktype': '弹幕数量趋势',
            'ranktime': time,
            'detail': response.text.replace('\\u', '\\\\u').replace('\'', '\\\''),
            'Crawltime': datetime.now().strftime('%Y-%m-%d'),
        }
        sql = 'replace into ' + self.mysql.get_sql_sentence('user_detail', message)
        print(sql)
        self.mysql.insert_one(sql)

    def timeline(self,response):  # 送礼时段分布
        if response.meta['time'] == '':
            time = 't'
        else:
            time = response.meta['time']
        message = {
            'fromid': response.meta['roomid'],
            'plat': response.meta['plat'],
            'ranktype': '送礼时段分布',
            'ranktime': time,
            'detail': response.text.replace('\\u', '\\\\u').replace('\'', '\\\''),
            'Crawltime': datetime.now().strftime('%Y-%m-%d'),
        }
        sql = 'replace into ' + self.mysql.get_sql_sentence('user_detail', message)
        print(sql)
        self.mysql.insert_one(sql)

    def preferences(self,response):  # 土豪偏好
        message = {
            'fromid': response.meta['roomid'],
            'plat': response.meta['plat'],
            'ranktype': '土豪偏好',
            'ranktime': 'm',
            'detail': response.text.replace('\\u', '\\\\u').replace('\'', '\\\''),
            'Crawltime': datetime.now().strftime('%Y-%m-%d'),
        }
        sql = 'replace into ' + self.mysql.get_sql_sentence('user_detail', message)
        print(sql)
        self.mysql.insert_one(sql)


    def pug_detail(mysql, response, plat, fromid):
        url1 = 'http://www.xiaohulu.com/test_spectator2/ajax_spec_history_list?plat_id={id}&from_id={fromid}&date={date}&p=1'
        result = re.findall("({.*?})", response.text)
        for item in result:
            info = json.loads(item)
            response = requests.get(url1.format(id=plat, fromid=fromid, date=info['date']), headers=headers)
            message = {
                'fromid': fromid,
                'plat': plat,
                'ranktime': info['date'],
                'detail': response.text.replace('\\u', '\\\\u').replace('\'', '\\\''),
                'Crawltime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            sql = 'replace into ' + mysql.get_sql_sentence('user_pug', message)
            print(sql)
            mysql.insert_one(sql)
            # print(message)

    def pug(self,response):  # 土豪足迹
        message = {
            'fromid': response.meta['roomid'],
            'plat': response.meta['plat'],
            'ranktype': '土豪足迹',
            'ranktime': 'm',
            'detail': response.text.replace('\'', '\\\''),
            'Crawltime': datetime.now().strftime('%Y-%m-%d'),
        }
        print(message)
        sql = 'replace into ' + self.mysql.get_sql_sentence('user_detail', message)
        print(sql)
        self.mysql.insert_one(sql)
        # pug_detail(mysql, response, plat, fromid)