#!/usr/env python3
import sys
sys.path.append('/data/web/utils/')
import scrapy
import time
import json
import urllib.request
import subprocess
from dbquery import DbQuery


class mySpider(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        for i in range(802,7090):
            url='http://youzan6.com/post/%s.html' % i
            time.sleep(3)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        img_data = []
        quote = response.css('div.box-post')
        data = {
            'title': quote.css("div.post-hd div.post-info h1.post-title::text").extract_first(),
            'ptime': quote.css("div.post-hd div.post-info p.post-extra").css("em")[1].css("em::text").extract_first(),
            'imgs': response.css('img.b-lazy::attr(data-src)').extract()
        }

        if data['imgs']:
            for img in data['imgs']:
                try:
                    r = urllib.request.Request(img)
                    r.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
                    response = urllib.request.urlopen(r)
                    content = response.read()

                    with open('/mnt/img/1.jpg', 'wb') as f:
                        f.write(content)
                        f.close()
                except Exception as e:
                    print("ERROR: ", e)
                try:
                    ret, imgdata = subprocess.getstatusoutput("ssh -i /root/.ssh/id_rsa ipfs "
                                                           "'ipfs add /export/img/1.jpg && rm -rf /export/img/1.jpg'")
                    print("ret:", ret)
                    if ret == 0:
                        imgdata = imgdata.split(' ')
                        print("ipfs data:", imgdata[1])
                        img_data.append(imgdata[1])
                except Exception as e:
                    print("ERROR: ", e)
            print("data: imgs: %s" % img_data)
            if img_data:
                try:
                    db = DbQuery()
                    title = data['title']
                    ptime = data['ptime']
                    j_data = {
                        'img_data': img_data
                    }
                    sql = "insert into tbl_web_page (title,ptime,images) values (%s, %s, %s)"
                    params = [title, ptime, json.dumps(j_data)]
                    db.connect()
                    db.execute(sql, params)
                    db.disconnect()
                except Exception as e:
                    raise e
