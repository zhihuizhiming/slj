# -*- coding: utf-8 -*-
import sys
sys.path.append('/data/web/utils/')
import re
import json
import requests

from dbquery import DbQuery
#from utils.dbquery import DbQuery
from logutils import getLogger

Log = getLogger(False, 'test')


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

def get_em(pid, id, leng):
    try:
        em = ''
        num = (leng + 1) if leng <= (id + 3) else (id + 3)
        min_num = 1 if id <= 3 else (id - 2)
        for i in range(min_num, num):
            if i == id:
                em += '<em>' + str(i) + '</em>'
            else:
                em += '<a href="/mm/' + str(pid) + '/' + str(i) + '">' + str(i) + '</a>'
        if num <= (leng - 1):
            em += '<i></i><a href="/mm/' + str(pid) + '/' + str(leng) + '">' + str(leng) + '</a>'
        return em
    except Exception as e:
        Log.error("ERROR: %s", e)

def get_page(pid, id=1):
    db = DbQuery()
    try:
        db.connect()
        sql = "select * from tbl_web_page where id = %s" % pid
        db.execute(sql)
        ret = db.fetchone()
        Log.debug("ret: %s", ret[0])
        if ret:
            title = ret[1]
            ptime = ret[2]
            img_list = json.loads(ret[3])['img_data']
            leng = len(img_list)
            likes = ret [4]
            visit = ret[5]
            imgsrc = img_list[int(id) - 1]
            em = get_em(pid, int(id), leng)
            Log.debug('em: %s', em)
            next_num = (int(id) + 1) if (int(id) + 1) < leng else leng
            html_dict = {
                '{TITLE}': title,
                '{PICINFO}': '[2015, '+ str(pid) + ', ' + str(leng)+']',
                '{TIME}': ptime,
                '{LIKE}': str(likes),
                '{VISIT}': str(visit),
                '{IMGSRC}': '/ip/'+imgsrc,
                '{HREF}': '/mm/'+ str(pid) + '/' + str(next_num),
                '{PRE}': '/mm/' + str(int(pid) - 1),
                '{EM}': em,
                '{NEXT}': '/mm/' + str(pid) + '/' + str(next_num),
                '{IMGLIST}': str(img_list)
            }
            html = open('/data/web/static/html/test.html', 'rb').read()
            html = html.decode('utf-8')
            html = multiple_replace(html, html_dict)
            #Log.debug("html: %s" % html)
            return html
        else:
            Log.warn("find %s :404" % pid)
    except Exception as e:
        Log.error("error: %s" % e)
    finally:
        db.disconnect()

def get_img(qm):
    try:
        ret = requests.get('https://ipfs.io/ipfs/'+qm)
        return ret.content
    except Exception as e:
        Log.error("error: %s", e)



if __name__ == '__main__':
    get_page(12)
