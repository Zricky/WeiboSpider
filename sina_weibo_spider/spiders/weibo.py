# -*- coding: utf-8 -*-
import scrapy
import re
from sina_weibo_spider.items import SinaWeiboSpiderItem
file_name = 'sina'
class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']

    user_name = 'pgone'
    start_url = 'https://weibo.cn'

    def start_requests(self):
        detail_url = self.start_url + '/' + self.user_name
        data = {
            'f':'search_0'
        }
        yield scrapy.FormRequest(detail_url, callback=self.parse_user, formdata=data)
    # sina weibo user mian activity
    def parse_user(self, response):
        user_info = response.xpath('//div[@class="ut"]/a/@href').extract()
        user_info_url = self.start_url + user_info[1]
        user_social_intercourse = response.xpath('//div[@class="tip2"]/a/@href').extract()
        user_follow = user_social_intercourse[0]
        user_fans = user_social_intercourse[1]
        user_follow_url = self.start_url + user_follow
        user_fans_url = self.start_url + user_fans

        yield scrapy.Request(user_info_url, callback=self.parse_user_info)

        print('user_fans_url',user_fans_url)

        print('user_follow_url',user_follow_url)


        yield scrapy.Request(user_follow_url, callback=self.parse_user_follows)

        yield scrapy.Request(user_fans_url, callback=self.parse_user_fans)
    # user infomaintion
    def parse_user_info(self,response):
        # auth = '未知'
        # sex = '未知'
        # area = '未知'
        id_ex = response.xpath('//div[@class="c"][2]/a/@href').extract_first()
        id = re.sub('\D','',id_ex)
        info = response.xpath('/html/body/div[7]/text()').extract()
        if '标签:' in info:
            index = info.index('标签:')
            info = info[:index]
            flags = response.xpath('//div[7]/a/text()').extract()
            if '更多>>' in flags:
                flags.remove('更多>>')
        else:
            flags=['...']

        # user_info = response.xpath('//div[@class="c"]').extract()[2]
        # pattern = re.compile(u'<.*?>')
        # infos = re.split(pattern,user_info)
        # name = infos[1].split(':')[1]
        # try:
        #     auth = infos[2].split(':')[1]
        #     sex = infos[3].split(':')[1]
        #     area = infos[4].split(':')[1]
        #     flags_ex = infos[9:]
        #     while '' in flags_ex:
        #         flags_ex.remove('')
        #     if '更多&gt;&gt;' in flags_ex:
        #         flags_ex.remove('更多&gt;&gt;')
        #     while '\xa0' in flags_ex:
        #         flags_ex.remove('\xa0')
        #     flags = flags_ex
        #     if not flags:
        #         flags = ['未知']
        # except :
        #     pass
        # finally:
        weibo_item = SinaWeiboSpiderItem()
        for field in weibo_item.fields:
            try:
                weibo_item[field] = eval(field)
            except NameError:
                print('Field is Not Defined', field)
        yield weibo_item


    # user follows
    def parse_user_follows(self, response):
        items = response.xpath('//tr/td[1]/a/@href').extract()
        for item in items:
            yield scrapy.Request(item, callback=self.parse_social_info)
        next_page_url = response.xpath('//*[@id="pagelist"]/form/div/a[1]/@href').extract_first(default='')
        if(next_page_url):
            yield scrapy.Request(self.start_url+next_page_url,callback=self.parse_user_follows)
    # user fans
    def parse_user_fans(self, response):
        items = response.xpath('//tr/td[1]/a/@href').extract()
        for item in items:
            yield scrapy.Request(item, callback=self.parse_social_info)
        next_page_url = response.xpath('//*[@id="pagelist"]/form/div/a[1]/@href').extract_first(default='')
        if (next_page_url):
            yield scrapy.Request(self.start_url + next_page_url, callback=self.parse_user_follows)
    # #the depth of crawl
    def parse_social_info(self,response):
        user_info = response.xpath('//div[@class="ut"]/a/@href').extract()
        user_info_url = self.start_url + user_info[1]
        yield scrapy.Request(user_info_url, callback=self.parse_user_info)


