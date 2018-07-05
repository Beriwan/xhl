# -*- coding: utf-8 -*-

# Scrapy settings for xhl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xhl'

SPIDER_MODULES = ['xhl.spiders']
NEWSPIDER_MODULE = 'xhl.spiders'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"


HTTPERROR_ALLOWED_CODES = [404]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xhl (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    # 'Cookie': 'PHPSESSID=k9av555ng9ntqcrdguveq3nm22; Hm_lvt_2772005b8bc0b193d080228322981977=1528770876; Hm_lvt_1c358b33dfa30c89dd3a1927a5921793=1528770876; xhl_cok=d8e0Bl3Mda5qkQtjGYQexSBBP3o5Ewa3OZ%2BKzz5FQG%2FEqWjqYBgWRcoxnPoRt%2B23PhD6nyF6%2BVqkErfZSQ; 6N3e_f2ec___XHLTXZ__www=0f594v2V4vbeCABmpyV%2F1ZUmdYs5EtNt6b35BRSZSYMeO9xIzNViHBl%2FHVuiMI3MWguA8zYu%2FiCKTs%2F4e4W4IfJK2%2BPpU0uLGy378xDb1Q; Hm_lpvt_1c358b33dfa30c89dd3a1927a5921793=1528875351; Hm_lpvt_2772005b8bc0b193d080228322981977=1528875351'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xhl.middlewares.XhlSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'xhl.middlewares.XhlDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'xhl.pipelines.XhlPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# REDIS_HOST = '192.168.0.107'
REDIS_HOST = '10.10.0.109'     # 主机名
REDIS_PORT = 6379
REDIS_PASSWORD = None