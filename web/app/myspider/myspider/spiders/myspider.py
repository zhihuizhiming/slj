#!/usr/env python3
import sys
sys.path.append('/data/web/utils/')
import os
import scrapy
import time
import json
import urllib.request
import subprocess
from dbquery import DbQuery


class mySpider(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        for i in range(3497, 7090):
            url='http://youzan6.com/post/%s.html' % i
            time.sleep(2)
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
            dir_name = 'myspider-0'
            images_path = '/mnt/img/'+ dir_name
            if os.path.exists(images_path):
                t_cmd = 'rm -rf ' + images_path
                t_ret,t_ret_d = subprocess.getstatusoutput(t_cmd)
            os.mkdir(images_path)
            n = 1
            for img in data['imgs']:
                try:
                    r = urllib.request.Request(img)
                    r.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
                    response = urllib.request.urlopen(r)
                    content = response.read()
                    img_name = images_path + '/' + str(n) + '.jpg'
                    with open(img_name, 'wb') as f:
                        f.write(content)
                        f.close()
                    n += 1
                except Exception as e:
                    print("ERROR: ", e)
            try:
                cmd_str = 'ls ' + images_path + '|wc -l'
                ret1, ret_data = subprocess.getstatusoutput(cmd_str)
                if ret1 == 0:
                    num = int(ret_data)
                    print('num: ', num)
                    if num == 0:
                        return
                    cmd = 'ssh -i /root/.ssh/id_rsa ipfs ipfs add -q -r /export/img/' + dir_name
                    ret, imgdata = subprocess.getstatusoutput(cmd)
                    if ret == 0:
                        image_list = imgdata.split('\n')
                        real_img_list = image_list[:len(image_list) - 1]
                        print(real_img_list)
                        if real_img_list:
                            db = DbQuery()
                            title = data['title']
                            ptime = data['ptime']
                            j_data = {
                                'img_data': real_img_list
                            }
                            sql = "insert into tbl_web_page (title,ptime,images) values (%s, %s, %s)"
                            params = [title, ptime, json.dumps(j_data)]
                            db.connect()
                            db.execute(sql, params)
                            db.disconnect()
            except Exception as e:
                print("ERROR: ", e)
