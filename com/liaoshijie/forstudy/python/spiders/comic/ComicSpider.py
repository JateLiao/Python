#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging

import scrapy
from bs4 import BeautifulSoup

# 漫画url
comic_url = "https://manhua.fzdm.com"
# 要爬的漫画名：死神、火影忍者、海贼王
comic_name = "海贼王"
# 漫画区间
index_start = 655
index_end = 1010
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
              + "\n漫画区间：" + str(index_start) + " -> " + str(index_end)
              + "\n保存路径：" + save_path)
        # start_urls = [comic_url]
        # for url in start_urls:
        yield scrapy.Request(url=comic_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print("解析函数被回调: " + response.url)
        content = response.body
        if not content:
            print("回调response异常")
            return

        # 用BeautifulSoup库进行节点的解析
        soup = BeautifulSoup(content, "html5lib")
        main_div = soup.find(name="div", attrs={"id": "mhmain"})
        ul_tag = main_div.find(name="ul")
        # 找到当前所有漫画
        all_comics_tag = ul_tag.find_all(name="div", attrs={"class": "round"})
        # 找到目标漫画序号
        target_index = 0
        is_find = False
        for comic_tag in all_comics_tag:
            target_index = target_index + 1
            current_a_tag = comic_tag.find(name="li").find(name="a")
            current_attrs = current_a_tag.attrs
            current_comic_name = current_attrs["title"]
            if comic_name in current_comic_name:
                is_find = True
                print("小样儿，终于找到你了吧：" + current_comic_name)
                break
        if not is_find:
            print("你瞅瞅你漫画名写的啥，啥也没找到...")
            print("\n\n\n\n爬完了，没有了，没有爬虫了\n\n\n")
            return
        target_url = "".join([comic_url, "/", str(target_index)])
        print("目标url：" + target_url)
        print("开始解析目标漫画url：" + target_url)
        yield scrapy.Request(url=target_url, callback=parse_target_url, dont_filter=True)


def parse_target_url(response):
    current_url = response.url
    print("解析当前漫画：" + current_url)
    content = response.body
    soup = BeautifulSoup(content, "html5lib")
    all_index_url_div = soup.find_all(name="li", attrs={"class": "pure-u-1-2 pure-u-lg-1-4"})
    for index_div in all_index_url_div:
        index_title = index_div.find(name="a").attrs["title"]
        index_href = index_div.find(name="a").attrs["href"]  # .replace("/", "")
        digital_ = "".join(list(filter(str.isdigit, index_href)))
        if "" == digital_:
            print("暂时不处理这种: {}---{}".format(index_href, index_title))
            continue
        index_no = int(digital_)
        if index_start <= index_no <= index_end:
            print("发现目标：{}---{},真实剧集：{}".format(index_href, index_title, index_no))
            target_index_url = "".join([current_url, index_href.replace("/", "")])
            print("开始解析目标剧集url：" + target_index_url)
            yield scrapy.Request(url=target_index_url, callback=page_target_index_url, dont_filter=True)


def page_target_index_url(response):
    return
