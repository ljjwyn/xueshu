import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy_splash.request import SplashRequest, SplashFormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider,Rule


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ['xueshu.baidu.com']
    start_urls = ['http://xueshu.baidu.com/usercenter/paper/show?paperid=93f237b1172b174c55f3bdfd91d2f2d2']
    restrict_css = '.title'
    '''rules = {
        Rule(LinkExtractor(restrict_css=restrict_css, tags='a', attrs='href'), follow=True, callback="parse_item")
    }'''

    def parse(self, response):
        title = response.css('.main-info h3 a::text').extract_first()
        print(title)

    '''def start_requests(self):
        splash_args = {"lua_source": """
                    --splash.response_body_enabled = true
                    splash.private_mode_enabled = false
                    splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                    assert(splash:go("http://xueshu.baidu.com/usercenter/paper/show?paperid=93f237b1172b174c55f3bdfd91d2f2d2"))
                    splash:wait(2)
                    return {html = splash:html()}
                    """}
        yield SplashRequest("http://xueshu.baidu.com/usercenter/paper/show?paperid=93f237b1172b174c55f3bdfd91d2f2d2", endpoint='run', args=splash_args, callback=self.onSave)

    def onSave(self, response):
        #value = response.css('.rel_title a::attr(href)').extract_first()
        value = response.xpath('//div[@class="con_related"]//li//p[@class="rel_title"]//a//@href').extract_first()
        print(value)'''