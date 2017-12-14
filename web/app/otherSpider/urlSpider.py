#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import bs4
import time
import requests
import fake_useragent
import os
import re
import json
import random
import subprocess
import sys
sys.path.append('/data/web/utils/')
from dbquery import DbQuery

class GetPictures(object):
    def __init__(self):
        self.url = 'http://www.mmjpg.com/mm/1'
        self.first_num = 102
        self.sum_num = 1190
        self.title = ''
        self.ptime = ''
        self.urls = self.get_urls()
        for url in self.urls:
            self.down_pictures(self.get_img_urls(url))

    # 得到所有套图的第一张所在网页的URL
    def get_urls(self):
        urls = []
        for i in list(range(self.first_num, self.first_num+self.sum_num)):
            url_split = self.url.split('/')
            url_split[-1] = str(i)
            urls.append('/'.join(url_split))
        return urls

    # 得到一共有多少张图
    def get_img_sum_num(self, img_url):
        fa = fake_useragent.UserAgent(verify_ssl=False)
        headers = {'User-Agent': fa.random,
                   'Referer': 'http://www.mmjpg.com'}
        request = requests.get(img_url, headers=headers)
        soup = bs4.BeautifulSoup(request.content, 'lxml')
        self.title = soup.title.string.split('_')[0]
        new_soup = soup.find(name='div',attrs={"class":"info"})
        self.ptime = new_soup.i.string.split(': ')[-1]
        # 获取标签里面的值
        img_sum_number = soup.find_all('a', href=re.compile('/mm'))[8].get_text().strip()
        img_sum_number = int(img_sum_number)
        return img_sum_number

    # 得到该套图中的所有图片的URL
    def get_img_urls(self, url):
        print(url.split('/')[-1])
        fa = fake_useragent.UserAgent(verify_ssl=False)
        headers = {'User-Agent': fa.random,
                   'Referer': 'http://m.mmjpg.com'}
        request = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(request.content, 'lxml')
        first_img_url = soup.find('img').get('src')     # 获取标签值
        url_split = first_img_url.split('/')
        img_urls = []
        for i in list(range(1, self.get_img_sum_num(url)+1)):
            url_split[-1] = (str(i)+'.jpg')
            img_urls.append('/'.join(url_split))
        return img_urls

    # 下载图片
    def down_pictures(self, img_urls):
        dir_name = str(img_urls[0].split('/')[-2])+'-'+str(img_urls[0].split('/')[-3])
        img_name = '/mnt/img/'+ dir_name
        if os.path.exists(img_name):    # 查重 如果这个文件夹存在则跳过 防止重复下载
            time.sleep(1)
            print(img_name+'存在')
            return True
        os.mkdir(img_name)
        for img_url in img_urls:
            fa = fake_useragent.UserAgent(verify_ssl=False)
            headers = {'User-Agent': fa.random,
                       'Referer': 'http://m.mmjpg.com'}
            request = requests.get(img_url, headers=headers)

            with open(img_name + u'/' + img_url.split('/')[-1], 'wb') as f:
                f.write(request.content)    # contents返回的为二进制   text返回的为union类型
                f.close()
                time.sleep(random.random()*2)
        cmd_str = 'ls ' + img_name + '|wc -l'
        ret, ret_data = subprocess.getstatusoutput(cmd_str)
        if ret == 0:
            num = int(ret_data)
            print('num: ', num)
            if num == 0:
                return True
            cmd = 'ssh -i /root/.ssh/id_rsa ipfs ipfs add -q -r /export/img/'+dir_name
            ret, imgdata = subprocess.getstatusoutput(cmd)
            image_list = imgdata.split('\n')
            real_img_list = image_list[:len(image_list) - 1]
            print(real_img_list)
            if real_img_list:
                try:
                    db = DbQuery()
                    title = self.title
                    ptime = self.ptime
                    j_data = {
                        'img_data': real_img_list
                    }
                    sql = "insert into tbl_web_page (title,ptime,images) values (%s, %s, %s)"
                    params = [title, ptime, json.dumps(j_data)]
                    db.connect()
                    db.execute(sql, params)
                    db.disconnect()
                except Exception as e:
                    raise e

# 运行程序
if __name__ == '__main__':
    GetPictures()