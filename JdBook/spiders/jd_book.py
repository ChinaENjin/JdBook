# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['jd.com']
    start_urls = [
        'https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=python&page={}&s=60&click=0'.format(
            str(i)) for i in range(1, 2, 2)]

    def __init__(self):
        self.deiver = webdriver.Chrome()
        self.deiver.set_page_load_timeout(60)

    def close(self, spider):
        time.sleep(5)
        self.deiver.quit()

    def start_requests(self):
        '''
        循环start_urls，封装requests对象，请求下载
        :return:
        '''
        for url in self.start_urls:
            # 此地request数据会发送到selenium, 动态抓取
            request = scrapy.Request(url, meta={'type': 'classify'}, callback=self.parse)
            yield request

    def parse(self, response):
        '''
        selenium返回的reponse结果
        :param response:
        :return:
        '''
        print("########################")
        li_list = response.xpath('//div[@id="J_goodsList"]/ul/li')
        print(f"li_len: {len(li_list)}")
        for li in li_list:
            li_sku = li.xpath('./@data-sku').extract_first()
            detail_url = 'https://item.jd.com/' + li_sku + ".html"
            request = scrapy.Request(detail_url, meta={'type': 'detail'}, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        print("$$$$$$$$$$$$$$$$")
        print(response.url)
        with open("jd_url.txt", "a+", encoding="utf-8") as f:
            f.write(f"{response.url}\n")
