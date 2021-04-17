import scrapy
import urllib

# from com.liaoshijie.forstudy.python.spiders.comic.ComicSpider import ComicSpider
#
# spider = ComicSpider
# spider.start_requests(spider)
url = "https://ac.qq.com/riman"
headers = {
    ":authority": "manhua.fzdm.com",
    ":path": "/2/1010/index_1.html",
    ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "ga=GA1.1.1583713336.1618148971; 4352_2568_125.67.188.136=1; 4243_2327_125.67.188.136=1; 4244_2325_125.67.188.136=1; 4243_2326_125.67.188.136=1; 4244_2525_125.67.188.136=1; 4244_2571_125.67.188.136=1; 4244_2570_125.67.188.136=1; 4244_2499_125.67.188.136=1; 4244_2402_125.67.188.136=1; 4240_2507_125.67.188.136=1; 4244_2444_125.67.188.136=1; 4244_2460_125.67.188.136=1; 4240_2463_125.67.188.136=1; beitouviews_4240=YpwbPEcaTRTWD3reFGt5JU3flgBDLhThlEM6w4dGCa5GfDgJEoVKT1mAlB%252BUfjEhUGCfTm7k%252BIxN1zuqMVcs%252FQu4CYqXpIhPPxTH8gnT%252BcyKbT6ZP9jCbKwFVLmM1esol85Y8YXVazlKgNTT1N7KvjZih8QWOz9hXsmh%252B0kDOo4SFVO4sO7LJD1eltBejz9ZsVJFjgg54jo5k7eRgGxP9K3PzRWLg6DEs9cTgD6VGYVIq7XCY%252FCFWkJ4hbJsJP7AeDh80kZr4nuexZziL3ZmmBXpqh%252B6Dc3tJD89rG7CaJ4nztNOmuLo%252FomGmjRcmTwNsqcD9jy2b2zb7%252BmABe3Onw%253D%253D; 4240_2470_125.67.188.136=1; picHost=http%3A//www-mipengine-org.mipcdn.com/i/p3.manhuapan.com; fixedview_4243=saVvQuil%252Bbljb57CHkBMGzj6OSFrhYEO9jtwJLUTUYvCLSNxbQ2vLtwgsMqkWXT86xQBYoNUc3x1rjHrDyFu4p%252FT7DZChSRSEuwC%252Bn6l%252BYgl8wH9RqGyeMkJmX9CIyVunyDOVf66RciaDLWyInfRYLRqREKiU76ZryW8fC2V2EpEzVd5LK5Gn9cG%252FTlZS8LT9RrboYE2sXEQX042qFsk0I32OnEfxEHJjfeTwVHt6ovxUny9IZKm1IKxcxKreQZkq2ioKkP2yzw4WXjs1udsuEu69m%252B8mXJGbldhe749aIz8Z5eGNYcpurrs9mfGlLrLcGyzeqoq5sDrw0JgPYUz9Q%253D%253D; fixedviewTop_4352=KCP56bSuGfyDXwT73%252BEPBgRNcb%252BPMoYMJ%252F1X0nTN6X%252FlmcAH5LCtSvbjV3Pym7pX50jby8FkiLjFZyHvXtIAGs7ImPVQGyVMDNi4YtQVB%252F8%252FYvkhKEwHSxTrnXt4sjTo9nWC8JUafaojofeOGmOVZDJmSwAS%252BSbwNK9pW3gnFodEBwpZ5MZWFCpx0j4qax2UP%252Frl8p94%252F3s%252BCpF%252B9RegfHLuo3gs1qUKOnjEl97i0E5S7xWbmILGoSRvrjwMi%252FCOqvzI9G04G1hGkJgNj9AmnnVHm5eh18xZyjPxOxR7zi0G%252FnPgJp6hkf94NyMuzETPORC5j04T%252F0uzutiuenC6og%253D%253D; richviews_4244=da7SaSX3usLAsr0%252FSrzaQTy%252Fzvm5eXDOww9vDHqu%252BQoEkb8QdLUqMccs68lz0EILQOLnU1mzZTKx1%252B3zZQ6nrt2zJtY6HNkM%252BY5x7Oa9Gi%252FWBtlyHrFt24qW1JztpiIxZ79QxLylNe9NlS%252B9fwibV19h5TxYibzNM9uq4pjbnPjbLBJBpkexWDL6cIOr44nUy%252B8ZY9nhJfNktSKz3CDruRJdsK7l8w2xAmdVuAlDj0SqnhPd5C9OmpHxc6e8Y3vLn9EbWoE8tyG68KIyPcp1PqCCs75lZBtY2j2A02VM2NVPLlGRjTF5tIxLcML%252BG0qu7d%252FkTQLeZmuwf4IL7ddk6Kq8%252BB7fF9XgMMS3GtKAumbSxoW1IDie1bJiU0bt%252BJiTOYzB3%252By7ydt%252FsQrE9bJ%252BvYjwjDUoO5SDh8MZSuWG%252FiTVadku7kj7AgTGeru3In6PgCQltEIlJl2%252BulXq58p%252F%252BN1MG%252Bsj1MS%252Fu7EEXrLt0L6osvZamWb5yWNVcU%252BUM2ljqu3nzOUQuMyEg7MBfG83YhcffUiaAfZKS0JHFOzEH7cbJlB9QmUWGLd9wtrCm5j8ZaslkX2AI2hb91xSeO5KPN5dEa1fD1sadq14%252B2dN0dTwpZJ%252ByeCLoi4m3rXf%252BshSJdof1OjFeWD1RIaPG9hBaN%252FM4Km5ujH%252BjU0DDqRIqK4%253D; _ga_1FZE0C2L80=GS1.1.1618669087.11.1.1618669104.0",
    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
}

print("测试scrapy")
req = scrapy.Request(url=url)
print(req.body)

url_req = urllib.request.Request(url)
response = urllib.request.urlopen(url_req)
data = response.read().decode('utf-8')

print(data)
