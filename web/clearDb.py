#!/usr/bin/env python
import sys
sys.path.append('/data/web/utils/')
from dbquery import DbQuery
import json

def clear_db():
    try:
        db = DbQuery()
        db.connect()
        offset = 0
        while True:
            sql = "select id,images from tbl_web_page limit 100 offset %s"
            params = [offset]
            db.execute(sql, params)
            ret = db.fetchall()
            if ret:
                for i in ret:
                    id = i[0]
                    imgs = json.loads(i[1])
                    data = imgs['img_data']
                    for string in data:
                        if not string.startswith('Qm'):
                            tmp = [string]
                            data = list(set(data) ^ set(tmp))
                    imgs['img_data'] = data
                    sql1 = "update tbl_web_page set images = %s where id = %s"
                    params1 = [json.dumps(imgs), id]
                    db.execute(sql1, params1)
                    offset += 1
            else:
                break
        print("all line:", offset)
        db.disconnect()
    except Exception as e:
        raise e

if __name__ == '__main__':
    clear_db()
