# -*- coding: utf-8 -*-

# Scrapy settings for lianjia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lianjia'

SPIDER_MODULES = ['lianjia.spiders']
NEWSPIDER_MODULE = 'lianjia.spiders'

# 请求获取cookie的url
COOKIE_URL = "http://112.74.58.112:8051/lianjia"
# 请求获取proxy的url
PROXY_URL = "http://112.74.58.112:8052/proxy"
# 渲染js splashurl
SPLASH_URL = "http://112.74.58.112:8049/"
# mongodb配置
MONGO_URI = "112.74.58.112"
#MONGO_URI = "localhost"
MONGO_DB = "lianjia"
#selenium middleware use it 
SELENIUM_TIMEOUT = 20

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
    "lianjia.middlewares.CookiesMiddleware": 820,
    "lianjia.middlewares.ProxyMiddleware": 830,
    "lianjia.middlewares.UserAgentMiddleware": 840,
    #"lianjia.middlewares.SeleniumMiddleware": 547,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'lianjia.pipelines.LianjiaPipeline': 300,
    'lianjia.pipelines.MongoPipeline': 400,
}

SPIDER_MIDDLEWARES = {
    "scrapy_splash.SplashDeduplicateArgsMiddleware": 100    
}

# 爬完后情况去重set和request list
#SCHEDULER_PERSIST = True

# 使用scrapy_redis调度器类
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 使用scrapy_redis去重类
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用scrapy_redis队列的先进先出队列
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.FifoQueue"
# redis配置
REDIS_HOST = "112.74.58.112"
REDIS_PORT = "6379"
REDIS_PASSWORD = None

# 配置splash的cache
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"

