#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import time
import psycopg2
import QueryInstance


class PgsqlQuery(QueryInstance.QueryInstance):
    '''
    Postgres Query interface
    '''

    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.password = config['pwd']
        self.database = config['dbname']
        self.params = 'dbname=%s host=%s port=%s user=%s password=%s' % (
            self.database, self.host, self.port, self.user, self.password)

    def connect(self):
        """
        数据库重连
        """
        flag = True
        while flag:
            try:
                self.connection = psycopg2.connect(self.params)
                self.cur = self.connection.cursor()
                flag = False
            except (psycopg2.DataError, psycopg2.IntegrityError,
                    psycopg2.InternalError, psycopg2.NotSupportedError,
                    psycopg2.OperationalError, psycopg2.ProgrammingError,
                    psycopg2.InterfaceError, psycopg2.DatabaseError):
                time.sleep(0.5)

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            raise e

    def execute(self, query, params=None):
        try:
            if isinstance(query, str):
                self.cur.execute(query, params)
                if query.startswith("insert") or query.startswith("INSERT") \
                        or query.startswith("update") or query.startswith("UPDATE") \
                        or query.startswith("delete") or query.startswith("DELETE"):
                    self.commit()
        except (psycopg2.DataError, psycopg2.IntegrityError,
                psycopg2.InternalError, psycopg2.NotSupportedError,
                psycopg2.OperationalError, psycopg2.ProgrammingError,
                psycopg2.InterfaceError, psycopg2.DatabaseError):
            self.connect()
            if isinstance(query, str):
                self.cur.execute(query)
                if query.startswith("insert") or query.startswith("INSERT") \
                        or query.startswith("update") or query.startswith("UPDATE") \
                        or query.startswith("delete") or query.startswith("DELETE"):
                    self.commit()
        except Exception as e:
            raise e

    def fetchone(self):
        retSet = []
        try:
            retSet = self.cur.fetchone()
        except Exception as e:
            raise e
        finally:
            return retSet

    def fetchall(self):
        retSet = []
        try:
            retSet = self.cur.fetchall()
        except Exception as e:
            raise e
        finally:
            return retSet

    def disconnect(self):
        try:
            self.cur.close()
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            raise e

    def execute_no_commit(self, query, params=None):
        try:
            if isinstance(query, str):
                self.cur.execute(query, params)
        except Exception as e:
            raise e
