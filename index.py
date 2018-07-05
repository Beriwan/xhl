# coding=UTF-8
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from xhl.db import Mysql


def get_url(mysql):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    url = 'http://www.xiaohulu.com/rank/?plat=1'
    url_set = 'http://www.xiaohulu.com'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    platfroms = soup.select('div.plat-zoom ul a')
    for platfrom in platfroms:
        url1 = url_set + platfrom['href']
        plat = re.search('\?plat=(\d+)',platfrom['href']).group(1)
        platfromname = platfrom.select('li')[0].string
        try:
            parse(url1, platfromname, plat, mysql)
        except Exception as e:
            with open('index.txt', 'a+') as f:
                f.write(url1 + '\n')
                f.write('error: %s \n' % e)


def text(mysql):
    url = 'https://www.xiaohulu.com/rank/?plat=29'
    parse(url, '一直播', 29, mysql)

def parse(url, platformname, plat, mysql):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    contents = soup.select('.container .pt_data ul li')
    for content in contents:
        messages = {
            'type' : content.select('dt')[0].string,
            'today' : content.select('dd')[1].string,
            'yesterday' : content.select(('dd'))[3].string,
            'platform': platformname,
            'time': datetime.now().strftime('%Y-%m-%d'),
        }
        sql = 'replace into ' + mysql.get_sql_sentence('home_list', messages)
        print(sql)
        mysql.insert_one(sql)

    ranks = soup.select('.anchor_data_list div.col-anchor-nav')
    rank = ranks[4].select('div.total div.row ul')

    num = 1
    rankname = '粉丝榜'
    for item in rank[0].select('a'):
        roomid = re.search('roomid=(.*?)\"', str(item)).group(1)
        try:
            anchor = item.select('dd')[1].string.replace('\'','\\\'' )
        except Exception:
            anchor = item.select('dd')[1].string
        messages1 = {
            'roomid': roomid,
            'plat':plat,
            'ranktype': rankname,
            'ranknum': num,
            'anchor': anchor,
            'platform': platformname,
            'img': item.select('dt img')[1]['src'],
            'rankdetail': item.select('dd')[0].string,
            'type': item.select('dd')[2].string,
            'ranktime': datetime.now().strftime('%m-%d'),
            'Crawltime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        sql = 'replace into ' + mysql.get_sql_sentence('rank_history', messages1)
        print(sql)

        mysql.insert_one(sql)
        num = num + 1
    if rank[1].select('a'):
        print('==================')
        for item in rank[1].select('a'):
            roomid = re.search('roomid=(.*?)\"', str(item)).group(1)
            try:
                anchor = item.select('dd div')[0].string.replace('\'','\\\'' )
            except Exception:
                anchor = item.select('dd div')[0].string
            messages2 = {
                'roomid': roomid,
                'plat':plat,
                'ranktype': rankname,
                'ranknum': item.select('dd')[0].string,
                'anchor': anchor,
                'platform': platformname,
                # 'img': item.select('dt img')[0]['src'],
                'rankdetail': item.select('dd')[2].string,
                'type': item.select('dd div')[1].string,
                'ranktime': datetime.now().strftime('%m-%d'),
                'Crawltime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            sql = 'replace into ' + mysql.get_sql_sentence('rank_history', messages2)
            print(sql)
            mysql.insert_one(sql)
    else:
        parse(url, platformname, plat, mysql)



if __name__ == '__main__':
    mysql = Mysql()
    # text(mysql)
    get_url(mysql)
    # mysql.close_db()