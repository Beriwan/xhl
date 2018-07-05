# coding=UTF-8
import os
import time
os.system('python index.py')
os.system('/usr/local/anaconda3/bin/scrapy crawl xhl_rank')
print('暂停60')
time.sleep(10)
os.system("/usr/local/anaconda3/bin/scrapy crawl xhl_detail")
os.system('python detail2.py')
print('暂停120')
time.sleep(10)
os.system("/usr/local/anaconda3/bin/scrapy crawl xhl_user")
print('暂停一天')