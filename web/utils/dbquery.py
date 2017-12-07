#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import dbqueryutil.PgsqlQuery


class DbQuery(object):
    """
    ESPC Universal Query class
    """

    def __init__(self, db=None, dbname=None):
        """
        init
        """
        if 'DB_NAME' in os.environ:
            db_host = os.environ['DB_SERVICE']
            db_port = os.environ['DB_PORT']
            db_username = os.environ['DB_USER']
            db_password = os.environ['DB_PASS']
            db_name = os.environ['DB_NAME']
            self.db_config = {
                'host': db_host,
                'port': db_port,
                'user': db_username,
                'pwd': db_password,
                'dbname': db_name
            }
        self.db = db
        self.dbname = dbname
        if db is None or db == 'pg':
            self.handle = self.get_pgsql_handle()

    def connect(self):
        """
        默认连接pgsql
        """
        if self.db is None or self.db == 'pg':
            self.connect_pgsql()

    def connect_pgsql(self):
        """
        connect pgsql
        """
        try:
            self.handle.connect()
        except Exception as e:
            raise e

    def execute(self, query, params=None):
        """
        默认执行pgsql
        """
        if self.db is None or self.db == 'pg':
            self.execute_pgsql(query, params)

    def execute_no_commit(self, query, params=None):
        if self.db is None or self.db == 'pg':
            self.execute_pgsql_no_commit(query, params)

    def execute_pgsql(self, query, params=None):
        """
        execte session operation
        """
        try:
            self.handle.execute(query, params)
        except Exception as e:
            raise e

    def execute_pgsql_no_commit(self, query, params=None):
        try:
            self.handle.execute_no_commit(query, params)
        except Exception as e:
            raise e

    def fetchone(self):
        """
        默认从pgsql中获取数据
        """
        ret = None
        if self.db is None or self.db == 'pg':
            ret = self.fetchone_pgsql()
        return ret

    def fetchone_pgsql(self):
        """
        get one record from result
        """
        ret = []
        try:
            ret = self.handle.fetchone()
        except Exception as e:
            raise e
        finally:
            return ret

    def fetchall(self):
        """
        默认从pgsql中获取数据
        """
        ret = None
        if self.db is None or self.db == 'pg':
            ret = self.fetchall_pgsql()
        return ret

    def fetchall_pgsql(self):
        """
        get all records from result
        """
        ret = []
        try:
            ret = self.handle.fetchall()
        except Exception as e:
            raise e
        finally:
            return ret

    def disconnect(self):
        """
        默认和pgsql断开连接
        """
        if self.db is None or self.db == 'pg':
            self.disconnect_pgsql()

    def disconnect_pgsql(self):
        """
        disconnect from pgsql
        """
        try:
            self.handle.disconnect()
        except Exception as e:
            raise e

    def get_pgsql_handle(self):
        """
        get QueryInstance
        """
        ret = None
        try:
            ret = dbqueryutil.PgsqlQuery.PgsqlQuery(self.db_config)
        except Exception as e:
            raise e
        finally:
            return ret


if __name__ == '__main__':

    # test pg
    testpg = DbQuery()
    testpg.connect()
    #testpg.execute("select uuid from tbl_asset_info")
    # recordOne = testpg.fetchone()
    # print recordOne
    #recordAll = testpg.fetchall()
    #print recordAll
    testpg.disconnect()
