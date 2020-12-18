# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from ..items import XueshuItem

class tencentNextPageSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0']
    # base_url='https://hr.tencent.com/position.php?&start=%s'
    # for i in range(0,391):
    #     # url=base_url%(i*10)
    #     start_urls.append(url)

    def parse(self, response):
        job_even=response.xpath('//tr[@class="even"]')
        job_odd=response.xpath('//tr[@class="odd"]')
        #合并数组
        jobs=job_even+job_odd

        for job in jobs:
            print(job)
            item=TencentItem()
            #时间
            date=job.xpath('.//td[5]/text()').extract()[0]
            item['date']=date
            #地点
            location=job.xpath('.//td[4]/text()').extract()[0]
            item['location']=location
            #人数
            num = job.xpath('.//td[3]/text()').extract()[0]
            item['num'] = num
            #职位类别
            type = job.xpath('.//td[2]/text()').extract()#['XXX']
            print(type)
            type=self.getvalue(type)

            item['type'] = type

            #职位名称
            name=job.xpath('.//td[1]/a/text()').extract()[0]
            item['name']=name
            #链接
            url = job.xpath('.//td[1]/a/@href').extract()[0]
            # 比较低级
            # url='https://hr.tencent.com/'+url
            #高级  #拼接全路径
            url = request.urljoin(response.url,url)
            item['url'] = url
            # print(name+'\t'+type+'\t'+num+'\t'+location+'\t'+date+'\t'+url)
            print(url)
            print('~~~~~~~~~~~')

            # yield item
            #请求详情页，二级流程
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={'data':item})

        #下一页
        next_url=response.xpath('//a[@id="next"]/@href').extract()[0]
        next_url=request.urljoin(response.url,next_url)

        #是否是最后一页
        last_page=response.xpath('//a[@id="next"]/@class').extract()
        last_page=self.getvalue(last_page)
        if last_page!='noactive':
            yield scrapy.Request(url=next_url,callback=self.parse)

    def parse_detail(self,response):
        # print('~~~~~~~~~~~detail~~~~~~~~~~~~`')
        # print(response.text)
        item=response.meta['data']
        with open('detail.html','w',encoding='utf-8') as f:
            f.write(response.body.decode('utf-8'))
        #工作职责
        duty=response.xpath('//tr[@class="c"][1]//li/text()').extract()
        # print(duty)#字符串列表
        duty=''.join(duty)
        item['duty'] = duty
        #工作要求
        rq=response.xpath('//tr[@class="c"][2]//li/text()').extract()
        rq=''.join(rq)
        item['rq']=rq
        # print(duty+'\n')
        # print(rq)
        # print('~~~~~~~~~~~~~~~`')
        yield item

    def getvalue(self,value):

        # return value[0] if value else ''
        if value == []:
            return ''
        else:
            return value[0]