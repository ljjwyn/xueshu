# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy_splash import SplashRequest

from xueshu.items import XueshuItem


class ScrapyxueshuSpider(CrawlSpider):

    def __init__(self, *args, **kwargs):
        super(ScrapyxueshuSpider, self).__init__(*args, **kwargs)  # 这里是关键
        self.url_set = list()

    name = 'XueShu'
    allowed_domains = ['xueshu.baidu.com']
    start_urls = ['http://xueshu.baidu.com/s?wd=机器学习',
                  'http://xueshu.baidu.com/s?wd=卷积神经网络',
                  'http://xueshu.baidu.com/s?wd=循环神经网络',
                  'http://xueshu.baidu.com/s?wd=反向传播',
                  'http://xueshu.baidu.com/s?wd=感知机'
                  'http://xueshu.baidu.com/s?wd=长短期记忆',
                  'http://xueshu.baidu.com/s?wd=深度置信网络',
                  'http://xueshu.baidu.com/s?wd=自然语言处理',
                  'http://xueshu.baidu.com/s?wd=目标监测',
                  'http://xueshu.baidu.com/s?wd=图像识别'
                  'http://xueshu.baidu.com/s?wd=机器翻译',
                  'http://xueshu.baidu.com/s?wd=关系抽取',
                  'http://xueshu.baidu.com/s?wd=命名实体识别',
                  'http://xueshu.baidu.com/s?wd=知识图谱',
                  'http://xueshu.baidu.com/s?wd=支持向量机'
                  'http://xueshu.baidu.com/s?wd=逻辑回归',
                  'http://xueshu.baidu.com/s?wd=决策树',
                  'http://xueshu.baidu.com/s?wd=随机森林',
                  'http://xueshu.baidu.com/s?wd=监督学习',
                  'http://xueshu.baidu.com/s?wd=强化学习',
                  'http://xueshu.baidu.com/s?wd=无监督学习'
                  ]
    rules = {
        Rule(LinkExtractor(restrict_css='.n', tags='a', attrs='href'), follow=True, callback="parse_item")
        # Rule(LinkExtractor(restrict_css='.leftnav_list_cont', tags='a', attrs='href'), follow=True, callback="parse_item")
    }

    def parse_item(self, response):
        paperId = response.css('.sc_content h3 a::attr(href)').re(r'paperuri%3A%28(.*)%29&')
        for paper_url in paperId:
            url = "http://xueshu.baidu.com/usercenter/paper/show?paperid=" + paper_url
            # yield scrapy.Request(url=url, callback=self.parse2)
            # print(url)
            self.url_set.append(url)
            yield SplashRequest(url=url, callback=self.get_url,
                                args={'wait': 1, 'url': url, 'lua_source': ''})
        urlList=self.url_set.copy()
        print("___________count",len(urlList))
        for urls in urlList:
            if urls in self.url_set:
                self.url_set.remove(urls)
            yield scrapy.Request(url=urls, callback=self.parse2)

    def parse2(self, response):
        print('==========================动态解析url=========================')
        item = XueshuItem()
        item['title'] = response.css('.main-info h3 a::text').extract_first()
        item['author'] = response.css('.author_text span a::text').extract()
        item['abstract'] = response.css('.abstract::text').extract_first()
        item['keyWords'] = response.css('.kw_main span a::text').extract()
        item['DOI'] = response.css('.doi_wr .kw_main::text').extract_first()
        item['cited'] = response.css('.sc_cite_cont::text').extract_first()
        yield item

    def get_url(self,response):
        value = response.xpath('//div[@class="con_related"]//li//p[@class="rel_title"]//a//@href').re('.*')
        for paper_url in list(value):
            url = "http://xueshu.baidu.com" + paper_url
            self.url_set.append(url)
            # yield scrapy.Request(url=url, callback=self.parse2)
