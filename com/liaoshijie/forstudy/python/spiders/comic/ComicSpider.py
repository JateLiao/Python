#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging

import scrapy

# 漫画url
comic_url = "https://manhua.fzdm.com"
# 要爬的漫画名：死神、火影忍者、海贼王
comic_name = "海贼王"
# 漫画区间
index_start = "655"
index_end = "1010"
# 漫画存放路径
save_path = "/Users/liaoshijie/Books/Comics/OnePiece"

logger = logging.getLogger("comic_spider_logger")
logger.setLevel(logging.INFO)


class ComicSpider(scrapy.Spider):
    name = "my_spider"
    allowed_domains = ["manhua.fzdm.com"]

    # custom_settings = {
    #     'LOG_LEVEL': 'INFO',
    #     'LOG_FILE': '/Users/liaoshijie/Workspace/python/ForStudy-Python/log/log.log'
    # }

    def start_requests(self):
        # logger.warning("开始爬取漫画...")
        # logger.warning("漫画地址：%s", comic_url)
        print("漫画url：" + comic_url
              + "\n漫画名：" + comic_name
              + "\n漫画区间：" + index_start + " -> " + index_end
              + "\n保存路径：" + save_path)
        # start_urls = [comic_url]
        # for url in start_urls:
        yield scrapy.Request(url=comic_url, callback=self.parse, dont_filter=True, errback=self.parse)

    def parse(self, response):
        print("解析函数被回调: " + response.url)
        content = response.body
        if not content:
            print("回调response异常")
            return

        # 用BeautifulSoup库进行节点的解析
        soup = BeautifulSoup(content, "html5lib")