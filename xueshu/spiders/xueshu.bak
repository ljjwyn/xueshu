#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashTextResponse, SplashJsonResponse, SplashResponse
from scrapy.http import HtmlResponse
from xueshu.items import XueshuItem


class MySpider(CrawlSpider):
    name = 'baiduxueshu'
    url = ['http://xueshu.baidu.com/usercenter/paper/show?paperid=5b9f2c599a5a150fbf8e94a72e18edae']

    def start_requests(self):
        for url in self.url:
            # Splash 默认是render.html,返回javascript呈现页面的HTML。
            yield SplashRequest(url, args={'wait': 10})

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="con_related"]//li//p[@class="rel_title"]',tags='a',attrs='href'), process_request='splash_request', follow=True),
    )

    # 这个方法是给Rule 中的process_request用的。
    def splash_request(self, request):
        """
          process_request is a callable, or a string (in which case a method from the spider object with that name will
        be used) which will be called with every request extracted by this rule,
        and must return a request or None (to filter out the request).
        :param request:
        :return: SplashRequest
        """
        return SplashRequest(url=request.url, args={'wait': 1})

    # 重写CrawlSpider 的方法
    def _requests_to_follow(self, response):
        """
        splash 返回的类型 有这几种SplashTextResponse, SplashJsonResponse, SplashResponse以及scrapy的默认返回类型HtmlResponse
        所以我们这里只需要检测这几种类型即可，相当于扩充了源码的检测类型
        :param response:
        :return:
        """
        # print(type(response)) # <class 'scrapy_splash.response.SplashTextResponse'>
        if not isinstance(response, (SplashTextResponse, SplashJsonResponse, SplashResponse, HtmlResponse)):
            return
        print('==========================动态解析url=========================')
        item = XueshuItem()
        item['title'] = response.css('.main-info h3 a::text').extract_first()
        item['author'] = response.css('.author_text span a::text').extract()
        item['abstract'] = response.css('.abstract::text').extract_first()
        item['keyWords'] = response.css('.kw_main span a::text').extract()
        item['DOI'] = response.css('.doi_wr .kw_main::text').extract_first()
        item['cited'] = response.css('.sc_cite_cont::text').extract_first()
        yield item

        seen = set()

        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def _build_request(self, rule, link):
        # 重要！！！！！这里重写父类方法，特别注意，需要传递meta={'rule': rule, 'link_text': link.text}
        # 详细可以查看 CrawlSpider 的源码
        r = SplashRequest(url=link.url, callback=self._response_downloaded, meta={'rule': rule, 'link_text': link.text},
                          args={'wait': 5, 'url': link.url, 'lua_source': ''})
        r.meta.update(rule=rule, link_text=link.text)
        return r


