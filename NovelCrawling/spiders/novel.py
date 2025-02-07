import scrapy
from lxml import etree

base_url = 'https://m.gulongbbs.com/'
init_url = base_url + 'zhentan/lmgs/'


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['m.gulongbbs.com']
    start_urls = [init_url]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'DEFAULT_REQUEST_HEADERS': {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "cookie": "Hm_lvt_d22910fef702a5c34dd8afa8d549db45=1738899424; HMACCOUNT=37D6BD70DAEB7D43; Hm_lpvt_d22910fef702a5c34dd8afa8d549db45=1738901108",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://m.gulongbbs.com/zhentan/lmgs/qygt/",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
    }

    def parse(self, response, **kwargs):
        tree = etree.HTML(response.text)
        for novel_name in ['七夜怪谈', '复活之路', '永生不死', '贞相大白']:
            element = tree.xpath(f"//a[text()='{novel_name}']")[0]
            novel_url = init_url + element.get('href')
            yield scrapy.Request(novel_url, callback=self.parse_chapter,
                                 meta={'novel': novel_name})

    def parse_chapter(self, response):
        novel_name = response.meta.get('novel')
        tree = etree.HTML(response.text)
        a_list = tree.xpath('//table/tr/td/a')
        for a in a_list:
            content_url = base_url + a.get('href')
            print(f'content_url={content_url}')
            yield scrapy.Request(content_url, callback=self.parse_chapter_content,
                                 meta={'title': novel_name + '#' + a.get('title')})

    def parse_chapter_content(self, response):
        title = response.meta.get('title')
        tree = etree.HTML(response.text)
        content = ''.join(tree.xpath("//div[@id='div_content' and @class='articleContent']/span//text()")).strip()
        yield {
            'title': title,
            'content': content
        }
