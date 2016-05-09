# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import scrapy
from mweibo.items import MweiboItem
import json
import time
from datetime import datetime

class WeiboSpider(scrapy.Spider):
    name = 'weibo2'
    topic = ''
    category = ''
    content = ''
    desc = ''
    def start_requests(self):
        cookies = {
                'SSOLoginState': '1460507872',
                '_T_WM': '33859cf3d3f852e532799a8a52a6be94',
                'SUHB': '0YhQaQoIYg-OWe', 
                'SUB':'_2A256KBOKDeRxGeRK4lES9S7PyTuIHXVZ0r3CrDV6PUJbrdBeLRD7kW1LHetWoxH_xs-Oxcm5dJh8pYK0zbeHGQ..',
                'M_WEIBOCN_PARAMS': 'luicode=10000011&lfid=100803&fid=100803_-_page_hot_list&uicode=10000011',
                'H5_INDEX': '0_all', 
                'H5_INDEX_TITLE':u'No7小强',  
                'gsid_CTandWM': '4uNnCpOz5Bm8k7R8vOXgTasDk5h',
                'browser': 'd2VpYm9mYXhpYW4=',
                'h5_deviceID': '090b8547ea8b88921e48a34fa364f2e7'}

        res = scrapy.Request('http://m.weibo.cn/', cookies = cookies, callback = self.after_login)
        yield res

    def after_login(self, response):
        for i in range(3):
            #time.sleep(5)
            con = scrapy.Request('http://m.weibo.cn/page/pageJson?containerid=&containerid=100803_-_page_hot_list&luicode=10000011&lfid=100803&v_p=11&ext=&fid=100803_-_page_hot_list&uicode=10000011&next_cursor=&page=%d' % (i+1), callback = self.topic)
            yield con

    def topic(self, response):
        item = MweiboItem()
        response = json.loads(response.body)
        card_group = response['cards'][0]['card_group']
        for card in card_group:
            try:
                item['topic'] = card['card_type_name']
                item['category'] = card['category']
                item['desc1'] = card['desc1']
                item['desc2'] = card['desc2']
                item['time'] = time.time()
                print item
                date = str(datetime.now())
                filename = filter(str.isalnum, date)[:10]
                with open(filename + '.txt', 'aw+') as f:
                    f.write(str(item))
            except:
                continue
