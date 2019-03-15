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
COOKIE_URL = "http://47.106.235.179:8051/lianjia"
# 请求获取proxy的url
PROXY_URL = "http://47.106.235.179:8050/proxy"
# mongodb配置
MONGO_URI = "47.106.235.179"
#MONGO_URI = "localhost"
MONGO_DB = "lianjia"

#selenium middleware use it 
SELENIUM_TIMEOUT = 20
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "lianjia.middlewares.CookiesMiddleware": 544,
    "lianjia.middlewares.ProxyMiddleware": 545,
    "lianjia.middlewares.UserAgentMiddleware": 546,
    "lianjia.middlewares.SeleniumMiddleware": 547,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'lianjia.pipelines.LianjiaPipeline': 300,
    'lianjia.pipelines.MongoPipeline': 400,
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

