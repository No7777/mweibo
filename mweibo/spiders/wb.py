# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import scrapy
from mweibo.items import MweiboItem
import json

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    link = ''
    topic = ''
    category = ''
    fid = ''
    def start_requests(self):
        cookies = {
                'SSOLoginState': '1460507872',
                '_T_WM': '5019f6c27a25df40cfba35c3878263f6',
                'SUHB': '02MeoRRxTHadeA', 
                'SUB':'_2A256CeSwDeRxGeRN71EQ9yrJyz-IHXVZ9Yz4rDV6PUJbrdBeLVX5kW1LHet4fsNkp8HAmmqvLnWq_zrP5kFC4w..',
                'M_WEIBOCN_PARAMS': 'luicode=10000011&lfid=100803&fid=100803_-_page_hot_list&uicode=10000011',
                'H5_INDEX': '0_all', 
                'H5_INDEX_TITLE':u'No7小强',  
                'gsid_CTandWM': '4uJbCpOz5nZuVNywNZKml9Pz887'}

        res = scrapy.Request('http://m.weibo.cn/', cookies = cookies, callback = self.after_login)
        yield res

    def after_login(self, response):
        for i in range(1000):
            con = scrapy.Request('http://m.weibo.cn/page/pageJson?containerid=&containerid=100803_-_page_hot_list&lcardid=100803_-_card_home_menu&uid=2493350327&luicode=10000011&lfid=100808773978e11e6ecc64fce0cc308ff83a96&v_p=11&ext=&fid=100803_-_page_hot_list&uicode=10000011&next_cursor=&page=%d' % (i+1), callback = self.topic)
            yield con

    def topic(self, response):
        response = json.loads(response.body)
        card_group = response['cards'][0]['card_group']
        for card in card_group:
            url = card['scheme']
            self.topic = card['card_type_name']
            self.link = card['actionlog']['oid']
            self.category = card['category']
            self.fid = card['actionlog']['fid']
            info = scrapy.Request(url, callback = self.display)
            yield info

    def display(self, response):
        for i in range(30):
            dis = scrapy.Request('http://m.weibo.cn/page/pageJson?containerid=%s&containerid=%s&luicode=10000011&lfid=100808b1466288c65d8753b3a72b5be1acb770&v_p=11&ext=&fid=%s&uicode=10000011&next_cursor=2399999960&page=%d' % (self.link, self.link, self.link, i + 1), callback = self.home)
            yield dis

    def home(self, response):
        item = MweiboItem()
        response = json.loads(response.body)
        card_group = response['cards'][0]['card_group']
        for card in card_group:
            try:
                mblog = card['mblog']
                text = mblog['text']
                user = mblog['user']['screen_name']
                gender = mblog['user']['gender']
                reposts_count = mblog['reposts_count']
                comments_count = mblog['comments_count']
                attitudes_count = mblog['attitudes_count']
                time = mblog['created_at']
                item['text'] = text
                item['user'] = user
                item['gender'] =gender
                item['reposts_count'] = reposts_count
                item['comments_count'] = comments_count
                item['attitudes_count'] = attitudes_count
                item['time'] =time
                item['topic'] = self.topic
                item['category'] = self.category
                print item
                with open('fourth.txt', 'aw+') as f:
                    f.write(str(item))
            except:
                continue
