# -*- coding: utf-8 -*-

# Scrapy settings for qfang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

ROBOTSTXT_OBEY = False
BOT_NAME = 'qfang'

SPIDER_MODULES = ['qfang.spiders']
NEWSPIDER_MODULE = 'qfang.spiders'
# 请求获取cookie的url
COOKIE_URL = "http://47.106.235.179:8051/qfang"
# 请求获取proxy的url
PROXY_URL = "http://47.106.235.179:8050/proxy"
# mongodb配置
MONGO_URI = "47.106.235.179"
#MONGO_URI = "localhost"
MONGO_DB = "qfang"

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "qfang.middlewares.CookiesMiddleware": 544,
    "qfang.middlewares.ProxyMiddleware": 545,
    "qfang.middlewares.UserAgentMiddleware": 546,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'qfang.pipelines.QfangPipeline': 300,
    'qfang.pipelines.MongoPipeline': 400,
}

# 使用scrapy_redis调度器类
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 使用scrapy_redis的去重类
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用scrapy_redis队列的先进先出队列
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.FifoQueue"
# redis配置
REDIS_HOST = "47.106.235.179"
REDIS_PORT = "6379"
REDIS_PASSWORD = None

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qfang (+http://www.yourdomain.com)'

# Obey robots.txt rules

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'qfang.middlewares.QfangSpiderMiddleware': 543,
#}


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


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
