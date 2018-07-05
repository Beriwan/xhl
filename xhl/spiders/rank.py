# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime

import requests
import scrapy
from bs4 import BeautifulSoup

from xhl.db import Mysql
import sys
sys.setrecursionlimit(1000000)

class RankSpider(scrapy.Spider):
    name = 'xhl_rank'
    allowed_domains = ['www.xiaohulu.com']
    start_urls = ['http://www.xiaohulu.com/']
    mysql = Mysql()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        cookie = 'PHPSESSID=k9av555ng9ntqcrdguveq3nm22; Hm_lvt_2772005b8bc0b193d080228322981977=1528770876; Hm_lvt_1c358b33dfa30c89dd3a1927a5921793=1528770876; xhl_cok=d8e0Bl3Mda5qkQtjGYQexSBBP3o5Ewa3OZ%2BKzz5FQG%2FEqWjqYBgWRcoxnPoRt%2B23PhD6nyF6%2BVqkErfZSQ; 6N3e_f2ec___XHLTXZ__www=0f594v2V4vbeCABmpyV%2F1ZUmdYs5EtNt6b35BRSZSYMeO9xIzNViHBl%2FHVuiMI3MWguA8zYu%2FiCKTs%2F4e4W4IfJK2%2BPpU0uLGy378xDb1Q; Hm_lpvt_1c358b33dfa30c89dd3a1927a5921793=1528875351; Hm_lpvt_2772005b8bc0b193d080228322981977=1528875351'

        itemDict = {}
        items = cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

    def start_requests(self):
        url = 'http://www.xiaohulu.com/Anchor/index.html?plat=1&class=all&day=1440m'
        url_set = 'http://www.xiaohulu.com/Anchor/index.html?plat={id}&class=all&day='
        url_rich = 'http://www.xiaohulu.com/Spectator/index.html?plat={id}&day='
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        platforms = soup.select('.container ul.panktip select')[1]
        for platform in platforms.select('option')[1:]:
            platformname = platform.string.strip()
            plat = re.search('plat=(\d+)&', platform['value']).group(1)
            url_plat = url_set.format(id=plat)
            url_richplat = url_rich.format(id=re.search('plat=(\d+)&', platform['value']).group(1))
            response1 = requests.get(url_plat, headers=self.headers)
            soup = BeautifulSoup(response1.text, 'lxml')
            dates = soup.select('.container ul.panktip select')[0]
            datelist = [dates.select('option')[1], dates.select('option')[9], dates.select('option')[15]]
            for date in datelist:
            # for date in dates.select('option'):
                url_time = url_plat + date['value']
                url_rich1 = url_richplat + date['value']
                yield scrapy.Request(url=url_time, meta={'date': date.string, 'plat': plat}, callback=self.parse)
                yield scrapy.Request(url=url_rich1, meta={'date': date.string, 'plat': plat, 'name': platformname},
                                     callback=self.rich, headers=self.headers, cookies=self.stringToDict())
                # main(url_time, data.string, mysql, plat)
                # rich(url_rich1, data.string, platformname, mysql, plat)

    def parse(self, response):
        try:
            list_rank = []
            soup = BeautifulSoup(response.text, 'lxml')
            titalranks = soup.find_all(attrs={'class': 'w560'})
            for item in titalranks:
                print(item.find(attrs={'class': 'h_list'}).string)
                # print(item.select('.stitle ul li'))
                for i in range(0, len(item.select('.stitle ul li')))[1:]:
                    rankname = item.select('.stitle ul li')[i].string
                    ranks = item.select('.mt20.lmmain div.svtable')[i]
                    ids = ranks.select('a')
                    contents = ranks.select('tr')
                    for n in range(0, len(ids)):
                        roomid = re.search('roomid=(.*?)&', str(ids[n])).group(1)
                        content = contents[n]
                        messages = {
                            'roomid': roomid,
                            'plat': response.meta['plat'],
                            'ranktype': rankname,
                            'ranknum': content.select('span.num')[0].string,
                            'anchor': re.search('</i>(.*)</h4>', str(content.select('dd h4')[0]), re.S).group(1),
                            'platform': content.select('dd h4 i')[0].string,
                            'type': re.match('(.*?)\s', content.select('dd p')[0].get_text()).group(1),
                            'img': content.select('dt img')[0]['src'],
                            'rankdetail': content.select('td.hsnum')[0].string.strip(),
                            'ranktime': response.meta['date'],
                            'Crawltime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        }
                        list_set = (
                        roomid, messages['plat'], messages['ranktype'], messages['ranknum'], messages['anchor'],
                        messages['platform'], messages['type'], messages['img'], messages['rankdetail'],
                        messages['ranktime'], messages['Crawltime'])
                        list_rank.append(list_set)
                    sql = "replace into rank_history(roomid,plat,ranktype,ranknum,anchor,platform,type,img,rankdetail,ranktime,Crawltime)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    print(sql)
                    self.mysql.insert_sql_many(sql,list_rank)
        except Exception as e:
            with open('error.txt', 'a+') as f:
                try:
                    f.write(response.url + '\n')
                    f.write('error: %s \n' % e)
                except Exception:
                    f.write(response.url + '\n')

    def rich_id(self,list):
        sql = "replace into rich_id(roomid,plat,name)values(%s,%s,%s)"
        # # print(sql)
        self.mysql.insert_sql_many(sql,list)

    def rich(self, response):
        try:
            list_rank = []
            list_price = []
            soup = BeautifulSoup(response.text, 'lxml')
            titalranks = soup.find_all(attrs={'class': 'w560'})
            for item in titalranks:
                rankname = item.select('.stitle h3')[0].string

                ranks = item.select('.mt20 div.svtable')[0]
                contents = ranks.select('tr')
                ids = ranks.select('a')
                for n in range(0, len(ids)):
                    roomid = re.search('fromid=(.*?)\"', str(ids[n])).group(1)
                    content = contents[n]
                    try:
                        anchor = content.select('dd h4')[0].string.replace('\'', '\\\'')
                    except Exception:
                        anchor = content.select('dd h4')[0].string
                    messages = {
                        'roomid': roomid,
                        'plat': response.meta['plat'],
                        'ranktype': rankname,
                        'ranknum': content.select('span.num')[0].string,
                        'anchor': anchor,
                        'platform': response.meta['name'],
                        'img': content.select('dt img')[0]['src'],
                        'rankdetail': content.select('td .hsnum')[0].string.strip(),
                        'ranktime': response.meta['date'],
                        'Crawltime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    if rankname == '土豪榜':
                        rich_set = (messages['roomid'], messages['plat'], messages['anchor'])
                        list_price.append(rich_set)
                    list_set = (
                        roomid, messages['plat'], messages['ranktype'], messages['ranknum'], messages['anchor'],
                        messages['platform'], messages['img'], messages['rankdetail'],
                        messages['ranktime'], messages['Crawltime'])
                    list_rank.append(list_set)
                sql = "replace into rank_history(roomid,plat,ranktype,ranknum,anchor,platform,img,rankdetail,ranktime,Crawltime)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                self.rich_id(list_price)
                self.mysql.insert_sql_many(sql, list_rank)

        except Exception as e:
            with open('error.txt', 'a+') as f:
                try:
                    f.write(response.url + '\n')
                    f.write('error: %s \n' % e)
                except Exception:
                    f.write(response.url + '\n')
