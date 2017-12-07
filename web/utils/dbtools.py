#!/usr/bin/env python
#-*- coding=utf-8 -*-

import time
import traceback

import psycopg2
from DBUtils import PooledDB

class _SocDB(object):
    def __init__(self, dbname, conn_num=3):
        """数据库连接池"""
        cm = ConfigManager()
        self.pool = PooledDB.PooledDB(psycopg2,
                                mincached=0,
                                maxcached=conn_num,
                                maxshared=conn_num,
                                maxconnections=0,
                                blocking=True,
                                maxusage=100,
                                host=cm.get_db_conf("host"),
                                user=cm.get_db_conf("username"),
                                password=cm.get_db_conf("password"),
                                database=dbname,
                                port=cm.get_db_conf("port"))

    def get_conn(self):
        """获取连接"""
        flag = True
        while flag:
            try:
                conn = SchedConn(self.pool.connection())
                flag = False
            except (psycopg2.DataError, psycopg2.IntegrityError,
                    psycopg2.InternalError, psycopg2.NotSupportedError,
                    psycopg2.OperationalError, psycopg2.ProgrammingError,
                    psycopg2.InterfaceError, psycopg2.DatabaseError):
                time.sleep(0.5)
        return conn

class SchedConn(object):
    def __init__(self, connection):
        """数据库连接对象"""
        self.conn = connection
        self.cur = self.conn.cursor()

    def close(self):
        """关闭游标，关闭数据库连接"""
        try:
            self.cur.close()
            self.conn.close()
        except:
            pass

    def commit(self):
        """提交操作"""
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def select(self, sqlcomment, params=None, dict_ret=True):
        """执行查询操作并返回字典结果"""
        convert = lambda x : x.strip() if type(x) == str else x
        try:
            if params:
                self.cur.execute(sqlcomment, params)
            else:
                self.cur.execute(sqlcomment)
            self.commit()
            if dict_ret:
                data = [dict((self.cur.description[i][0].strip(), \
                    convert(value)) for i, value in enumerate(row)) \
                                    for row in self.cur.fetchall()]
            else:
                data = self.cur.fetchall()
            return data
        except:
            traceback.print_exc()
            return None
    
    def execute(self, sqlcomment, params=None):
        """执行插入，修改等sql操作"""
        try:
            if params:
                self.cur.execute(sqlcomment, params)
            else:
                self.cur.execute(sqlcomment)
            self.commit()
        except:
            self.conn.rollback()
            raise Exception(traceback.format_exc())

    def _execute(self,sqlcomment, params=None):
        try:
            if params:
                self.cur.execute(sqlcomment, params)
            else:
                self.cur.execute(sqlcomment)
        except:
            raise Exception(traceback.format_exc())

    def execute_batch(self, sqlcomment, params=None):
        """执行批量插入"""
        try:
            if params:
                args_str = ','.join(self.cur.mogrify("%s", (p, )) for p in params)
                self.cur.execute(sqlcomment + args_str)
            self.commit()
        except:
            self.conn.rollback()
            raise Exception(traceback.format_exc())
                

class _SchedDB(_SocDB):
    def __init__(self, conn_num=10):
        _SocDB.__init__(self, 'espc', conn_num=conn_num)

SchedDB = _SchedDB()
TvmDB = SchedDB

if __name__ == "__main__":
    conn = SchedDB.get_conn()
    sql = "select * from tvm_asset_info;"
    print(conn.select(sql))
    conn.close()

