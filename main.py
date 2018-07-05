# coding=UTF-8
import os
import time
os.system('python index.py')
os.system('scrapy crawl xhl_rank')
print('暂停60')
time.sleep(10)
os.system("scrapy crawl xhl_detail")
os.system('python detail2.py')
print('暂停120')
time.sleep(10)
os.system("scrapy crawl xhl_user")
print('暂停一天')
