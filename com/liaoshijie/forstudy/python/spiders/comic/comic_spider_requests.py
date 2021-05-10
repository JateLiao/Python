#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import os
import re
import urllib

import requests
import scrapy
from bs4 import BeautifulSoup

# 漫画url
comic_url = "https://manhua.fzdm.com"
pic_url_pattern = "http://www-mipengine-org.mipcdn.com/i/p3.manhuapan.com/{}"
# 要爬的漫画名：死神、火影忍者、海贼王
comic_name = "海贼王"
# 漫画区间
index_start = 1011
index_end = 1012
# 漫画存放路径
save_path = "/Users/liaoshijie/Books/Comics/"

logger = logging.getLogger("comic_spider_logger")
logger.setLevel(logging.INFO)
headers = {
    ":authority": "manhua.fzdm.com",
    ":path": "/2/1010/index_1.html",
    ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "_ga=GA1.1.1583713336.1618148971; 4352_2568_125.67.188.136=1; 4243_2327_125.67.188.136=1; 4244_2325_125.67.188.136=1; 4243_2326_125.67.188.136=1; 4244_2525_125.67.188.136=1; 4244_2571_125.67.188.136=1; 4244_2570_125.67.188.136=1; 4244_2499_125.67.188.136=1; 4244_2402_125.67.188.136=1; 4240_2507_125.67.188.136=1; 4244_2444_125.67.188.136=1; 4244_2460_125.67.188.136=1; 4240_2463_125.67.188.136=1; beitouviews_4240=YpwbPEcaTRTWD3reFGt5JU3flgBDLhThlEM6w4dGCa5GfDgJEoVKT1mAlB%252BUfjEhUGCfTm7k%252BIxN1zuqMVcs%252FQu4CYqXpIhPPxTH8gnT%252BcyKbT6ZP9jCbKwFVLmM1esol85Y8YXVazlKgNTT1N7KvjZih8QWOz9hXsmh%252B0kDOo4SFVO4sO7LJD1eltBejz9ZsVJFjgg54jo5k7eRgGxP9K3PzRWLg6DEs9cTgD6VGYVIq7XCY%252FCFWkJ4hbJsJP7AeDh80kZr4nuexZziL3ZmmBXpqh%252B6Dc3tJD89rG7CaJ4nztNOmuLo%252FomGmjRcmTwNsqcD9jy2b2zb7%252BmABe3Onw%253D%253D; 4240_2470_125.67.188.136=1; picHost=http://www-mipengine-org.mipcdn.com/i/p3.manhuapan.com;fixedviewTop_4352=XK4RzfL66xxKNbpYmZw7vDfgookBjv98qpxdSPzpvRdRm0eDtviNB%252F84ZlBdyzo78RzSYGTeVqeIFux93P8iz1Ts4RgcTocW%252Fkn0a7GUJoQj%252Bn5OHa%252FV75VxFEunKLsFQYVd3C5yLxK0fGWad3JK56sVUtLkLMIUDdC2lUMfSBkFJXJKu8OwmKXX6FJ%252FBB8Opl7PggJ6w7KceSvsj6IsP7L3Jqricf7AM2Caku5YFnLtHzCX1Lf1eOGCtIIphgP4uiSsf2%252FC1Wyx499lBM8Qq8oLnjTlse6xH7PgzIG4I5Gy3kd4BPRCkyy7p%252B0eTfKdFMC94U2PubMC7ZsI1CrBGg%253D%253D; fixedview_4243=fpMrbJ2jKxc%252FeIt1wbLBxY2wg1AuzKebUstRtLgNahSc98riQK2rcTFTaN57yXQR4akAczcCkp%252FhRMSUap4NuK9G7fyHBm64V9LNtR3djYm42jeEJOhn2WZD75pBGQ4qOhXihmApK%252F3tSbZDVpoxnfySQsdtyI9j8JlX3LPyPmyKJ2BvpdzSRIX9zaV9ltMRLrUOeWfNOBE77ibCpH4QTUEYWBh0VV9%252BcbyH07w4s87D%252Bds%252BgZ1eM1seazB6as1a7L4%252BTsLzSdnkZt52JywGjXUBbfem2FWfs%252BxaL9jmOthMbjzpM3Z4GJL%252BfKP5bGoVlfMYFMU6JUMlDBNt5FVPJQ%253D%253D; richviews_4244=dJQb0gcRm0De9PbjE4SsAB%252FCrbOAJawEYSJu7UlkTarPEsUccnuIu35R%252Btwy8ioD24r%252FJP79rPgvL3Cime%252BWmgOC2CaexA8OxCcUuDzF85ONQl6dIuKf3mCuRmL2k5Em2sGxqNM%252BYOnKZuP5Ryv7qxt%252B%252BJqdx81EOPg0tZUT33dFR49k7x%252FAcrumH8vzov0ldW61LnYBP3OgA2zvhRHijHthsOYW4RPAEc%252Bat7iWWarKmDNgq%252F0U8Io1FXmIpgYJap3pQGYG07d%252Fg8feJYoq7qPXyU92Hl0wYEpPt7cDSLl3M%252FxCUNUrP8%252F%252F6jp61juSFCj9%252FMViLks5Hc8wRG7gAXMCumUgBsaGz5LvgTkb7DPdHbtbj8s6fPIoXh0j62xJ%252BZb9KAsWvD4t%252FkDLdnlxYMlJ4R08V6TyP4xOqPBfsuO0ZqbLiEsfLZSy8K4upTTZhDdCpoUCTZ23erMyL8CcSTuYkPOlHFMSQliu8Pdx7yb2J8WKqgcC9appcXVrCcIHPod%252BWBtv1Jl%252FYOfy0lUI1EzNw%252BUYZ15N9xHBvm6Gu4LfZDItLcQBJSy5hvKpkMUMjiyq9lOx8qcRb90cwu6CIW8oEYxLCqzZCKVSgRBaHocKvMVj9t1pXCUSHyhcQ6UnZi7ROrJUF0xECoWWu0zXLaYkiZTsL8X0x6%252BFcPYpy6U%253D; _ga_1FZE0C2L80=GS1.1.1618669087.11.1.1618671365.0",
    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
}


class ComicSpider(scrapy.Spider):
    name = "my_spider"
    allowed_domains = ["manhua.fzdm.com"]

    def start_requests(self):
        # logger.warning("开始爬取漫画...")
        # logger.warning("漫画地址：%s", comic_url)
        print("漫画url：" + comic_url
              + "\n漫画名：" + comic_name
              + "\n漫画区间：" + str(index_start) + " -> " + str(index_end)
              + "\n保存路径：" + save_path)
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
            yield scrapy.Request(url=target_index_url, callback=parse_page_target_index_url, dont_filter=True)


def parse_page_target_index_url(response):
    # 获取当前集，并创建文件夹
    main_url = response.url
    soup = BeautifulSoup(response.body, "html5lib")
    index_name = soup.find(name="div", attrs={"id": "pjax-container"}).find(name="h1").text
    index_name = str.strip(index_name)
    # 创建文件夹
    parent_path = save_path + comic_name + "/" + index_name
    if not os.path.exists(parent_path):
        print("漫画路径创建：" + parent_path)
        os.makedirs(parent_path)
    ## 实际是从https://xxxxx.com/2/456/index_0.html开始解析
    for index_no in range(50):
        index_no_url = main_url + "index_{}.html".format(str(index_no))
        # 判断是否404
        if not is_valid_url(index_no_url):
            print("到此为止了：{}".format(index_no_url))
            break
        print("开始解析图片url：" + index_no_url)
        yield scrapy.Request(url=index_no_url, callback=parse_index_no_url, headers=headers,
                             cb_kwargs={"parent_path": parent_path,
                                        "index_no": index_no})


def parse_index_no_url(response, parent_path, index_no):
    if response.status != 200:
        print("爬完了...{}\n".format(str(index_no)))
        return
    print(parent_path + "/" + str(index_no))
    soup = BeautifulSoup(response.body, "html5lib")
    script_list_tag = soup.find_all(name="script", attrs={"type": "text/javascript"})
    for script_tag in script_list_tag:
        script_text = script_tag.text
        if "var mhurl" in script_text and "var mhurl1" not in script_text:
            match = re.search("mhurl.+jpg", script_text)
            if match:
                pic_url = pic_url_pattern.format(match.group().replace("mhurl=\"", ""))
                print("找到图片：{}".format(pic_url))
                # 下载保存图片到本地
                file_name = parent_path + "/" + str(index_no) + ".jpg"
                urllib.request.urlretrieve(pic_url, filename=file_name)
            break
    return


def is_valid_url(url):
    re_status = requests.head(url).status_code
    return re_status == 200
