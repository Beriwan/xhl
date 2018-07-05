# coding=UTF-8
import json
import re
from datetime import datetime
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup

from xhl.db import Mysql


class Anchordetail(object):

    def __init__(self):
        self.headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                }
        self.times = ['','w','m']
        self.mysql = Mysql()


    def rich_gift(self, roomid, plat):  #送礼土豪
        for time in self.times:
            url  = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_price_tyrants?plat_id={plat}&room_id={roomid}&t={time}'.format(plat=plat,roomid=roomid,time=time)
            response = requests.get(url, headers=self.headers)
            if time == '':
                time = 't'
            message = {
                'roomid': roomid,
                'plat': plat,
                'ranktype':'送礼土豪',
                'ranktime':time,
                'detail':response.text.replace('\\u','\\\\u').replace('\'','\\\''),
                'Crawltime': datetime.now().strftime('%Y-%m-%d'),
            }
            sql = 'replace into ' + self.mysql.get_sql_sentence('anchor_test',message)
            print(sql)
            self.mysql.insert_one(sql)



    def preferences(self, roomid, plat): #土豪偏好
        for time in self.times:
            url  = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_source_gname_range?plat_id={plat}&room_id={roomid}&t={time}'.format(plat=plat,roomid=roomid,time=time)
            response = requests.get(url, headers=self.headers)
            if time == '':
                time = 't'
            message = {
                'roomid': roomid,
                'plat': plat,
                'ranktype': '土豪偏好',
                'ranktime': time,
                'detail': response.text.replace('\\u','\\\\u').replace('\'','\\\''),
                'Crawltime': datetime.now().strftime('%Y-%m-%d'),
            }
            sql = 'replace into ' + self.mysql.get_sql_sentence('anchor_test', message)
            print(sql)
            self.mysql.insert_one(sql)

    def rich_id(self,roomid,plat,name):
        message1 = {
            'roomid': roomid,
            'plat': plat,
            'name': name,
        }
        sql = 'replace into ' + self.mysql.get_sql_sentence('rich_id', message1)
        # print(sql)
        self.mysql.insert_one(sql)


    def price_list(self, roomid, plat): #礼物活跃排行榜
        for time in self.times:
            url  = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_price_list?plat_id={plat}&room_id={roomid}&t={time}'.format(plat=plat,roomid=roomid,time=time)
            response = requests.get(url, headers=self.headers)
            text = response.text[:-1]+','+ response.text[-1:]
            result = re.findall("({.*?}),", text)
            if len(result) != 0:
                for item in result:
                    item = json.loads(item)
                    self.rich_id(item['from_id'],item['platform_id'],item['from_name'])
            if time == '':
                time = 't'
            message = {
                'roomid': roomid,
                'plat': plat,
                'ranktype': '礼物活跃排行榜',
                'ranktime': time,
                'detail': response.text.replace('\\u','\\\\u').replace('\'','\\\''),
                'Crawltime': datetime.now().strftime('%Y-%m-%d'),
            }
            sql = 'replace into ' + self.mysql.get_sql_sentence('anchor_test', message)
            print(sql)
            self.mysql.insert_one(sql)


    def timeline(self, roomid, plat): #土豪活跃时段
        times = ['w', 'm']
        for time in times:
            url  = 'https://www.xiaohulu.com/test_anchor2/ajax_anchor_timeline_range?plat_id={plat}&room_id={roomid}&t={time}'.format(plat=plat,roomid=roomid,time=time)
            response = requests.get(url, headers=self.headers)
            if time == '':
                time = 't'
            message = {
                'roomid': roomid,
                'plat':plat,
                'ranktype': '土豪活跃时段',
                'ranktime': time,
                'detail': response.text.replace('\\u','\\\\u').replace('\'','\\\''),
                'Crawltime': datetime.now().strftime('%Y-%m-%d'),
            }
            sql = 'replace into ' + self.mysql.get_sql_sentence('anchor_test', message)
            print(sql)
            self.mysql.insert_one(sql)

    def get_table(self,index, response, timestr, data, dict):
        key = 'case{index}'.format(index=index)
        text = 'case {index}:(.*?)obj.str '.format(index=index)
        table1 = re.search(text, response.text, re.S).group(1).strip()
        dict[key] = timestr.search(table1).group(1) + ',' + data.search(table1).group(1)


    def others(self,roomid,plat):
        url = 'http://www.xiaohulu.com/anchor2/details/?plat={plat}&roomid={roomid}'.format(plat=plat, roomid=roomid)
        response = requests.get(url, headers=self.headers)
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
        self.get_table(0, response, timestr, data, dict)
        for i in range(2, 17):
            self.get_table(i, response, timestr, data, dict)
        # print(dict)
        anchor = soup.select('.a_card_left ul li')
        anchor_list = []  #主播个人信息
        for item in anchor[:-1]:
            if item.get_text().strip() != '':
                anchor_list.append(item.get_text().strip())
            if item.select('img'):
                anchor_list.append(item.select('img')[0]['src'])
        # print(anchor_list)
        message = {
            'roomid': roomid,
            'plat': plat,
            'anchor':str(anchor_list).replace('\'', '\\\''),
            'achieve': str(list).replace('\'', '\\\''),
            'rankindex': str(indexs).replace('\'', '\\\''),
            'crawltime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'gift': str(gift_list).replace('\'', '\\\''),
            'table': str(dict).replace('\'', '\\\''),
        }
        sql = 'replace into ' + self.mysql.get_sql_sentence('anchor_detail', message)
        print(sql)
        self.mysql.insert_one(sql)



    def main(self,roomid,plat):
        self.rich_gift(roomid,plat)
        self.preferences(roomid,plat)
        self.price_list(roomid,plat)
        self.timeline(roomid,plat)
        self.others(roomid, plat)

    def get(self):
        with open('detail.txt','r') as f:
            items = f.readlines()
        with open('detail.txt','w') as f_w:
            for item in items:
                plat = re.search('\?plat=(\d+)&',item).group(1)
                roomid = re.search('&roomid=(\d+)',item).group(1)
                try:
                    self.main(roomid,plat)
                except Exception:
                        f_w.write(item + '\n')


    def run(self):
        self.get()
        self.mysql.close_db()

if __name__ == '__main__':
    anchor = Anchordetail()
    anchor.run()
    # main(mysql,'2227358645','57')
    # mysql.close_db()



